# Module 09 — Data Management — Exercise

ဤ exercise ၆ ခုကို `modules/09_data_management/lab.py` တွင် `def exercise_1()` … `def exercise_6()` အဖြစ် implement လုပ်ထားသည်။
Exercise တိုင်းသည် **Python standard library သာ** သုံးရမည် — `datasets`၊ `numpy`၊ `pandas` နှင့် network ကို မသုံးရ။
Data ကို script ကိုယ်တိုင် temporary directory ထဲ ရေးပြီး ဖတ်ရမည်။ **Download လုပ်ရန် dataset တစ်ခုမျှ မရှိရ။**

## Exercise 1 — CSV ဖိုင်ကို record စာရင်း အဖြစ် ဖတ်ခြင်း

**လိုအပ်ချက်။** Script ကိုယ်တိုင် CSV ဖိုင် တစ်ခုကို temporary directory ထဲ ရေးပြီး၊ ထို ဖိုင်ကို record (dict) စာရင်း အဖြစ် ပြန်ဖတ်ရမည်။
ဖိုင်တွင် column သုံးခု — `id`၊ `text`၊ `label` — ပါရမည်။ Row အရေအတွက်သည် အနည်းဆုံး ၁၀၀၀ ဖြစ်ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. `tempfile.mkdtemp()` ဖြင့် temporary directory တစ်ခု ဖန်တီးပါ။
2. `csv.DictWriter` ဖြင့် `reviews.csv` ကို ရေးပါ။ `label` ကို row အစဉ်အလိုက် `positive` / `negative` အဖြစ် သတ်မှတ်ပါ။
3. `csv.DictReader` ဖြင့် ထို ဖိုင်ကို ပြန်ဖတ်ပြီး `dict` စာရင်း တစ်ခု တည်ဆောက်ပါ။
4. Row အရေအတွက်၊ column အမည် (sorted)၊ label အရေအတွက် နှင့် ပထမ/နောက်ဆုံး record ၏ `id` ကို print ပါ။
5. `shutil.rmtree(..., ignore_errors=True)` ကို `finally` block ထဲ ထည့်ပါ။

**အောင်မြင်မှု စစ်နည်း။** `len(records)` သည် ရေးလိုက်သည့် row အရေအတွက်နှင့် တူရမည်။ `sorted(records[0])` သည် `['id', 'label', 'text']` ဖြစ်ရမည်။
ပထမ record ၏ `id` သည် `0`၊ နောက်ဆုံး record ၏ `id` သည် row အရေအတွက် အနုတ် ၁ ဖြစ်ရမည်။ Label နှစ်မျိုး၏ အရေအတွက် စုစုပေါင်းသည် row စုစုပေါင်းနှင့် တူရမည်။

## Exercise 2 — Streaming နှင့် loading ၏ peak memory ကို နှိုင်းယှဉ်ခြင်း

**လိုအပ်ချက်။** Exercise 1 ၏ CSV ဖိုင်ကို နည်းလမ်း နှစ်မျိုးဖြင့် ဖတ်ပြီး peak memory ကို `tracemalloc` ဖြင့် တိုင်းရမည်။

- **Streaming** — generator တစ်ခုဖြင့် row တစ်ခုချင်း ဖတ်ပြီး ရေတွက်သည်။ စာရင်း တစ်ခုလုံးကို မသိမ်းပါ။
- **Loading** — row အားလုံးကို `dict` စာရင်း အဖြစ် memory ထဲ သိမ်းသည်။

**လုပ်ရမည့် အဆင့်။**

1. `tracemalloc.start()` ဖြင့် စပါ။ ထို့နောက် လိုချင်သည့် လုပ်ငန်းကို လုပ်ပါ။ `tracemalloc.get_traced_memory()` သည် `(current, peak)` tuple ကို ပြန်သည်။ `tracemalloc.stop()` ဖြင့် ရပ်ပါ။
2. Peak ကိန်းဂဏန်း နှစ်ခုကို **64 KiB bucket အထိ round up** လုပ်ပါ။ `tracemalloc` ၏ raw peak သည် allocator အလိုက် run တိုင်းတွင် KB အနည်းငယ် လှုပ်ရှားနိုင်သည့်အတွက် bucket ဖြင့် ပြပါ။
3. `load peak / stream peak` အချိုးကို ကိန်းပြည့်အဖြစ် print ပါ။
4. Stream peak သည် load peak ထက် **သေးရမည်**၊ အချိုးသည် **၁၀ ထက် မငယ်ရ** ဟု `assert` ဖြင့် စစ်ပါ။

**အောင်မြင်မှု စစ်နည်း။** နည်းလမ်း နှစ်မျိုး၏ row အရေအတွက် တူရမည်။ အချိုးသည် ၁၀ ထက် ကြီးရမည်။
Script ကို ငါးကြိမ် run ပါက print သည့် ကိန်းဂဏန်း သုံးခု (stream peak၊ load peak၊ အချိုး) သည် တူညီရမည်။

## Exercise 3 — Seed သတ်မှတ်ပြီး 70/15/15 split ခွဲခြင်း

**လိုအပ်ချက်။** Exercise 1 ၏ record များကို train ၇၀%၊ validation ၁၅%၊ test ၁၅% အဖြစ် ခွဲရမည်။ Seed ကို `random.Random(seed)` ဖြင့်သာ သုံးရမည် — module-level `random` function များကို မသုံးရ။

**လုပ်ရမည့် အဆင့်။**

1. `list(range(len(records)))` ဖြင့် index စာရင်း တည်ဆောက်ပါ။
2. `random.Random(SEED).shuffle(indices)` ဖြင့် ထို စာရင်းကို ရောပါ။ Seed သည် ကိန်းသေ (`42`) ဖြစ်ရမည်။
3. `indices` ကို အပိုင်း သုံးပိုင်း ဖြတ်ပါ — ပထမ ၇၀% train၊ နောက် ၁၅% validation၊ ကျန် ၁၅% test။
4. Split တိုင်း၏ row အရေအတွက်၊ ရာခိုင်နှုန်း နှင့် ပထမ record ၏ `id` ကို print ပါ။
5. Seed တူညီဖြင့် ဒုတိယအကြိမ် ခွဲပြီး ပထမ `id` များ တူမတူ စစ်ပါ။ Seed အခြားတစ်ခု (`1234`) ဖြင့် လည်း ခွဲပြီး ပြောင်းသွားကြောင်း ပြပါ။

**အောင်မြင်မှု စစ်နည်း။** Split သုံးခု၏ row စုစုပေါင်းသည် မူရင်း row စုစုပေါင်းနှင့် တူရမည်။
Row ၂၀၀၀၀ ဖြစ်ပါက အရေအတွက်သည် 14000 / 3000 / 3000 ဖြစ်ရမည်။ Seed တူညီပါက ပထမ `id` များ တူရမည်။ Seed မတူပါက မတူရမည်။

## Exercise 4 — CSV / JSON / Parquet / Arrow ၏ trade-off ကို ရွေးချယ်ခြင်း

**လိုအပ်ချက်။** Format လေးမျိုး၏ `size`၊ `read speed` နှင့် `best for` ကို **data အဖြစ်** (dictionary) သိမ်းပြီး၊ scenario တစ်ခုစီအတွက် format ကို ရွေးသည့် function တစ်ခု ရေးရမည်။

**လုပ်ရမည့် အဆင့်။**

1. Source lesson ၏ ဇယားအတိုင်း format တိုင်း၏ `size`၊ `read_speed`၊ `best_for` ကို dictionary ထဲ ထည့်ပါ။
2. Format ဇယားကို အမည် sorted အစဉ်ဖြင့် print ပါ။
3. `choose_format(human_readable, nested, columnar_analytics, in_memory)` function တစ်ခု ရေးပါ — ဦးစားပေး အစဉ်မှာ `in_memory` → Arrow၊ `columnar_analytics` → Parquet၊ `nested` → JSON၊ `human_readable` → CSV ဖြစ်သည်။
4. Scenario လေးခုအတွက် ရလဒ်ကို print ပြပါ — analytics query၊ in-memory training၊ spreadsheet ဖတ်ခြင်း၊ API ၏ nested record။
5. Scenario တိုင်း၏ ရလဒ်ကို `assert` ဖြင့် စစ်ပါ။

**အောင်မြင်မှု စစ်နည်း။** Analytics scenario သည် `Parquet`၊ in-memory scenario သည် `Arrow`၊ spreadsheet သည် `CSV`၊ API သည် `JSON` ကို ပြန်ရမည်။
Format ဇယားတွင် `Arrow` ၏ `read_speed` သည် `fastest`၊ `CSV` ၏ `size` သည် `large` ဖြစ်ရမည်။

## Exercise 5 — ဖိုင်ကြီးများအတွက် policy ဆုံးဖြတ်ခြင်း

**လိုအပ်ချက်။** ဖိုင် လေးခု၏ အချက်အလက် (path၊ size၊ အမျိုးအစား၊ အဖွဲ့အစည်း နှင့် အတူတူ သုံးမသလား၊ အတိအကျ ပြန်လုပ်ရန် လိုသလား) ကို ပေးပြီး `.gitignore` / Git LFS / DVC ကို ဆုံးဖြတ်သည့် function တစ်ခု ရေးရမည်။

**လုပ်ရမည့် အဆင့်။**

1. Source lesson ၏ `.gitignore` pattern စာရင်းကို constant တစ်ခုအဖြစ် ထားပါ။
2. Git LFS track လုပ်သည့် pattern စာရင်းကို သီးခြား constant အဖြစ် ထားပါ။
3. ဖိုင် လေးခု၏ အချက်အလက်ကို `dict` စာရင်းအဖြစ် သိမ်းပါ — checkpoint (240 MB၊ shared)၊ raw dataset (84 MB၊ ပြန်ရယူနိုင်)၊ curated parquet (1500 MB၊ shared၊ reproducible)၊ tokenizer (3 MB၊ shared)။
4. Policy function — `must_reproduce` ဖြစ်ပါက DVC၊ shared model weight ဖြစ်ပါက Git LFS၊ ကျန်ပါက `.gitignore`။
5. ရလဒ်ကို `path` sorted အစဉ်ဖြင့် print ပြီး အကြောင်းရင်းကို တစ်လိုင်း ထည့်ပါ။ Pattern စာရင်းများကို `sorted()` ဖြင့် print ပါ။

**အောင်မြင်မှု စစ်နည်း။** `data/training_set.parquet` → `DVC`၊ `models/checkpoint.pt` → `Git LFS`၊ `data/raw/reviews.csv` → `.gitignore`။
Pattern စာရင်းတွင် `*.pt` နှင့် `models/` ပါရမည်။ `sorted()` မသုံးဘဲ set ကို print ခြင်း မပြုရ။

## Exercise 6 — Dataset အစီရင်ခံစာ ထုတ်ခြင်း

**လိုအပ်ချက်။** Exercise 1–5 ၏ ရလဒ်များကို စုစည်းပြီး dataset တစ်ခု၏ အစီရင်ခံစာ တစ်ခု print ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. CSV ဖိုင် ရေးပြီး record အားလုံးကို ဖတ်ပါ။
2. ထို record များကို `json.dump` ဖြင့် `reviews.json` အဖြစ် ရေးပါ။
3. `os.path.getsize` ဖြင့် CSV နှင့် JSON ဖိုင် နှစ်ခု၏ byte အရေအတွက် ကို **တကယ် တိုင်းပါ**။ အချိုးကို print ပါ။
4. Exercise 3 ၏ split ကို ပြန်လုပ်ပြီး row အရေအတွက် ကို ထည့်ပါ။
5. Streaming နှင့် loading ၏ peak (64 KiB bucket) ကို ထည့်ပါ။ Label အရေအတွက် (key sorted) ကို ထည့်ပါ။
6. Cache တည်နေရာ နှစ်ခု — `~/.cache/huggingface/datasets/` နှင့် `~/.cache/huggingface/hub/` — ကို မှတ်ပါ။
7. Parquet နှင့် Arrow ၏ byte အရေအတွက်ကို **မဖော်ပြရ**။ Standard library ဖြင့် ထို format နှစ်မျိုးကို ရေး၍ မရနိုင်သောကြောင့် မတိုင်းတာရသေးသည့် ကိန်းဂဏန်းကို မတီးရ။ ထို အချက်ကို အစီရင်ခံစာထဲ မှတ်ရမည်။

**အောင်မြင်မှု စစ်နည်း။** JSON ဖိုင်သည် CSV ဖိုင် ထက် **ကြီးရမည်** — key အမည်များကို row တိုင်းတွင် ထပ်ရေးသည့်အတွက် ဖြစ်သည်။
CSV နှင့် JSON byte အရေအတွက် နှစ်ခုစလုံးသည် သုည ထက် ကြီးရမည်။ Split သုံးခု၏ row စုစုပေါင်းသည် dataset ၏ row စုစုပေါင်းနှင့် တူရမည်။

## Lab ကို run စစ်ခြင်း

```bash
python3 modules/09_data_management/lab.py
```

Exercise တိုင်း ပြီးဆုံးသည့်အခါ `[OK] exercise_N — <အတိုချုပ်>` လိုင်း ကို print ရမည်။
အားလုံး အောင်မြင်ပါက နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ကို ပြပြီး exit code `0` ဖြင့် ပြီးဆုံးရမည်။
