# Module 13 — Python for AI Engineering — Exercise

ဤ exercise ၆ ခုကို `modules/13_python_for_ai_engineering/lab.py` တွင် `def exercise_1()` … `def exercise_6()` အဖြစ် implement လုပ်ထားသည်။
Exercise တိုင်းသည် **Python standard library သာ** သုံးရမည် — `numpy`၊ `pandas` နှင့် network ကို မသုံးရ။ Random လိုပါက `random.Random(seed)` ကဲ့သို့ seeded generator ကို သုံးရမည်၊ module အဆင့် `random` ကို မသုံးရ။
Set ကို print လုပ်လိုပါက `sorted()` ဖြင့် ပြရမည်။

## Exercise 1 — `Record` dataclass နှင့် CSV loader

**လိုအပ်ချက်။** `@dataclass(frozen=True)` ဖြင့် `Record` ကို သတ်မှတ်ရမည်။ ထို class တွင် `features: tuple[float, ...]` နှင့် `label: int` field နှစ်ခု ရှိရမည်။ ထို့နောက် Script ကိုယ်တိုင် CSV ဖိုင် တစ်ခုကို temporary directory ထဲ ရေးပြီး၊ ထို ဖိုင်ကို `Record` စာရင်း အဖြစ် ပြန်ဖတ်ရမည်။ Row အရေအတွက်သည် ၄၀၀ ဖြစ်ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. `random.Random(SEED)` ဖြင့် cluster နှစ်ခုမှ record ၄၀၀ ခု ဖန်တီးပါ — label 0 အတွက် `(2.0, 50.0)`၊ label 1 အတွက် `(4.0, 70.0)` ဗဟိုနှင့် ပြန့်နှံ့မှု `(1.0, 10.0)`။
2. `record_to_row` ဖြင့် `Record` ကို `x1`၊ `x2`၊ `label` key များ ပါသည့် dict အဖြစ် ပြောင်းပါ။
3. `tempfile.mkdtemp()` ဖြင့် temporary directory ဖန်တီးပြီး `csv.DictWriter` ဖြင့် `data.csv` ကို ရေးပါ။ `newline=""` နှင့် `encoding="utf-8"` ကို မမေ့ရ။
4. `csv.DictReader` ဖြင့် ထို ဖိုင်ကို ပြန်ဖတ်ပြီး `row_to_record` မှတစ်ဆင့် `Record` စာရင်း တည်ဆောက်ပါ။ CSV သည် field တိုင်းကို string အဖြစ် ပြန်ပေးသည်ကို သတိထားပါ — `float()` နှင့် `int()` ဖြင့် ပြောင်းရမည်။
5. Row အရေအတွက်၊ column အမည် (sorted)၊ label အရေအတွက် နှင့် ပထမ record ကို print ပါ။
6. `shutil.rmtree(..., ignore_errors=True)` ကို `finally` block ထဲ ထည့်ပါ။

**အောင်မြင်မှု စစ်နည်း။** `len(loaded) == 400`၊ `loaded == records` (roundtrip သည် တန်ဖိုး တိုင်းကို ထိန်းသည်)၊ `isinstance(loaded[0], Record)` ဖြစ်ပြီး label count နှစ်ခု၏ ပေါင်းလဒ်သည် ၄၀၀ ဖြစ်ရမည်။

## Exercise 2 — seed ပါသည့် train/test split

**လိုအပ်ချက်။** `train_test_split(items, test_fraction=0.2, seed=7)` ကို ရေးရမည်။ Function သည် `random.Random(seed)` ကို သုံးပြီး index စာရင်းကို shuffle လုပ်ရမည်။ Test share 20% ဖြစ်ပါက record ၄၀၀ မှ train ၃၂၀ နှင့် test ၈၀ ရရမည်။

**လုပ်ရမည့် အဆင့်။**

1. `test_fraction` သည် `0.0 < x < 1.0` မဟုတ်ပါက `ValueError` မြှောက်ပါ။ `len(items) < 2` ဖြစ်ပါက လည်း `ValueError` မြှောက်ပါ။
2. `order = list(range(len(items)))` ဖန်တီးပြီး `random.Random(seed).shuffle(order)` လုပ်ပါ။ Index များကို shuffle လုပ်သောကြောင့် input list သည် မူရင်း အတိုင်း ကျန်ရမည်။
3. `n_test = min(max(1, round(len(items) * test_fraction)), len(items) - 1)` ဖြင့် side တိုင်းတွင် အနည်းဆုံး item တစ်ခု ကျန်စေပါ။
4. Train နှင့် test ကို index order မှ ပြန်ဆောက်ပြီး အရွယ်အစား၊ ပေါင်းလဒ် နှင့် overlap ကို print ပါ။
5. Seed တူညီပါက split တူညီသည်ကို နှင့် seed ၁ သို့ ပြောင်းပါက ပထမ record ပြောင်းသည်ကို စစ်ပါ။

**အောင်မြင်မှု စစ်နည်း။** `len(train) == 320`၊ `len(test) == 80`၊ `len(train) + len(test) == 400`၊ `set(train) & set(test) == set()`၊ seed တူညီသည့် ခေါ်ဆိုမှု နှစ်ခုသည် feature စာရင်း တူညီပြီး seed အသစ်သည် ပထမ record ကို ပြောင်းရမည်။

## Exercise 3 — mini-batch generator

**လိုအပ်ချက်။** `batches(items, batch_size, drop_last=False)` ကို generator အဖြစ် ရေးရမည်။ Item ၃၂၀ နှင့် batch size ၄၈ အတွက် batch အရေအတွက်သည် ၇ ခု ဖြစ်ရမည် — နောက်ဆုံး batch သည် ၃၂ ခု ဖြစ်သည်။

**လုပ်ရမည့် အဆင့်။**

1. `batch_size < 1` ဖြစ်ပါက `ValueError` မြှောက်ရမည်။ ထို check ကို **အပြင်ဘက်** function တွင် ထားပါ၊ generator အတွင်း မထားရ — generator function သည် ပထမ `next()` အထိ code မရပ်သောကြောင့် error သည် နောက်ကျမှ လာသည်။
2. အတွင်းဘက် `_batch_iter` တွင် `itertools.islice` ဖြင့် batch တိုင်းကို ယူပါ။
3. Batch အလွတ် ဖြစ်ပါက သို့မဟုတ် `drop_last=True` ဖြစ်ပြီး batch သည် batch size အောက် ငယ်ပါက ရပ်ပါ။
4. Batch အရွယ်အစား စာရင်း၊ `drop_last=True` ဖြင့် ရသည့် စာရင်း နှင့် generator expression အပေါ် batch ဖွဲ့ခြင်းကို print ပါ။
5. Epoch loop တစ်ခုတွင် epoch တိုင်းအတွက် `batches()` ကို **ထပ်ခေါ်** ပြီး generator အသစ် ဖန်တီးပါ။ `batches(range(7), 3)` ၏ အလျားများသည် `[3, 3, 1]` ဖြစ်ရမည်။

**အောင်မြင်မှု စစ်နည်း။** `sizes == [48, 48, 48, 48, 48, 48, 32]`၊ ပေါင်းလဒ်သည် ၃၂၀၊ `drop_last` စာရင်းသည် batch ၆ ခု၊ epoch နှစ်ခု၏ စာရင်းသည် တူညီရမည်။

## Exercise 4 — dot product၊ mean နှင့် standardizer

**လိုအပ်ချက်။** `dot`၊ `mean`၊ `std` နှင့် `make_standardizer` ကို pure Python ဖြင့် ရေးရမည်။ `dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0])` သည် 32.0 ဖြစ်ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. `dot` ကို `zip(a, b, strict=True)` ဖြင့် ရေးပါ။ `strict` သည် vector အလျား မတူပါက `ValueError` မြှောက်သည်။ ထို argument သည် **Python 3.10+** လိုသည်။
2. `mean` သည် list အလွတ်အတွက် `ValueError` မြှောက်ရမည်။ `std` သည် `n` ဖြင့် စားသည့် population standard deviation ဖြစ်ရမည် — `statistics.pstdev` နှင့် တူညီသည်။
3. `make_standardizer(rows)` သည် column mean နှင့် std ကို တစ်ကြိမ်တည်း တွက်ပြီး ထို တန်ဖိုးများကို ထိန်းထားသည့် closure တစ်ခု ပြန်ပေးရမည်။ Constant column (std = 0) အတွက် scale ကို 1.0 သတ်မှတ်ပါ။
4. Values `[2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]` အတွက် mean နှင့် std ကို print ပါ။
5. Training row `[(1.0, 100.0), (2.0, 300.0), (3.0, 500.0)]` အပေါ် standardizer ကို fit လုပ်ပြီး ထို row များ နှင့် test row `(4.0, 700.0)` ကို standardize လုပ်ပါ။ Standardize လုပ်ပြီးသား training row များ၏ mean သည် 0.0 ဖြစ်ရမည်။

**အောင်မြင်မှု စစ်နည်း။** dot 32.0၊ mean 5.0၊ std 2.0၊ standardize ရလဒ်သည် `[[-1.225, -1.225], [0.0, 0.0], [1.225, 1.225]]`၊ test row သည် `[2.449, 2.449]`၊ အလျား မတူသည့် `dot` သည် `ValueError` မြှောက်ရမည်။

## Exercise 5 — error မတက်သည့် အမှား သုံးမျိုး

**လိုအပ်ချက်။** ဤ lesson တွင် ဖော်ပြသည့် အမှား သုံးမျိုးကို **တကယ် run ၍** သရုပ်ပြပြီး ထို့နောက် ဖြေရှင်းရမည် — share လုပ်ထားသည့် list၊ mutable default argument နှင့် ကုန်သွားသည့် generator။

**လုပ်ရမည့် အဆင့်။**

1. `weights = [0.5, -1.2, 3.0]`၊ `alias = weights`၊ `alias[0] = 99.0` လုပ်ပြီး `weights` ပြောင်းသွားသည်ကို print ပါ။ ထို့နောက် `independent = list(weights)` ဖြင့် copy လုပ်ပြီး `independent[1] = 0.0` ဖြင့် `weights` ကို မထိခိုက်တော့သည်ကို ပြပါ။ `alias is weights` သည် `True` ဖြစ်သည်ကို စစ်ပါ။
2. `def add_bad(item, bucket=[])` နှင့် `def add_good(item, bucket=None)` ကို module အဆင့်တွင် သတ်မှတ်ပါ။ `add_bad("a")` ပြီးနောက် `add_bad("b")` ခေါ်ပါက `['a', 'b']` ရသည်ကို ပြပါ။ `add_good` သည် တစ်ကြိမ်လျှင် တစ်ခုသာ ပေးသည်ကို ပြပါ။
3. `squares = (i * i for i in range(5))` ကို `list()` ဖြင့် နှစ်ကြိမ် ဖြတ်ပါ — ပထမ အကြိမ်တွင် `[0, 1, 4, 9, 16]` ရပြီး ဒုတိယ အကြိမ်တွင် `[]` ရသည်ကို ပြပါ။
4. ဖြေရှင်းရန် `squares_factory()` function တစ်ခု ရေးပြီး epoch တိုင်းအတွက် generator အသစ် ရသည်ကို ပြပါ။
5. `add_bad("c") == ["a", "b", "c"]` ဖြစ်သည်ကို assert ဖြင့် အတည်ပြုပါ — mutable default သည် တကယ် စုပုံနေသည်။

**အောင်မြင်မှု စစ်နည်း။** ထုတ်လာသည့် လိုင်းများသည် `weights` ပြောင်းသွားခြင်း၊ `add_bad` စုပုံခြင်း နှင့် ဒုတိယ pass အလွတ် ဖြစ်ခြင်းကို ပြရမည်။ `add_good("c")` နှင့် `squares_factory()` သည် မှန်ကန်သည့် ရလဒ် ကို ပြရမည်။

## Exercise 6 — အချိန် နှင့် memory အစီရင်ခံစာ

**လိုအပ်ချက်။** Dot product variant ၃ မျိုး — index loop၊ `zip` generator နှင့် `map + operator.mul` — ကို seed ပါသည့် float ၂၀၀,၀၀၀ အပေါ် တိုင်းပြီး list နှင့် generator ၏ peak memory ကို နှိုင်းယှဉ်ပါ။ Output သည် run တိုင်းတွင် တူညီရမည်။

**လုပ်ရမည့် အဆင့်။**

1. `rng = random.Random(SEED)` ဖြင့် vector နှစ်ခု ဖန်တီးပါ။
2. `best_time(fn, *args, repeat=5)` ကို `time.perf_counter()` ဖြင့် ရေးပြီး run ၅ ခုအနက် **အနည်းဆုံး** အချိန်ကို ပြန်ပေးပါ။
3. `peak_bytes(fn)` ကို `tracemalloc` ဖြင့် ရေးပါ — `start()`၊ `fn()`၊ `get_traced_memory()[1]`၊ `finally: stop()`။
4. Variant သုံးမျိုး၏ ရလဒ်သည် တူညီသည်ကို စစ်ပါ။
5. **Wall-clock စက္ကန့်ဂဏန်းကို မပြရ။** ထို အစား repeat အရေအတွက် နှင့် variant အမည် စာရင်း (sorted) ကို print ပါ။
6. `sum([i * i for i in range(100_000)])` နှင့် `sum(i * i for i in range(100_000))` တို့၏ peak ကို တိုင်းပြီး ဂဏန်းကို bucket (list အတွက် 1 MiB၊ generator အတွက် 64 KiB) အထိ round up လုပ်ပြီး print ပါ။

**အောင်မြင်မှု စစ်နည်း။** Variant သုံးမျိုး၏ ရလဒ်သည် 6 decimal အထိ တူညီရမည်၊ အချိန် တိုင်းတာမှု တိုင်းသည် 0 ထက် ကြီးရမည်၊ generator ၏ peak သည် list ၏ peak ထက် ငယ်ရမည်၊ list သည် အနည်းဆုံး 3 MiB ဖြစ်ရမည်။ Run သုံးကြိမ်၏ output သည် byte အလိုက် တူညီရမည်။
