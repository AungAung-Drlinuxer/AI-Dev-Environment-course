# Module 09 — Data Management — Solution

ဤဖိုင်ရှိ အဖြေ အားလုံးသည် `modules/09_data_management/lab.py` ကို **တကယ် run** ၍ ရသည့် output ဖြစ်သည်။
Hand-computed ကိန်းဂဏန်း တစ်ခုမျှ မပါပါ။ Run command နှင့် ရလဒ် အပြည့်အစုံမှာ နောက်ဆုံးတွင် ဖော်ပြထားသည်။

Dataset အားလုံးသည် **script ကိုယ်တိုင် temporary directory ထဲ ရေးသည့် CSV ဖိုင်** ဖြစ်သည်။ Network မှ dataset မရယူပါ၊
`datasets`၊ `numpy`၊ `pandas` တို့ကို မသုံးပါ — Python standard library သာ ဖြစ်သည်။

---

## Exercise 1 — CSV ဖိုင်ကို record စာရင်း အဖြစ် ဖတ်ခြင်း

**အနှစ်ချုပ်။** CSV ဖိုင် တစ်ခုကို ကိုယ်တိုင် ရေးပြီး `csv.DictReader` ဖြင့် `dict` စာရင်း အဖြစ် ပြန်ဖတ်သည်။
`csv.DictReader` သည် ပထမလိုင်းကို header အဖြစ် ယူပြီး လိုင်းတိုင်းကို `dict` တစ်ခုအဖြစ် ပြန်ပေးသည်။ `dict(row)` သည် ထို row ကို ရိုးရိုး `dict` အဖြစ် ပြောင်းသည်။

```python
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


def _load_records(path):
    """Read every record into a list. This is the loading (eager) reader."""
    with open(path, newline="", encoding="utf-8") as handle:
        return [dict(row) for row in csv.DictReader(handle)]
```

`text` column တွင် `{:05d}` ကို သုံးသည်။ ထို့ကြောင့် နံပါတ်တိုင်းသည် စာလုံး ၅ လုံး ရှိပြီး row တိုင်း၏ အရွယ်အစား ကိန်းသေ ဖြစ်သည်။
ဤအချက်သည် Exercise 2 ၏ memory တိုင်းတာမှုကို ရှင်းလင်းစေသည်။

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 1 / 6: exercise_1 ---
  file:       reviews.csv
  rows:       20000
  columns:    ['id', 'label', 'text']
  labels:     ['negative', 'positive']
  label count:
    negative  10000
    positive  10000
  first row:  id=0 label=positive
  last row:   id=19999 label=negative
  type of first record: dict
[OK] exercise_1 - read a CSV file as a list of records
```

Row ၂၀၀၀၀၊ column သုံးခု၊ label နှစ်မျိုး စီ ၁၀၀၀၀ စီ ဖြစ်သည်။ ပထမ record ၏ `id` သည် `0`၊ နောက်ဆုံး record ၏ `id` သည် `19999` ဖြစ်သည်။
`id` သည် CSV မှ ပြန်လာသည့်အခါ **string** ဖြစ်သည် — CSV တွင် type အချက်အလက် မပါသောကြောင့် ဖြစ်သည်။ ထို အချက်ကို `assert records[0]["id"] == "0"` ဖြင့် စစ်ထားသည်။

---

## Exercise 2 — Streaming နှင့် loading ၏ peak memory ကို နှိုင်းယှဉ်ခြင်း

**အနှစ်ချုပ်။** Generator သည် row တစ်ခုချင်း ဖတ်ပြီး ဖတ်ပြီးသား row ကို ချက်ချင်း လွှတ်သည်။ ထို့ကြောင့် peak memory သည် row အရေအတွက်နှင့် မသက်ဆိုင်ပါ။
List `[… for row in …]` သည် row အားလုံးကို သိမ်းသည်။ ထို့ကြောင့် peak memory သည် row အရေအတွက်နှင့် အချိုးကျ တိုးသည်။

```python
def _stream_records(path):
    """Yield one record at a time. This is the streaming (lazy) reader."""
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            yield dict(row)


def _round_up_kib(value_bytes, granularity_kib=64):
    """Round a byte count up to a coarse, stable KiB bucket.

    `tracemalloc` peaks are allocator-dependent: the raw figure can move by a
    few kilobytes between runs and between Python builds. Rounding up to a
    64 KiB bucket removes that noise, so the number printed here is
    reproducible instead of unstable.
    """
    step = granularity_kib * KIB
    return ((value_bytes + step - 1) // step) * step // KIB
```

**64 KiB bucket အထိ round up လုပ်ရသည့် အကြောင်းရင်း။** `tracemalloc` သည် Python interpreter ၏ allocation ကို မှတ်သည်။
Raw peak သည် run တိုင်းတွင် KB အနည်းငယ် လှုပ်ရှားနိုင်ပြီး interpreter version အလိုက် လည်း ပြောင်းနိုင်သည်။
Bucket ဖြင့် ပြပါက print သည့် ကိန်းဂဏန်း သုံးခုသည် run တိုင်းတွင် တူညီသည် (ငါးကြိမ် run ၍ စစ်ထားသည်)။

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 2 / 6: exercise_2 ---
  rows read by streaming: 20000
  rows held by loading:   20000
  stream peak (rounded up to 64 KiB): 192 KiB
  load   peak (rounded up to 64 KiB): 7744 KiB
  load peak / stream peak: about 40x
  streaming keeps memory constant; loading grows with row count.
[OK] exercise_2 - streaming and loading peak memory compared
```

နည်းလမ်း နှစ်မျိုးစလုံးသည် row ၂၀၀၀၀ ကို ဖတ်သည်။ Stream peak သည် **192 KiB**၊ load peak သည် **7744 KiB** ဖြစ်သည်။
အချိုးသည် **၄၀ ဆ** ခန့် ဖြစ်သည်။ Row အရေအတွက် တူညီသော်လည်း peak memory သည် ဆယ်ဆချီ ကွာသည် —
streaming သည် row ကို ဖတ်ပြီးသည့်နောက် လွှတ်သည့်အတွက် ဖြစ်သည်။

---

## Exercise 3 — Seed သတ်မှတ်ပြီး 70/15/15 split ခွဲခြင်း

**အနှစ်ချုပ်။** Index စာရင်းတစ်ခု တည်ဆောက်ပြီး `random.Random(seed).shuffle(indices)` ဖြင့် ရောကာ အပိုင်း သုံးပိုင်း ဖြတ်သည်။
`random.Random(seed)` သည် မိမိကိုယ်ပိုင် state ရှိသည့် generator ဖြစ်သည်။ ထို့ကြောင့် module-level `random` state ကို မထိခိုက်ဘဲ run တိုင်းတွင် တူညီသည့် အစဉ် ရသည်။

```python
def split_records(records, seed=SEED, train_ratio=0.70, val_ratio=0.15):
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
```

Row ၂၀၀၀၀ ဖြစ်သည့်အတွက် ၇၀% = 14000၊ ၁၅% = 3000၊ ၁၅% = 3000 ဖြစ်ပြီး စုစုပေါင်း အတိအကျ ကိုက်သည်။

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 3 / 6: exercise_3 ---
  train        14000 rows (70.0%)  first id=5117
  validation    3000 rows (15.0%)  first id=19075
  test          3000 rows (15.0%)  first id=5368
  split names (sorted): ['test', 'train', 'validation']
  same seed reproduces the same first record: True
  seed 1234 changes the first train id: 5117 -> 381
[OK] exercise_3 - 70/15/15 split with a fixed seed
```

Seed `42` ဖြင့် train ၏ ပထမ `id` သည် `5117` ဖြစ်သည်။ ထို seed ဖြင့် ဒုတိယအကြိမ် run ပါက ထပ် `5117` ရသည် (reproducible)။
Seed `1234` ဖြင့် ပြောင်းပါက `381` ဖြစ်သွားသည် — seed က ရောသည့် အစဉ်ကို ဆုံးဖြတ်ကြောင်း ပြသည်။
Split အမည် စာရင်းကို `sorted()` ဖြင့် print ထားသည် (set ကို တိုက်ရိုက် မပြပါ။ အကြောင်းရင်းမှာ set ၏ အစဉ်သည် run တိုင်းတွင် တူညီကြောင်း အာမမခံနိုင်သည့်အတွက် ဖြစ်သည်)။

---

## Exercise 4 — CSV / JSON / Parquet / Arrow ၏ trade-off ကို ရွေးချယ်ခြင်း

**အနှစ်ချုပ်။** Source lesson ၏ ဇယားကို code ထဲတွင် dictionary အဖြစ် သိမ်းပြီး scenario အလိုက် ရွေးသည့် function ကို ရေးသည်။
ဇယားကို code အဖြစ် သိမ်းသည့်အခါ ထို အချက်အလက်အပေါ် `assert` ဖြင့် စစ်နိုင်သည်၊ print လည်း လုပ်နိုင်သည်။

```python
FORMAT_TABLE = {
    "CSV": {"size": "large", "read_speed": "slow", "best_for": "human readability, spreadsheets"},
    "JSON": {"size": "large", "read_speed": "slow", "best_for": "APIs, nested data"},
    "Parquet": {"size": "small", "read_speed": "fast", "best_for": "analytics, columnar queries"},
    "Arrow": {"size": "small", "read_speed": "fastest", "best_for": "in-memory processing (used internally by the datasets library)"},
}


def choose_format(human_readable, nested, columnar_analytics, in_memory):
    if in_memory:
        return "Arrow"
    if columnar_analytics:
        return "Parquet"
    if nested:
        return "JSON"
    if human_readable:
        return "CSV"
    return "Parquet"
```

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 4 / 6: exercise_4 ---
  format table (from the source lesson):
  format   size   read       best for
  Arrow    small  fastest    in-memory processing (used internally by the datasets library)
  CSV      large  slow       human readability, spreadsheets
  JSON     large  slow       APIs, nested data
  Parquet  small  fast       analytics, columnar queries
  scenario decisions:
    analyst runs column-level aggregate queries      -> Parquet
    training loop reads batches in memory            -> Arrow
    reviewer opens the file in a spreadsheet         -> CSV
    service returns nested records over an API       -> JSON
  rule: Parquet on disk, Arrow in memory, CSV/JSON for interchange.
[OK] exercise_4 - CSV/JSON/Parquet/Arrow trade-offs applied
```

ဇယားသည် source lesson ၏ ကိန်းဂဏန်းအတိုင်း ဖြစ်သည် — CSV နှင့် JSON သည် `large`/`slow`၊ Parquet သည် `small`/`fast`၊ Arrow သည် `small`/`fastest` ဖြစ်သည်။
စည်းမျဉ်းမှာ — **disk ပေါ်တွင် Parquet၊ memory ထဲတွင် Arrow၊ interchange အတွက် CSV/JSON** ဖြစ်သည်။

---

## Exercise 5 — ဖိုင်ကြီးများအတွက် policy ဆုံးဖြတ်ခြင်း

**အနှစ်ချုပ်။** `.gitignore`၊ Git LFS နှင့် DVC တို့၏ ရွေးချယ်မှုကို အချက် နှစ်ချက်ဖြင့် ဆုံးဖြတ်သည် —
**data ကို အတိအကျ ပြန်လုပ်ရန် လို/မလို** နှင့် **အဖွဲ့အစည်း အတူတူ သုံးသည့် model weight ဟုတ်/မဟုတ်**။

```python
GITIGNORE_PATTERNS = [
    "*.bin", "*.safetensors", "*.pt", "*.onnx",
    "data/*.parquet", "data/*.csv", "models/",
]

GIT_LFS_TRACKED = ["*.bin", "*.safetensors"]


def large_file_policy(entry):
    if entry["must_reproduce"]:
        return "DVC", "exact experiments must be reproducible on another machine"
    if entry["shared"] and entry["kind"] == "model weights":
        return "Git LFS", "team shares model weights through git"
    return ".gitignore", "data can be re-fetched, so it must not enter git"
```

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 5 / 6: exercise_5 ---
  path                             size MB  policy       reason
  data/raw/reviews.csv                  84  .gitignore   data can be re-fetched, so it must not enter git
  data/training_set.parquet           1500  DVC          exact experiments must be reproducible on another machine
  models/checkpoint.pt                 240  Git LFS      team shares model weights through git
  models/tokenizer.bin                   3  Git LFS      team shares model weights through git
  .gitignore patterns this course ships (sorted): ['*.bin', '*.onnx', '*.pt', '*.safetensors', 'data/*.csv', 'data/*.parquet', 'models/']
  Git LFS tracked patterns (sorted): ['*.bin', '*.safetensors']
  Git LFS quota note: free tier gives 1 GB; check your plan before pushing.
[OK] exercise_5 - large-file policy applied to weights and data
```

ဖိုင် လေးခုသည် policy သုံးမျိုးကို ပြသည် —

- ပြန်ရယူနိုင်သည့် raw dataset (84 MB) → **`.gitignore`**။ ဖိုင် ကို git ထဲ မထည့်ဘဲ download script ဖြင့် ပြန်ယူသည်။
- အတိအကျ ပြန်လုပ်ရန် လိုသည့် curated data (1500 MB) → **DVC**။ `.dvc` ဖိုင် (hash ပါသည်) ကို git ထဲ ထည့်ပြီး data အစစ်ကို remote storage ထဲ ထားသည်။
- အဖွဲ့အစည်း အတူတူ သုံးသည့် model weight (240 MB နှင့် 3 MB) → **Git LFS**။

Pattern စာရင်း နှစ်ခုကို `sorted()` ဖြင့် print ထားသည်။ Set ကို တိုက်ရိုက် print ပါက အစဉ် မတည်ငြိမ်သည့်အတွက် ဖြစ်သည်။
Git LFS ၏ `1 GB free` သည် source lesson တွင် ပါသည့် ကိန်းဂဏန်း ဖြစ်သည်။ Quota မူဝါဒသည် **version အလိုက် ပြန်စစ်ရန် လိုသည်**။

---

## Exercise 6 — Dataset အစီရင်ခံစာ ထုတ်ခြင်း

**အနှစ်ချုပ်။** Row၊ column၊ label အရေအတွက်၊ ဖိုင်အရွယ်အစား၊ split နှင့် cache တည်နေရာကို တစ်နေရာတည်းတွင် ပြသည်။
ဖိုင်အရွယ်အစား နှစ်ခုကို `os.path.getsize` ဖြင့် **တကယ် တိုင်း** ထားသည်။

```python
        csv_bytes = os.path.getsize(csv_path)
        json_bytes = os.path.getsize(json_path)
        ...
        print("  csv bytes       {}".format(csv_bytes))
        print("  json bytes      {}".format(json_bytes))
        print("  json/csv        {:.2f}x".format(json_bytes / csv_bytes))
```

**ရလဒ် (တကယ် run ထားသည်)။**

```
--- 6 / 6: exercise_6 ---
  dataset report
  ----------------------------------------------
  file            reviews.csv
  rows            20000
  columns         ['id', 'label', 'text']
  label counts    negative=10000, positive=10000
  csv bytes       1508905
  json bytes      2168890
  json/csv        1.44x
  split           train=14000 validation=3000 test=3000
  stream peak     192 KiB
  load peak       7744 KiB
  cache locations
    datasets      ~/.cache/huggingface/datasets/
    models        ~/.cache/huggingface/hub/
  note: Parquet and Arrow are the source's recommended storage format,
        but the standard library cannot write them, so no Parquet
        byte count is reported here.
[OK] exercise_6 - dataset report printed
```

JSON ဖိုင်သည် CSV ဖိုင် ထက် **၁.၄၄ ဆ** ကြီးသည်။ အကြောင်းရင်းမှာ JSON သည် key အမည် (`id`၊ `text`၊ `label`) ကို **row တိုင်းတွင် ထပ်ရေး** သည့်အတွက် ဖြစ်သည်။
CSV သည် header ကို တစ်ကြိမ်သာ ရေးသည်။ ဤ အချက်သည် source lesson ၏ ဇယားတွင် CSV နှင့် JSON နှစ်ခုစလုံး `large` ဖြစ်သည့် အကြောင်းရင်းကို လက်တွေ့ ပြသည်။

**Parquet နှင့် Arrow ၏ byte အရေအတွက်ကို ဖော်ပြခြင်း မပြုပါ။** Standard library တွင် Parquet သို့မဟုတ် Arrow ရေးသည့် module မရှိပါ။
ထို့ကြောင့် ထို format နှစ်မျိုး၏ ဖိုင်အရွယ်အစားကို ဤ lab တွင် **တိုင်းတာနိုင်ခြင်း မရှိပါ**။ မတိုင်းတာရသေးသည့် ကိန်းဂဏန်းကို တီးလုပ်ခြင်း မပြုဘဲ
ထို အချက်ကို အစီရင်ခံစာ ကိုယ်တိုင် မှတ်ထားသည်။ Parquet ၏ ဖိုင်အရွယ်အစား အကျိုးကျေးဇူးကို ကိုယ်တိုင် တိုင်းလိုပါက
`datasets` library install လုပ်ပြီး `dataset.to_parquet(...)` ကို `os.path.getsize` ဖြင့် နှိုင်းယှဉ်ရသည် (network လိုသည်)။

---

## Run အပြည့်အစုံ

```bash
python3 modules/09_data_management/lab.py
```

Exit code သည် `0` ဖြစ်သည်။ နောက်ဆုံးလိုင်းများမှာ —

```
--- 6 / 6: exercise_6 ---
  ...
[OK] exercise_6 - dataset report printed

[PASS] All 6/6 exercises passed successfully.
```

`[OK]` လိုင်း ၆ လိုင်း နှင့် `[PASS]` လိုင်း တစ်လိုင်း ရသည်။
