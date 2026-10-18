#!/usr/bin/env python3
"""Module 13 - Python for AI Engineering - offline, deterministic lab.

The lab uses the Python standard library only. No network, no NumPy, no
pandas. It builds the small toolkit that later lessons reuse:

    exercise 1  a Record dataclass and a CSV loader
    exercise 2  a seeded train and test split
    exercise 3  a mini-batch generator
    exercise 4  dot product, mean and a standardizer
    exercise 5  three silent bugs, demonstrated and then fixed
    exercise 6  a speed and memory measurement report

Every value printed here is reproducible. Time is measured but the seconds
are not printed, because a wall-clock number changes on every machine; the
report prints the repeat count instead. Memory is printed as a coarse,
rounded quantity so that it does not move between runs.

Run:
    python3 modules/13_python_for_ai_engineering/lab.py
"""

from __future__ import annotations

import csv
import math
import operator
import random
import tempfile
import time
import tracemalloc
from dataclasses import dataclass
from itertools import islice
from pathlib import Path

# A fixed seed makes every random draw reproducible: the same seed produces the
# same dataset on every machine and every run.
SEED = 7

# 400 records is the size that the source lesson's main.py uses.
ROW_COUNT = 400

# Split and batch sizes from the source lesson's complete run.
TEST_FRACTION = 0.2
BATCH_SIZE = 48

# Sizes for the measurement step. Small enough that the whole lab finishes in
# well under a second, large enough that the memory difference is visible.
VECTOR_SIZE = 200_000
MEMORY_N = 100_000

KIB = 1024


# ---------------------------------------------------------------------------
# the toolkit
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Record:
    """One sample: a tuple of float features and an integer label.

    frozen=True means the object cannot change after creation, so it can be
    used as a dict key or put in a set.
    """

    features: tuple[float, ...]
    label: int


def make_dataset(n=ROW_COUNT, seed=SEED):
    """Build `n` records from two clusters, with a seeded generator."""
    rng = random.Random(seed)
    centers = {0: (2.0, 50.0), 1: (4.0, 70.0)}
    spreads = (1.0, 10.0)
    records = []
    for index in range(n):
        label = index % 2
        features = tuple(rng.gauss(center, spread) for center, spread in zip(centers[label], spreads))
        records.append(Record(features, label))
    return records


def record_to_row(record):
    """Turn a Record into a plain dict with x1, x2, ... and a label key."""
    row = {"x{}".format(i + 1): value for i, value in enumerate(record.features)}
    row["label"] = record.label
    return row


def save_records_csv(records, path):
    """Write the records to `path` as CSV and return the Path."""
    path = Path(path)
    rows = [record_to_row(record) for record in records]
    if not rows:
        raise ValueError("no records to save")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def row_to_record(row, names, label_field="label"):
    """Convert one CSV row (all values are strings) into a Record."""
    if label_field not in row:
        raise ValueError("row has no {!r} field: {}".format(label_field, row))
    if set(row) != {*names, label_field}:
        raise ValueError("row fields {} do not match {}".format(list(row), [*names, label_field]))
    return Record(tuple(float(row[name]) for name in names), int(row[label_field]))


def load_records(path, label_field="label"):
    """Read a CSV file into a list of Record objects."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return []
    names = [key for key in rows[0] if key != label_field]
    return [row_to_record(row, names, label_field) for row in rows]


def train_test_split(items, test_fraction=TEST_FRACTION, seed=SEED):
    """Split `items` into train and test with a private seeded generator."""
    if not 0.0 < test_fraction < 1.0:
        raise ValueError("test_fraction must be between 0 and 1, got {}".format(test_fraction))
    if len(items) < 2:
        raise ValueError("need at least 2 items to split, got {}".format(len(items)))
    order = list(range(len(items)))
    random.Random(seed).shuffle(order)
    n_test = min(max(1, round(len(items) * test_fraction)), len(items) - 1)
    test = [items[i] for i in order[:n_test]]
    train = [items[i] for i in order[n_test:]]
    return train, test


def batches(items, batch_size, drop_last=False):
    """Return a generator that yields lists of at most `batch_size` items.

    The argument check is in this outer function, not in the generator, so a
    bad batch_size raises at once instead of later inside a training loop.
    """
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1, got {}".format(batch_size))
    return _batch_iter(iter(items), batch_size, drop_last)


def _batch_iter(iterator, batch_size, drop_last):
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch or (drop_last and len(batch) < batch_size):
            return
        yield batch


def dot(a, b):
    """Dot product. strict=True raises if the two vectors differ in length."""
    return sum(x * y for x, y in zip(a, b, strict=True))


def mean(values):
    """Arithmetic mean; raises on an empty input."""
    if not values:
        raise ValueError("mean() needs at least one value")
    return sum(values) / len(values)


def std(values):
    """Population standard deviation (divide by n, like statistics.pstdev)."""
    mu = mean(values)
    return math.sqrt(sum((value - mu) ** 2 for value in values) / len(values))


def column_stats(rows):
    """Return (means, standard deviations) for the columns of `rows`."""
    columns = list(zip(*rows))
    return [mean(column) for column in columns], [std(column) for column in columns]


def make_standardizer(rows):
    """Return a closure that standardizes a row with the statistics of `rows`.

    The statistics are computed once, from the training rows, and the returned
    function keeps them. A constant column has std 0, so its scale becomes 1.
    """
    means, stds = column_stats(rows)
    scales = [s if s > 0 else 1.0 for s in stds]

    def standardize(row):
        return [(value - m) / s for value, m, s in zip(row, means, scales, strict=True)]

    return standardize


def add_bad(item, bucket=[]):
    """The buggy version: the default list is created once, at def time."""
    bucket.append(item)
    return bucket


def add_good(item, bucket=None):
    """The correct version: a new list is created inside the call."""
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def dot_index_loop(a, b):
    total = 0.0
    for index in range(len(a)):
        total += a[index] * b[index]
    return total


def dot_map(a, b):
    return sum(map(operator.mul, a, b))


def best_time(fn, *args, repeat=5):
    """Return the fastest of `repeat` runs, in seconds."""
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - start)
    return min(times)


def peak_bytes(fn):
    """Return the peak number of traced bytes while `fn()` runs."""
    tracemalloc.start()
    try:
        fn()
        return tracemalloc.get_traced_memory()[1]
    finally:
        tracemalloc.stop()


def sum_squares_list(n):
    return sum([i * i for i in range(n)])


def sum_squares_generator(n):
    return sum(i * i for i in range(n))


def bucket_kib(value_bytes, granularity_kib=64):
    """Round a byte count up to a coarse, stable KiB bucket.

    `tracemalloc` peaks can move by a few kilobytes between runs, so the raw
    figure is not printed directly; a rounded bucket keeps the report stable.
    """
    step = granularity_kib * KIB
    return ((value_bytes + step - 1) // step) * step // KIB


# ---------------------------------------------------------------------------
# exercise 1
# ---------------------------------------------------------------------------

def exercise_1():
    """Define Record and load a self-written CSV back into records."""
    workdir = tempfile.mkdtemp(prefix="mod13_ex1_")
    try:
        records = make_dataset(ROW_COUNT, seed=SEED)
        path = save_records_csv(records, Path(workdir) / "data.csv")
        loaded = load_records(path)

        first = loaded[0]
        columns = sorted(record_to_row(first))
        print("  file:        {}".format(Path(path).name))
        print("  rows:        {}".format(len(loaded)))
        print("  columns:     {}".format(columns))
        print("  features per row: {}".format(len(first.features)))
        print("  labels (sorted):  {}".format(sorted({record.label for record in loaded})))
        counts = {}
        for record in loaded:
            counts[record.label] = counts.get(record.label, 0) + 1
        print("  label counts:     {}".format(
            " ".join("{}={}".format(k, counts[k]) for k in sorted(counts))))
        print("  roundtrip equals the original records: {}".format(loaded == records))
        print("  first record: Record(features=({:.3f}, {:.3f}), label={})".format(
            first.features[0], first.features[1], first.label))
        print("  type of one item: {}".format(type(first).__name__))

        assert len(loaded) == ROW_COUNT
        assert loaded == records, "CSV roundtrip must preserve every value"
        assert isinstance(first, Record)
        assert sum(counts.values()) == ROW_COUNT

        print("[OK] exercise_1 — Record dataclass and CSV loader")
        return loaded
    finally:
        import shutil

        shutil.rmtree(workdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# exercise 2
# ---------------------------------------------------------------------------

def exercise_2():
    """Split the records into train and test with a seeded generator."""
    records = make_dataset(ROW_COUNT, seed=SEED)
    train, test = train_test_split(records, test_fraction=TEST_FRACTION, seed=SEED)

    print("  input rows:  {}".format(len(records)))
    print("  test share:  {}".format(TEST_FRACTION))
    print("  train rows:  {}".format(len(train)))
    print("  test rows:   {}".format(len(test)))
    print("  train + test == input: {}".format(len(train) + len(test) == len(records)))
    print("  records in both splits: {}".format(len(set(train) & set(test))))

    again_train, again_test = train_test_split(records, test_fraction=TEST_FRACTION, seed=SEED)
    print("  same seed reproduces the same split: {}".format(
        [r.features for r in again_train] == [r.features for r in train]))

    other_train, _ = train_test_split(records, test_fraction=TEST_FRACTION, seed=1)
    print("  seed 1 changes the first training record: {}".format(
        [round(v, 3) for v in other_train[0].features] != [round(v, 3) for v in train[0].features]))

    print("  input list untouched (first feature still {:.3f}): {}".format(
        records[0].features[0], records[0].features[0] == make_dataset(1, seed=SEED)[0].features[0]))

    assert len(train) == 320 and len(test) == 80
    assert len(train) + len(test) == ROW_COUNT
    assert set(train) & set(test) == set()
    assert [r.features for r in again_train] == [r.features for r in train]
    assert other_train[0].features != train[0].features

    print("[OK] exercise_2 — seeded train and test split")
    return train, test


# ---------------------------------------------------------------------------
# exercise 3
# ---------------------------------------------------------------------------

def exercise_3():
    """Yield mini-batches from a generator, and rebuild it for each epoch."""
    items = list(range(320))

    sizes = [len(batch) for batch in batches(items, BATCH_SIZE)]
    print("  items:            {}".format(len(items)))
    print("  batch size:       {}".format(BATCH_SIZE))
    print("  batch sizes:      {}".format(sizes))
    print("  number of batches: {}".format(len(sizes)))

    dropped = [len(batch) for batch in batches(items, BATCH_SIZE, drop_last=True)]
    print("  with drop_last:   {}".format(dropped))

    squares = (i * i for i in range(7))
    print("  batches over a generator expression: {}".format(
        [len(batch) for batch in batches(squares, 3)]))

    print("  one new generator per epoch:")
    for epoch in range(2):
        epoch_sizes = [len(batch) for batch in batches(items, BATCH_SIZE)]
        print("    epoch {}: {}".format(epoch, epoch_sizes))

    assert sizes == [48] * 6 + [32]
    assert sum(sizes) == 320
    assert dropped == [48] * 6
    assert [len(batch) for batch in batches(range(7), 3)] == [3, 3, 1]

    print("[OK] exercise_3 — mini-batch generator")
    return sizes


# ---------------------------------------------------------------------------
# exercise 4
# ---------------------------------------------------------------------------

def exercise_4():
    """Implement dot product, mean and a standardizer in pure Python."""
    print("  dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) = {}".format(dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])))

    values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    print("  values: {}".format(values))
    print("  mean:   {}".format(mean(values)))
    print("  std:    {}  (population, divide by n)".format(std(values)))

    train_rows = [(1.0, 100.0), (2.0, 300.0), (3.0, 500.0)]
    standardize = make_standardizer(train_rows)
    scaled_train = [[round(value, 3) for value in standardize(row)] for row in train_rows]
    print("  train rows standardized: {}".format(scaled_train))
    print("  a test row (4.0, 700.0): {}".format([round(value, 3) for value in standardize((4.0, 700.0))]))

    means_after = column_stats([row for row in scaled_train])[0]
    print("  means of the standardized training rows: {}".format([round(value, 6) for value in means_after]))

    lengths_mismatch = False
    try:
        dot([1.0, 2.0], [1.0, 2.0, 3.0])
    except ValueError:
        lengths_mismatch = True
    print("  dot with two different lengths raises ValueError: {}".format(lengths_mismatch))

    flat = make_standardizer([(5.0, 1.0), (5.0, 3.0), (5.0, 5.0)])
    print("  a constant column keeps a scale of 1: {}".format([round(v, 3) for v in flat((5.0, 7.0))]))

    assert round(dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]), 6) == 32.0
    assert round(mean(values), 6) == 5.0
    assert round(std(values), 6) == 2.0
    assert scaled_train == [[-1.225, -1.225], [0.0, 0.0], [1.225, 1.225]]
    assert [round(value, 6) for value in means_after] == [0.0, 0.0]
    assert lengths_mismatch is True

    print("[OK] exercise_4 — dot product, mean and standardizer")
    return scaled_train


# ---------------------------------------------------------------------------
# exercise 5
# ---------------------------------------------------------------------------

def exercise_5():
    """Demonstrate and then fix three bugs that give wrong results silently."""
    print("  bug 1 - two names refer to one list")

    weights = [0.5, -1.2, 3.0]
    alias = weights
    alias[0] = 99.0
    print("    weights after alias[0] = 99.0:  {}".format(weights))
    print("    alias is weights (the same object): {}".format(alias is weights))

    independent = list(weights)
    independent[1] = 0.0
    print("    after independent = list(weights); independent[1] = 0.0:")
    print("      weights     {}".format(weights))
    print("      independent {}".format(independent))

    print("  bug 2 - a mutable default argument keeps its value between calls")
    print("    add_bad('a')  -> {}".format(add_bad("a")))
    print("    add_bad('b')  -> {}   (the old item is still there)".format(add_bad("b")))
    print("    add_good('a') -> {}".format(add_good("a")))
    print("    add_good('b') -> {}   (a new list for each call)".format(add_good("b")))

    print("  bug 3 - a generator is empty after one pass")

    def squares_factory():
        return (i * i for i in range(5))

    used_up = squares_factory()
    first_pass = list(used_up)
    second_pass = list(used_up)
    print("    first  pass: {}".format(first_pass))
    print("    second pass: {}   (the generator is used up)".format(second_pass))
    print("    fixed - call the factory again for each epoch:")
    print("      epoch 0: {}".format(list(squares_factory())))
    print("      epoch 1: {}".format(list(squares_factory())))

    assert alias is weights
    assert weights == [99.0, -1.2, 3.0]
    assert independent == [99.0, 0.0, 3.0]
    assert add_bad("c") == ["a", "b", "c"], "the buggy default really accumulates"
    assert add_good("c") == ["c"]
    assert first_pass == [0, 1, 4, 9, 16]
    assert second_pass == []
    assert list(squares_factory()) == [0, 1, 4, 9, 16]

    print("[OK] exercise_5 — shared list, mutable default and used-up generator")
    return {"shared": True, "mutable_default": True, "used_up_generator": True}


# ---------------------------------------------------------------------------
# exercise 6
# ---------------------------------------------------------------------------

def exercise_6():
    """Print a measurement report: repeat counts and rounded peak memory."""
    rng = random.Random(SEED)
    a = [rng.random() for _ in range(VECTOR_SIZE)]
    b = [rng.random() for _ in range(VECTOR_SIZE)]

    timings = {
        "index loop": best_time(dot_index_loop, a, b),
        "zip generator": best_time(dot, a, b),
        "map + mul": best_time(dot_map, a, b),
    }
    results = {
        "index loop": dot_index_loop(a, b),
        "zip generator": dot(a, b),
        "map + mul": dot_map(a, b),
    }
    agree = len({round(value, 6) for value in results.values()}) == 1

    list_peak = bucket_kib(peak_bytes(lambda: sum_squares_list(MEMORY_N)), granularity_kib=1024)
    generator_peak = bucket_kib(peak_bytes(lambda: sum_squares_generator(MEMORY_N)), granularity_kib=64)

    print("  speed: dot product of {:,} floats, best of 5".format(VECTOR_SIZE))
    print("    variants measured: {}".format(sorted(timings)))
    print("    repeats per variant: 5")
    print("    all three variants agree: {}".format(agree))
    print("    seconds are not printed - a wall-clock number is not stable")
    print("    every timing was positive: {}".format(all(seconds > 0 for seconds in timings.values())))
    print("  memory: peak bytes to sum {:,} squares".format(MEMORY_N))
    print("    list       (rounded up to 1 MiB): {} KiB".format(list_peak))
    print("    generator  (rounded up to 64 KiB): {} KiB".format(generator_peak))
    print("    the generator peak is smaller: {}".format(generator_peak < list_peak))
    print("    the generator holds one item at a time; the list holds every item")

    assert agree is True
    assert all(seconds > 0 for seconds in timings.values())
    assert generator_peak < list_peak
    assert list_peak >= 3072, "a list of 100,000 squares is at least a few MiB"

    print("[OK] exercise_6 — speed and memory measurement report")
    return {"variants": sorted(timings), "generator_peak_kib": generator_peak, "list_peak_kib": list_peak}


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------

EXERCISES = [
    ("exercise_1", exercise_1),
    ("exercise_2", exercise_2),
    ("exercise_3", exercise_3),
    ("exercise_4", exercise_4),
    ("exercise_5", exercise_5),
    ("exercise_6", exercise_6),
]


def main():
    print("=" * 62)
    print("Module 13 - Python for AI Engineering - offline lab")
    print("=" * 62)

    for index, (name, function) in enumerate(EXERCISES, start=1):
        print()
        print("--- {} / 6: {} ---".format(index, name))
        function()

    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
