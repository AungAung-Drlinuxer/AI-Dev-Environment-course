# Module 12 — Exercise

Exercise တိုင်းကို `modules/12_debugging_and_profiling/lab.py` တွင် သက်ဆိုင်ရာ `exercise_N()`
function အဖြစ် implement လုပ်ထားသည်။ `python3 modules/12_debugging_and_profiling/lab.py` ကို run ပါ။
Lab သည် offline ဖြစ်သည် — Python standard library သာ သုံးသည်; torch၊ network၊ GPU မလိုပါ။
Nested list ကို tensor အဖြစ် ကိုယ်စားပြုသဖြင့် shape၊ dtype နှင့် NaN ကို torch မလိုဘဲ စစ်နိုင်သည်။

## Exercise 1 — debug_print ဖြင့် shape၊ dtype နှင့် NaN ကို ကြည့်ရှုခြင်း

**လိုအပ်ချက်** — nested list ကို tensor အဖြစ် ယူ၍ shape၊ dtype၊ min၊ max၊ mean နှင့် NaN ရှိ/မရှိကို
source ၏ `debug_print(name, tensor)` ပုံစံအတိုင်း တစ်လိုင်းတည်းဖြင့် ပြရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ `tensor_shape(data)` ဖြင့် nested list ၏ shape ကို tuple အဖြစ် ရယူသည် — `[[1,2],[3,4]]` သည် `(2, 2)` ဖြစ်သည်။
၂။ `flatten(data)` ဖြင့် element အားလုံးကို flat list အဖြစ် ချသည်။
၃။ `infer_dtype(values)` ဖြင့် element အမျိုးအစားမှ `bool`၊ `int64` သို့မဟုတ် `float32` ကို ခန့်မှန်းသည်။
၄။ min၊ max နှင့် mean ကို NaN/Inf မဟုတ်သည့် တန်ဖိုးများအပေါ်တွင် တွက်ပြီး `has_nan` ကို သီးခြား ပြသည်။
၅။ Deterministic batch (၃×၄) ကို စစ်ပြီးနောက် ကွက်တစ်ခုတွင် `float("nan")` ကို ထည့်၍ ထပ် စစ်သည်။

**အောင်မြင်မှု စစ်နည်း** — shape သည် `(3, 4)` ဖြစ်ရမည်၊ dtype သည် `float32` ဖြစ်ရမည်၊
original batch တွင် `has_nan=False` ဖြစ်ရမည်၊ NaN ထည့်ပြီးနောက် `has_nan=True` နှင့် `nan_count=1`
ဖြစ်ရမည်၊ min နှင့် max သည် `-2.0` နှင့် `2.0` ဖြစ်ရမည်။ Output တွင် `[OK] exercise_1` ပေါ်ရမည်။

## Exercise 2 — သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို ဖမ်းခြင်း

**လိုအပ်ချက်** — forward pass တွင် စားခြင်းမှ တကယ်ဖြစ်သည့် NaN ကို ဖန်တီး၍ `nan_detector`
ဖြင့် step အလိုက် ဖမ်းရမည်။ NaN ကို **ဖော်ပြခြင်း မဟုတ်ဘဲ တကယ် run ၍ ထုတ်ရမည်**။

**လုပ်ရမည့်အဆင့်**

၁။ ပထမ path — `1.0 / 0.0` ကို `try/except` ဖြင့် ခေါ်၍ `ZeroDivisionError` ကို ဖမ်းသည်။
   Pure Python တွင် သုညဖြင့် စားခြင်းသည် exception မြှင့်သည်။
၂။ ဒုတိယ path — IEEE 754 အရ divisor သည် non-finite (`inf`) ဖြစ်သောအခါ `inf / inf` သည်
   exception မမြှင့်ဘဲ **NaN အမှန်** ကို ပြန်သည်။ `forward_pass(inputs, float("inf"))` ကို ခေါ်သည်။
၃။ `nan_detector(values, step)` ဖြင့် `math.isnan` သုံး၍ NaN ရှိသည့် index များကို ရှာသည်။
၄။ NaN ၏ index နှင့် step ကို လူဖတ်နိုင်သည့် လိုင်းဖြင့် ပြသည်။

**အောင်မြင်မှု စစ်နည်း** — `ZeroDivisionError` ဖမ်းမိရမည်၊ output တွင် NaN တစ်ခု ရှိရမည်၊
`nan_indices == [2]` ဖြစ်ရမည်၊ `outputs[2]` သည် NaN ဖြစ်ရမည်၊ finite/inf ရလဒ်သည် `0.0` ဖြစ်ရမည်။
Output တွင် `[OK] exercise_2` ပေါ်ရမည်။

## Exercise 3 — matmul shape မတိုက်ဆိုင်ခြင်းကို ကြိုတင် ဖမ်းခြင်း

**လိုအပ်ချက်** — matmul မလုပ်မီ shape နှစ်ခု တိုက်ဆိုင်/မတိုက်ဆိုင် စစ်ပြီး မတိုက်ဆိုင်ပါက
ရှင်းလင်းသည့် အကြောင်းပြချက်ဖြင့် ငြင်းရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ Matmul ၏ လိုအပ်ချက်သည် `a[1] == b[0]` ဖြစ်သည်။ Output shape သည် `(a[0], b[1])` ဖြစ်သည်။
၂။ `check_shapes(a_shape, b_shape)` တွင် 2D မဟုတ်သည့် shape ကို ဦးစွာ ငြင်းသည်။
၃။ အခြေအနေ သုံးမျိုးကို စမ်းသည် — တိုက်ဆိုင်သည့် shape၊ inner dimension မတိုက်ဆိုင်သည့် shape၊
   1D shape။
၄။ တိုက်ဆိုင်သည့် အခြေအနေအတွက် guard ကို အတည်ပြုပြီးမှ `matmul(a, b)` ကို တကယ် ခေါ်သည်။

**အောင်မြင်မှု စစ်နည်း** — `(4, 784) @ (784, 256)` သည် အတည်ပြု ခံရမည်၊ output shape သည်
`(4, 256)` ဖြစ်ရမည်၊ `(4, 784) @ (256, 10)` နှင့် 1D case တို့သည် ငြင်းခံရမည်၊
`[[1,2],[3,4]] @ [[5,6],[7,8]]` သည် `[[19, 22], [43, 50]]` ဖြစ်ရမည်။ Output တွင် `[OK] exercise_3` ပေါ်ရမည်။

## Exercise 4 — cProfile-style stats မှ hotspot ကို ရှာခြင်း

**လိုအပ်ချက်** — ပေးထားသည့် cProfile-style stats ဇယားမှ အချိန်အများဆုံး function ကို
ရှာရမည်၊ ထို့အပြင် project ၏ ကိုယ်ပိုင် code ထဲမှ hotspot ကို သီးခြား ခွဲထုတ်ရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ ဇယားတွင် (function name, ncalls, tottime, cumtime) ဟူသည့် column လေးခု ရှိသည်။
၂။ `rank_functions(stats, key, limit)` ဖြင့် ဇယားကို column အလိုက် စီသည် — cumtime အများဆုံးကို ဦးစွာ ကြည့်သည်။
၃။ `is_own_code(name)` ဖြင့် `site-packages` နှင့် `<built-in` frame များကို ဖယ်သည်။
၄။ `hottest_own_code(stats, "tottime")` ဖြင့် project code ထဲမှ self time အများဆုံး function ကို ရှာသည်။
၅။ Hotspot သည် အနှေးဆုံး function ၏ cumtime ထဲမှ ရာခိုင်နှုန်း မည်မျှ ရှိသည်ကို တွက်ပြသည်။

**အောင်မြင်မှု စစ်နည်း** — cumtime အများဆုံးသည် `train_step` ဖြစ်ရမည်၊ project code ထဲမှ
tottime အများဆုံးသည် `load_batch` ဖြစ်ရမည်၊ `site-packages` frame သည် own code မဟုတ်ရ၊
hotspot share သည် ၄၀ ရာခိုင်နှုန်း ထက် ကြီးရမည်။ Output တွင် `[OK] exercise_4` ပေါ်ရမည်။

## Exercise 5 — tracemalloc-style snapshot မှ နေရာကို ရှာခြင်း

**လိုအပ်ချက်** — ပေးထားသည့် tracemalloc-style snapshot မှ အများဆုံး allocate လုပ်သည့်
နေရာကို ရှာပြီး လူဖတ်နိုင်သည့် size format ဖြင့် ပြရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ Snapshot တွင် (location, size_bytes, count) ဟူသည့် တန်ဖိုး သုံးခု ရှိသည်။
၂။ `memory_report(snapshot, limit)` ဖြင့် size အလိုက် စီ၍ tracemalloc ၏ format အတိုင်း
   `location: size=..., count=..., average=...` လိုင်းများ ထုတ်သည်။
၃။ `format_size(nbytes)` ဖြင့် byte ကို MiB၊ KiB သို့မဟုတ် B အဖြစ် ပြောင်းသည် — `average` သည် size ÷ count ဖြစ်သည်။
၄။ `top_allocation(snapshot)` ဖြင့် အများဆုံး နေရာကို ခွဲထုတ်ပြီး snapshot စုစုပေါင်းကို ပြသည်။

**အောင်မြင်မှု စစ်နည်း** — အများဆုံး နေရာသည် `data_loader.py:120` ဖြစ်ရမည်၊ size သည်
`51200000` byte ဖြစ်ရမည်၊ `format_size(51200000) == "48.8 MiB"` ဖြစ်ရမည်၊
`format_size(262144) == "256.0 KiB"` ဖြစ်ရမည်။ Output တွင် `[OK] exercise_5` ပေါ်ရမည်။

## Exercise 6 — loss curve မှ overfit ကို ဆုံးဖြတ်ခြင်း

**လိုအပ်ချက်** — epoch၊ train loss နှင့် validation loss ပါသည့် ဇယားမှ run သည် overfit
ဖြစ်/မဖြစ်၊ healthy ဖြစ်/မဖြစ် ဆုံးဖြတ်ရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ ဇယားထဲတွင် NaN ရှိပါက `numerical-instability` ဟု ဆုံးဖြတ်သည် — အခြား စစ်ဆေးမှု မလိုပါ။
၂။ `best_val_loss` နှင့် ထို တန်ဖိုး ရသည့် epoch ကို ရှာသည်။
၃။ Train loss ကျနေစဉ် val loss သည် best value မှ တက်လာပါက `overfitting` ဟု ဆုံးဖြတ်သည်။
၄။ နှစ်ခုလုံး တက်ပါက `diverging`၊ နှစ်ခုလုံး ကျပါက `healthy-learning` ဟု ဆုံးဖြတ်သည်။
၅။ ဇယား သုံးခုကို စမ်းသည် — overfit run၊ healthy run နှင့် unstable run။

**အောင်မြင်မှု စစ်နည်း** — overfit table ၏ verdict သည် `overfitting` ဖြစ်ရမည်၊ best val epoch သည်
၃ ဖြစ်ရမည်၊ healthy table သည် `healthy-learning` ဖြစ်ရမည်၊ NaN ပါသည့် table သည်
`numerical-instability` ဖြစ်ရမည်။ Output တွင် `[OK] exercise_6` ပေါ်ရမည်။
နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ပေါ်ရမည်။
