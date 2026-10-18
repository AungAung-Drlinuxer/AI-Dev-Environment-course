# Module 09 — Data Management

> Data သည် လောင်စာ ဖြစ်သည်။ ထို data ကို မည်သို့ စီမံသည်က project တစ်ခု၏ အမြန်နှုန်းကို ဆုံးဖြတ်သည်။

**Type:** Build · **Language:** Python · **Time:** ~45 min · **Source lesson:** `phases/00-setup-and-tooling/09-data-management`

## ရည်ရွယ်ချက်

ဤ module ပြီးဆုံးသည့်အခါ ဖတ်ရှုသူသည် အောက်ပါ အရာများကို လုပ်နိုင်ရမည် —

- Hugging Face `datasets` library ဖြင့် dataset များကို **load**၊ **stream** နှင့် **cache** လုပ်ခြင်း
- **CSV**၊ **JSON**၊ **Parquet** နှင့် **Arrow** format များအကြား ပြောင်းလဲခြင်း၊ ထို format များ၏ အားသာချက်/အားနည်းချက်ကို ရှင်းပြနိုင်ခြင်း
- seed သတ်မှတ်၍ **reproducible** train/validation/test split များ ဖန်တီးခြင်း
- ဖိုင်ကြီးများ (model weight၊ dataset) ကို `.gitignore`၊ **Git LFS** သို့မဟုတ် **DVC** ဖြင့် စီမံခြင်း

## လိုအပ်ချက် (Prerequisites)

- Module 01 (Dev Environment) — Python 3.11+ နှင့် terminal အခြေခံ အသုံးပြုနိုင်ခြင်း
- Python အခြေခံ — variable၊ function၊ list၊ dict၊ `for` loop၊ `with` statement
- ဤ module ၏ lab ကို run ရန် **network မလိုပါ**၊ **package တစ်ခုမျှ install လုပ်ရန် မလိုပါ**။ Lab သည် Python standard library သာ သုံးသည်။
- Lab ရှိ `csv`၊ `json`၊ `tracemalloc`၊ `random.Random(seed)` တို့ကို မဖတ်ဖူးသေးပါက အဆင်ပါသည် — `solution.md` တွင် တစ်လိုင်းချင်း ရှင်းပြထားသည်။

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. Step 1: Install the datasets library
2. Step 2: Load a dataset
3. Step 3: Stream large datasets
4. Step 4: Dataset formats
5. Step 5: Data splits
6. Step 6: Download and cache models
7. Step 7: Handle large files
8. Step 8: Storage patterns
9. Datasets Used in This Course

## Exercise စာရင်း

| # | Exercise | တစ်လိုင်း အနှစ်ချုပ် |
|---|---|---|
| 1 | `load_csv_records` | ကိုယ်တိုင်ရေးသော CSV ဖိုင်ကို record (dict) စာရင်း အဖြစ် ဖတ်ပြီး column၊ row နှင့် label အရေအတွက် ကို စစ်ခြင်း |
| 2 | `stream_vs_load` | generator ဖြင့် တစ်လိုင်းချင်း ဖတ်ခြင်း နှင့် အပြည့်ဖတ်ခြင်း၏ peak memory ကို `tracemalloc` ဖြင့် နှိုင်းယှဉ်ခြင်း |
| 3 | `split_dataset` | seed သတ်မှတ်ထားသည့် `random.Random(seed)` ဖြင့် 70/15/15 train/validation/test split ခွဲပြီး ပြန်လုပ်နိုင်မှုကို စစ်ခြင်း |
| 4 | `format_tradeoffs` | CSV / JSON / Parquet / Arrow ၏ trade-off ကို data အဖြစ် သိမ်းပြီး scenario အလိုက် format ရွေးချယ်ခြင်း |
| 5 | `large_file_policy` | checkpoint၊ model weight နှင့် dataset ဖိုင်များအတွက် `.gitignore` / Git LFS / DVC ကို ဆုံးဖြတ်ခြင်း |
| 6 | `dataset_report` | row၊ column၊ label၊ ဖိုင်အရွယ်အစား၊ split နှင့် cache တည်နေရာ ပါဝင်သည့် dataset အစီရင်ခံစာ ထုတ်ခြင်း |

## ဖိုင်စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise နှင့် ဖိုင် စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — အခြေခံ သဘောတရား၊ format နှိုင်းယှဉ်ချက်၊ command နှင့် လုပ်ဆောင်ချက်၊ သတိထားရန် အချက်၊ ကိုယ်တိုင်စစ်မေးခွန်း |
| `exercise.md` | လက်တွေ့ လုပ်ရမည့် exercise ၆ ခု (လိုအပ်ချက်၊ အဆင့်၊ အောင်မြင်မှု စစ်နည်း) |
| `solution.md` | exercise ၆ ခု၏ အဖြေ — တကယ် run ၍ ရသည့် output နှင့်တကွ |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## Lab ကို run စစ်ခြင်း

```bash
python3 modules/09_data_management/lab.py
```

ဤ command သည် exercise ၆ ခုကို အစဉ်လိုက် run ပြီး exercise တိုင်း၏ ရလဒ်ကို လူဖတ်နိုင်သော လိုင်းများဖြင့် print သည်။
အောင်မြင်ပါက နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ကို ပြပြီး exit code `0` ဖြင့် ပြီးဆုံးသည်။

Lab သည် data ကို မိမိကိုယ်တိုင် ရေးသည် — temporary directory တစ်ခုထဲသို့ CSV ဖိုင် တစ်ခု ရေးပြီး၊ ဖတ်ပြီး၊ ပြီးဆုံးသည့်အခါ ဖျက်ပစ်သည်။
ထို့ကြောင့် network မရှိသည့် စာသင်ခန်း သို့မဟုတ် offline machine တွင် လည်း run နိုင်သည်။

## Cautions

- command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
- Model weight (`*.bin`၊ `*.safetensors`၊ `*.pt`၊ `*.onnx`) နှင့် dataset ဖိုင်ကြီးများကို git ထဲ မထည့်ရ။
- Cache ဖိုင်များသည် disk နေရာ အများအပြား ယူနိုင်သည် — မလိုအပ်တော့သော cache ကို ရံဖန်ရံခါ စစ်ပါ။
