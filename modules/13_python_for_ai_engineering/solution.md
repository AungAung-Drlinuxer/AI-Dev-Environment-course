# Module 13 — Python for AI Engineering — Solution

ဤဖိုင်ရှိ output အားလုံးသည် `modules/13_python_for_ai_engineering/lab.py` ကို **တကယ် run ၍** ရသည့် ရလဒ် ဖြစ်သည်။ Hand-computed တန်ဖိုး မဟုတ်ပါ။

Run command —

```bash
python3 modules/13_python_for_ai_engineering/lab.py
```

## Exercise 1 — `Record` dataclass နှင့် CSV loader

CSV ဖိုင် ရေးသည့်အခါ `newline=""` နှင့် `encoding="utf-8"` ကို ပေးရသည်။ CSV သည် field တိုင်းကို string အဖြစ် ပြန်ပေးသောကြောင့် `row_to_record` သည် `float()` နှင့် `int()` ဖြင့် ပြောင်းသည်။ `Record` သည် `frozen=True` ဖြစ်သောကြောင့် `__eq__` ကို ရရှိပြီး list နှစ်ခုကို တိုက်ရိုက် နှိုင်းယှဉ်နိုင်သည်။

```python
@dataclass(frozen=True)
class Record:
    features: tuple[float, ...]
    label: int


def load_records(path, label_field="label"):
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return []
    names = [key for key in rows[0] if key != label_field]
    return [row_to_record(row, names, label_field) for row in rows]
```

တကယ် run ၍ ရသည့် output —

```text
--- 1 / 6: exercise_1 ---
  file:        data.csv
  rows:        400
  columns:     ['label', 'x1', 'x2']
  features per row: 2
  labels (sorted):  [0, 1]
  label counts:     0=200 1=200
  roundtrip equals the original records: True
  first record: Record(features=(1.744, 55.114), label=0)
  type of one item: Record
[OK] exercise_1 — Record dataclass and CSV loader
```

`roundtrip equals the original records: True` သည် ဖိုင်မှ ပြန်ဖတ်သည့် record များ သည် မူရင်း နှင့် တန်ဖိုး တိုင်း တူညီသည်ကို အတည်ပြုသည်။ Label နှစ်ခုစလုံးသည် ၂၀၀ စီ ဖြစ်ရသည့် အကြောင်းရင်းမှာ `make_dataset` သည် label ကို `index % 2` ဖြင့် သတ်မှတ်သောကြောင့် ဖြစ်သည်။

## Exercise 2 — seed ပါသည့် train/test split

Seed တူညီပါက shuffle အစဉ် တူညီသည်၊ ထို့ကြောင့် split တူညီသည်။ Index စာရင်းကို shuffle လုပ်သောကြောင့် input list သည် မူရင်း အတိုင်း ကျန်သည်။

```python
def train_test_split(items, test_fraction=TEST_FRACTION, seed=SEED):
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
```

တကယ် run ၍ ရသည့် output —

```text
--- 2 / 6: exercise_2 ---
  input rows:  400
  test share:  0.2
  train rows:  320
  test rows:   80
  train + test == input: True
  records in both splits: 0
  same seed reproduces the same split: True
  seed 1 changes the first training record: True
  input list untouched (first feature still 1.744): True
[OK] exercise_2 — seeded train and test split
```

`records in both splits: 0` သည် train နှင့် test ထပ် နေခြင်း မရှိသည်ကို ပြသည်။ ထို အချက်သည် debugging နှင့် profiling သင်ခန်းစာတွင် ဖော်ပြသည့် test score လွန်ကဲ မြင့်မားမှုကို ကာကွယ်သည်။

## Exercise 3 — mini-batch generator

Argument check ကို အပြင်ဘက် function တွင် ထားသည်၊ ထို့ကြောင့် `batches(data, 0)` သည် ချက်ချင်း `ValueError` မြှောက်သည်။

```python
def batches(items, batch_size, drop_last=False):
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1, got {}".format(batch_size))
    return _batch_iter(iter(items), batch_size, drop_last)


def _batch_iter(iterator, batch_size, drop_last):
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch or (drop_last and len(batch) < batch_size):
            return
        yield batch
```

တကယ် run ၍ ရသည့် output —

```text
--- 3 / 6: exercise_3 ---
  items:            320
  batch size:       48
  batch sizes:      [48, 48, 48, 48, 48, 48, 32]
  number of batches: 7
  with drop_last:   [48, 48, 48, 48, 48, 48]
  batches over a generator expression: [3, 3, 1]
  one new generator per epoch:
    epoch 0: [48, 48, 48, 48, 48, 48, 32]
    epoch 1: [48, 48, 48, 48, 48, 48, 32]
[OK] exercise_3 — mini-batch generator
```

Epoch နှစ်ခု၏ စာရင်းသည် တူညီရသည့် အကြောင်းရင်းမှာ epoch တိုင်းအတွက် `batches()` ကို ထပ်ခေါ်၍ generator အသစ် ဖန်တီးသောကြောင့် ဖြစ်သည်။ Generator တစ်ခုတည်းကို ထပ် ဖြတ်ပါက ဒုတိယ epoch သည် အလွတ် ဖြစ်သည်။

## Exercise 4 — dot product၊ mean နှင့် standardizer

`zip(..., strict=True)` သည် vector အလျား မတူပါက `ValueError` မြှောက်သည်။ `make_standardizer` သည် column statistics ကို တစ်ကြိမ်တည်း တွက်ပြီး closure ဖြင့် ထိန်းထားသည်။

```python
def dot(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def make_standardizer(rows):
    means, stds = column_stats(rows)
    scales = [s if s > 0 else 1.0 for s in stds]

    def standardize(row):
        return [(value - m) / s for value, m, s in zip(row, means, scales, strict=True)]

    return standardize
```

တကယ် run ၍ ရသည့် output —

```text
--- 4 / 6: exercise_4 ---
  dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) = 32.0
  values: [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
  mean:   5.0
  std:    2.0  (population, divide by n)
  train rows standardized: [[-1.225, -1.225], [0.0, 0.0], [1.225, 1.225]]
  a test row (4.0, 700.0): [2.449, 2.449]
  means of the standardized training rows: [0.0, 0.0]
  dot with two different lengths raises ValueError: True
  a constant column keeps a scale of 1: [0.0, 2.449]
[OK] exercise_4 — dot product, mean and standardizer
```

`means of the standardized training rows: [0.0, 0.0]` သည် standardizer သည် မှန်ကန်စွာ အလုပ် လုပ်သည်ကို ပြသည်။ နောက်ဆုံး လိုင်းတွင် ပထမ column သည် ကိန်းသေ (5.0) ဖြစ်သဖြင့် scale 1.0 ရပြီး standardized တန်ဖိုးသည် 0.0 ဖြစ်သည်။

## Exercise 5 — error မတက်သည့် အမှား သုံးမျိုး

ထရိုက်ပုံ အပြည့်အစုံ —

```python
weights = [0.5, -1.2, 3.0]
alias = weights
alias[0] = 99.0          # weights ကိုပါ ပြောင်းသည်

independent = list(weights)
independent[1] = 0.0     # weights ကို မထိခိုက်


def add_bad(item, bucket=[]):
    bucket.append(item)
    return bucket


def add_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


def squares_factory():
    return (i * i for i in range(5))
```

တကယ် run ၍ ရသည့် output —

```text
--- 5 / 6: exercise_5 ---
  bug 1 - two names refer to one list
    weights after alias[0] = 99.0:  [99.0, -1.2, 3.0]
    alias is weights (the same object): True
    after independent = list(weights); independent[1] = 0.0:
      weights     [99.0, -1.2, 3.0]
      independent [99.0, 0.0, 3.0]
  bug 2 - a mutable default argument keeps its value between calls
    add_bad('a')  -> ['a']
    add_bad('b')  -> ['a', 'b']   (the old item is still there)
    add_good('a') -> ['a']
    add_good('b') -> ['b']   (a new list for each call)
  bug 3 - a generator is empty after one pass
    first  pass: [0, 1, 4, 9, 16]
    second pass: []   (the generator is used up)
    fixed - call the factory again for each epoch:
      epoch 0: [0, 1, 4, 9, 16]
      epoch 1: [0, 1, 4, 9, 16]
[OK] exercise_5 — shared list, mutable default and used-up generator
```

အမှား သုံးမျိုးစလုံးသည် **error မတက်ဘဲ** ရလဒ် မှား ကို ပေးသည်။ ဤ ရလဒ်များကို ဖတ်ရှုသူ တိုင်း မြင်နိုင်ရန် print လုပ်ထားသည်။ `add_bad("c") == ["a", "b", "c"]` ဖြစ်သည်ကို assert ဖြင့် လည်း အတည်ပြုထားသည် — mutable default သည် function object အပေါ် တွင် တကယ် စုပုံနေသည်။

## Exercise 6 — အချိန် နှင့် memory အစီရင်ခံစာ

အချိန်ကို တိုင်းတာ သော်လည်း wall-clock ဂဏန်းကို **မပြပါ** — ထို ဂဏန်းသည် machine နှင့် run အလိုက် ပြောင်းသည့်အတွက် output ကို မတည်ငြိမ်စေသည်။ ထို အစား repeat အရေအတွက် ကို print သည်။ Memory ဂဏန်းကို bucket အထိ round up လုပ်သည်။

```python
def best_time(fn, *args, repeat=5):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        fn(*args)
        times.append(time.perf_counter() - start)
    return min(times)


def bucket_kib(value_bytes, granularity_kib=64):
    step = granularity_kib * KIB
    return ((value_bytes + step - 1) // step) * step // KIB
```

တကယ် run ၍ ရသည့် output —

```text
--- 6 / 6: exercise_6 ---
  speed: dot product of 200,000 floats, best of 5
    variants measured: ['index loop', 'map + mul', 'zip generator']
    repeats per variant: 5
    all three variants agree: True
    seconds are not printed - a wall-clock number is not stable
    every timing was positive: True
  memory: peak bytes to sum 100,000 squares
    list       (rounded up to 1 MiB): 4096 KiB
    generator  (rounded up to 64 KiB): 64 KiB
    the generator peak is smaller: True
    the generator holds one item at a time; the list holds every item
[OK] exercise_6 — speed and memory measurement report
```

Variant သုံးမျိုးသည် သင်္ချာ အတူတူ လုပ်သည်၊ ထို့ကြောင့် `all three variants agree: True` ဖြစ်ရသည်။ Memory တွင် list သည် ၄ MiB ဖြစ်ပြီး generator သည် 64 KiB (အတိုင်းအတာ အနည်းဆုံး bucket) ဖြစ်သည် — Figure 3 တွင် ဖော်ပြသည့် ပုံစံ အတိုင်း ဖြစ်သည်။

## Run အပြည့်အစုံ

```text
==============================================================
Module 13 - Python for AI Engineering - offline lab
==============================================================

--- 1 / 6: exercise_1 ---
  ...
--- 6 / 6: exercise_6 ---
  ...

[PASS] All 6/6 exercises passed successfully.
```

Exit code သည် `0` ဖြစ်သည်။ Output သည် run တိုင်းတွင် byte အလိုက် တူညီသည် (run သုံးကြိမ် နှိုင်းယှဉ်စစ်ပြီး)။
