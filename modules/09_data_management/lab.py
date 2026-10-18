#!/usr/bin/env python3
"""Module 09 - Data Management - offline, deterministic lab.

The lab uses the Python standard library only. No network, no `datasets`
package, no pandas, no numpy. Every dataset it works on is a CSV file that
this script writes into a temporary directory and deletes again.

Run:
    python3 modules/09_data_management/lab.py
"""

import csv
import json
import os
import random
import shutil
import tempfile
import tracemalloc

# A fixed seed makes the split reproducible: the same seed produces the same
# split on every machine and every run.
SEED = 42

# Row count for the generated CSV. 20000 rows is large enough that the
# difference between streaming and loading is measurable, and small enough
# that the whole lab finishes in well under a second.
ROW_COUNT = 20000

KIB = 1024


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _write_sample_csv(directory, name="reviews.csv", rows=ROW_COUNT):
    """Write a deterministic CSV into `directory` and return its path."""
    path = os.path.join(directory, name)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "text", "label"])
        writer.writeheader()
        for index in range(rows):
            writer.writerow(
                {
                    "id": index,
                    "text": "sample review text number {:05d} for the data management lab".format(index),
                    "label": "positive" if index % 2 == 0 else "negative",
                }
            )
    return path


def _stream_records(path):
    """Yield one record at a time. This is the streaming (lazy) reader."""
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            yield dict(row)


def _load_records(path):
    """Read every record into a list. This is the loading (eager) reader."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _round_up_kib(value_bytes, granularity_kib=64):
    """Round a byte count up to a coarse, stable KiB bucket.

    `tracemalloc` peaks are allocator-dependent: the raw figure can move by a
    few kilobytes between runs and between Python builds. Rounding up to a
    64 KiB bucket removes that noise, so the number printed here is
    reproducible instead of unstable.
    """
    step = granularity_kib * KIB
    return ((value_bytes + step - 1) // step) * step // KIB


# ---------------------------------------------------------------------------
# exercise 1
# ---------------------------------------------------------------------------

def exercise_1():
    """Read a CSV file as a list of records."""
    workdir = tempfile.mkdtemp(prefix="mod09_ex1_")
    try:
        path = _write_sample_csv(workdir)
        records = _load_records(path)

        labels = sorted({record["label"] for record in records})
        counts = {}
        for record in records:
            counts[record["label"]] = counts.get(record["label"], 0) + 1

        print("  file:       {}".format(os.path.basename(path)))
        print("  rows:       {}".format(len(records)))
        print("  columns:    {}".format(sorted(records[0].keys())))
        print("  labels:     {}".format(labels))
        print("  label count:")
        for label in sorted(counts):
            print("    {:<9} {}".format(label, counts[label]))
        print("  first row:  id={} label={}".format(records[0]["id"], records[0]["label"]))
        print("  last row:   id={} label={}".format(records[-1]["id"], records[-1]["label"]))
        print("  type of first record: {}".format(type(records[0]).__name__))

        assert len(records) == ROW_COUNT
        assert sorted(records[0].keys()) == ["id", "label", "text"]
        assert records[0]["id"] == "0"
        assert records[-1]["id"] == str(ROW_COUNT - 1)
        assert sum(counts.values()) == ROW_COUNT

        print("[OK] exercise_1 - read a CSV file as a list of records")
        return records
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# exercise 2
# ---------------------------------------------------------------------------

def exercise_2():
    """Compare the peak memory of streaming against loading."""
    workdir = tempfile.mkdtemp(prefix="mod09_ex2_")
    try:
        path = _write_sample_csv(workdir)

        tracemalloc.start()
        streamed = 0
        for _record in _stream_records(path):
            streamed += 1
        _current, stream_peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        loaded = _load_records(path)
        _current, load_peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Rounded, reproducible quantities: see `_round_up_kib` for why the
        # raw byte count is not printed directly.
        stream_peak_kib = _round_up_kib(stream_peak_bytes)
        load_peak_kib = _round_up_kib(load_peak_bytes)
        ratio = load_peak_kib // stream_peak_kib

        print("  rows read by streaming: {}".format(streamed))
        print("  rows held by loading:   {}".format(len(loaded)))
        print("  stream peak (rounded up to 64 KiB): {} KiB".format(stream_peak_kib))
        print("  load   peak (rounded up to 64 KiB): {} KiB".format(load_peak_kib))
        print("  load peak / stream peak: about {}x".format(ratio))
        print("  streaming keeps memory constant; loading grows with row count.")

        assert streamed == len(loaded) == ROW_COUNT
        assert stream_peak_kib < load_peak_kib, "streaming must use less peak memory than loading"
        assert ratio >= 10, "expected an order-of-magnitude difference, got {}x".format(ratio)

        print("[OK] exercise_2 - streaming and loading peak memory compared")
        return {"stream_peak_kib": stream_peak_kib, "load_peak_kib": load_peak_kib, "ratio": ratio}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# exercise 3
# ---------------------------------------------------------------------------

def split_records(records, seed=SEED, train_ratio=0.70, val_ratio=0.15):
    """Split `records` into train/validation/test with a seeded generator.

    `random.Random(seed)` is a seeded generator: it is deterministic and is
    the only permitted use of `random` in this course.
    """
    total = len(records)
    indices = list(range(total))
    random.Random(seed).shuffle(indices)

    n_train = int(total * train_ratio)
    n_val = int(total * val_ratio)

    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]

    return {
        "train": [records[i] for i in train_idx],
        "validation": [records[i] for i in val_idx],
        "test": [records[i] for i in test_idx],
    }


def exercise_3():
    """Create a 70/15/15 train/validation/test split with a fixed seed."""
    workdir = tempfile.mkdtemp(prefix="mod09_ex3_")
    try:
        path = _write_sample_csv(workdir)
        records = _load_records(path)

        splits = split_records(records, seed=SEED)
        total = len(records)

        for name in ("train", "validation", "test"):
            part = splits[name]
            print(
                "  {:<11} {:>6} rows ({:.1%})  first id={}".format(
                    name, len(part), len(part) / total, part[0]["id"]
                )
            )

        sizes = sorted(name for name in splits)
        print("  split names (sorted): {}".format(sizes))

        again = split_records(records, seed=SEED)
        same_first_ids = all(splits[name][0]["id"] == again[name][0]["id"] for name in sizes)
        print("  same seed reproduces the same first record: {}".format(same_first_ids))

        other_seed = split_records(records, seed=1234)
        print("  seed 1234 changes the first train id: {} -> {}".format(
            splits["train"][0]["id"], other_seed["train"][0]["id"]
        ))

        assert sum(len(splits[name]) for name in sizes) == total
        assert len(splits["train"]) == 14000
        assert len(splits["validation"]) == 3000
        assert len(splits["test"]) == 3000
        assert same_first_ids
        assert splits["train"][0]["id"] != other_seed["train"][0]["id"]

        print("[OK] exercise_3 - 70/15/15 split with a fixed seed")
        return splits
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# ---------------------------------------------------------------------------
# exercise 4
# ---------------------------------------------------------------------------

# Trade-offs taken from the source lesson's format comparison table.
FORMAT_TABLE = {
    "CSV": {"size": "large", "read_speed": "slow", "best_for": "human readability, spreadsheets"},
    "JSON": {"size": "large", "read_speed": "slow", "best_for": "APIs, nested data"},
    "Parquet": {"size": "small", "read_speed": "fast", "best_for": "analytics, columnar queries"},
    "Arrow": {"size": "small", "read_speed": "fastest", "best_for": "in-memory processing (used internally by the datasets library)"},
}

FORMAT_SCENARIOS = [
    {
        "name": "analyst runs column-level aggregate queries",
        "human_readable": False,
        "nested": False,
        "columnar_analytics": True,
        "in_memory": False,
    },
    {
        "name": "training loop reads batches in memory",
        "human_readable": False,
        "nested": False,
        "columnar_analytics": False,
        "in_memory": True,
    },
    {
        "name": "reviewer opens the file in a spreadsheet",
        "human_readable": True,
        "nested": False,
        "columnar_analytics": False,
        "in_memory": False,
    },
    {
        "name": "service returns nested records over an API",
        "human_readable": False,
        "nested": True,
        "columnar_analytics": False,
        "in_memory": False,
    },
]


def choose_format(human_readable, nested, columnar_analytics, in_memory):
    """Pick a storage format from the source table, as data."""
    if in_memory:
        return "Arrow"
    if columnar_analytics:
        return "Parquet"
    if nested:
        return "JSON"
    if human_readable:
        return "CSV"
    return "Parquet"


def exercise_4():
    """Reason over the CSV / JSON / Parquet / Arrow trade-offs."""
    print("  format table (from the source lesson):")
    print("  {:<8} {:<6} {:<10} {}".format("format", "size", "read", "best for"))
    for name in sorted(FORMAT_TABLE):
        row = FORMAT_TABLE[name]
        print("  {:<8} {:<6} {:<10} {}".format(name, row["size"], row["read_speed"], row["best_for"]))

    print("  scenario decisions:")
    decisions = {}
    for scenario in FORMAT_SCENARIOS:
        picked = choose_format(
            human_readable=scenario["human_readable"],
            nested=scenario["nested"],
            columnar_analytics=scenario["columnar_analytics"],
            in_memory=scenario["in_memory"],
        )
        decisions[scenario["name"]] = picked
        print("    {:<48} -> {}".format(scenario["name"], picked))

    print("  rule: Parquet on disk, Arrow in memory, CSV/JSON for interchange.")

    assert decisions["analyst runs column-level aggregate queries"] == "Parquet"
    assert decisions["training loop reads batches in memory"] == "Arrow"
    assert decisions["reviewer opens the file in a spreadsheet"] == "CSV"
    assert decisions["service returns nested records over an API"] == "JSON"
    assert FORMAT_TABLE["Arrow"]["read_speed"] == "fastest"
    assert FORMAT_TABLE["CSV"]["size"] == "large"

    print("[OK] exercise_4 - CSV/JSON/Parquet/Arrow trade-offs applied")
    return decisions


# ---------------------------------------------------------------------------
# exercise 5
# ---------------------------------------------------------------------------

# Patterns taken from the source lesson's `.gitignore` example.
GITIGNORE_PATTERNS = [
    "*.bin",
    "*.safetensors",
    "*.pt",
    "*.onnx",
    "data/*.parquet",
    "data/*.csv",
    "models/",
]

# Files tracked with Git LFS in the source lesson.
GIT_LFS_TRACKED = ["*.bin", "*.safetensors"]

LARGE_FILES = [
    {"path": "models/checkpoint.pt", "size_mb": 240, "kind": "model weights", "shared": True, "must_reproduce": False},
    {"path": "data/raw/reviews.csv", "size_mb": 84, "kind": "downloaded dataset", "shared": False, "must_reproduce": False},
    {"path": "data/training_set.parquet", "size_mb": 1500, "kind": "curated dataset", "shared": True, "must_reproduce": True},
    {"path": "models/tokenizer.bin", "size_mb": 3, "kind": "model weights", "shared": True, "must_reproduce": False},
]


def large_file_policy(entry):
    """Decide between .gitignore, Git LFS and DVC.

    Rules from the source lesson:
      .gitignore -> low complexity, personal projects, data you can re-fetch
      Git LFS    -> medium complexity, teams sharing model weights via git
      DVC        -> high complexity, reproducible experiments, large datasets, teams
    """
    if entry["must_reproduce"]:
        return "DVC", "exact experiments must be reproducible on another machine"
    if entry["shared"] and entry["kind"] == "model weights":
        return "Git LFS", "team shares model weights through git"
    return ".gitignore", "data can be re-fetched, so it must not enter git"


def exercise_5():
    """Apply the large-file policy to model weights and datasets."""
    print("  {:<30} {:>9}  {:<12} {}".format("path", "size MB", "policy", "reason"))
    decisions = {}
    for entry in sorted(LARGE_FILES, key=lambda item: item["path"]):
        policy, reason = large_file_policy(entry)
        decisions[entry["path"]] = policy
        print("  {:<30} {:>9}  {:<12} {}".format(entry["path"], entry["size_mb"], policy, reason))

    print("  .gitignore patterns this course ships (sorted): {}".format(sorted(GITIGNORE_PATTERNS)))
    print("  Git LFS tracked patterns (sorted): {}".format(sorted(GIT_LFS_TRACKED)))
    print("  Git LFS quota note: free tier gives 1 GB; check your plan before pushing.")

    assert decisions["data/training_set.parquet"] == "DVC"
    assert decisions["models/checkpoint.pt"] == "Git LFS"
    assert decisions["models/tokenizer.bin"] == "Git LFS"
    assert decisions["data/raw/reviews.csv"] == ".gitignore"
    assert "*.pt" in GITIGNORE_PATTERNS and "models/" in GITIGNORE_PATTERNS
    assert "*.bin" in GIT_LFS_TRACKED and "*.safetensors" in GIT_LFS_TRACKED

    print("[OK] exercise_5 - large-file policy applied to weights and data")
    return decisions


# ---------------------------------------------------------------------------
# exercise 6
# ---------------------------------------------------------------------------

def exercise_6():
    """Print a dataset report for the generated CSV."""
    workdir = tempfile.mkdtemp(prefix="mod09_ex6_")
    try:
        path = _write_sample_csv(workdir)

        records = _load_records(path)
        splits = split_records(records, seed=SEED)

        csv_path = os.path.join(workdir, "reviews.csv")
        json_path = os.path.join(workdir, "reviews.json")
        with open(json_path, "w", encoding="utf-8") as handle:
            json.dump(records, handle, ensure_ascii=False)

        csv_bytes = os.path.getsize(csv_path)
        json_bytes = os.path.getsize(json_path)

        counts = {}
        for record in records:
            counts[record["label"]] = counts.get(record["label"], 0) + 1

        stream_info = _exercise_2_memory(path)

        print("  dataset report")
        print("  " + "-" * 46)
        print("  file            reviews.csv")
        print("  rows            {}".format(len(records)))
        print("  columns         {}".format(sorted(records[0].keys())))
        print("  label counts    {}".format(
            ", ".join("{}={}".format(k, counts[k]) for k in sorted(counts))
        ))
        print("  csv bytes       {}".format(csv_bytes))
        print("  json bytes      {}".format(json_bytes))
        print("  json/csv        {:.2f}x".format(json_bytes / csv_bytes))
        print("  split           train={} validation={} test={}".format(
            len(splits["train"]), len(splits["validation"]), len(splits["test"])
        ))
        print("  stream peak     {} KiB".format(stream_info["stream_peak_kib"]))
        print("  load peak       {} KiB".format(stream_info["load_peak_kib"]))
        print("  cache locations")
        print("    datasets      ~/.cache/huggingface/datasets/")
        print("    models        ~/.cache/huggingface/hub/")
        print("  note: Parquet and Arrow are the source's recommended storage format,")
        print("        but the standard library cannot write them, so no Parquet")
        print("        byte count is reported here.")

        assert len(records) == ROW_COUNT
        assert csv_bytes > 0 and json_bytes > 0
        assert csv_bytes < json_bytes, "JSON repeats the header keys on every row, so it is larger"
        assert len(splits["train"]) + len(splits["validation"]) + len(splits["test"]) == ROW_COUNT
        assert sum(counts.values()) == ROW_COUNT

        print("[OK] exercise_6 - dataset report printed")
        return {"rows": len(records), "csv_bytes": csv_bytes, "json_bytes": json_bytes}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _exercise_2_memory(path):
    """Re-measure the streaming/loading peaks for the report (see exercise 2)."""
    tracemalloc.start()
    for _record in _stream_records(path):
        pass
    _current, stream_peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    _loaded = _load_records(path)
    _current, load_peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "stream_peak_kib": _round_up_kib(stream_peak_bytes),
        "load_peak_kib": _round_up_kib(load_peak_bytes),
    }


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
    print("=" * 60)
    print("Module 09 - Data Management - offline lab")
    print("=" * 60)

    for index, (name, function) in enumerate(EXERCISES, start=1):
        print()
        print("--- {} / 6: {} ---".format(index, name))
        function()

    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
