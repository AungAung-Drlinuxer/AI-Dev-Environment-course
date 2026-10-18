# Module 12 — Solution

အောက်ပါ ရလဒ် အားလုံးသည် `python3 modules/12_debugging_and_profiling/lab.py` ကို တကယ် run ၍
ရသည့် output ဖြစ်သည်။ Hand-computed တန်ဖိုး မဟုတ်ပါ။ Run သုံးကြိမ်၏ output သည်
byte တစ်လုံးမှ မကွာဘဲ တူညီသည် (wall-clock time ကို ပုံနှိပ်မထုတ်ပါ)။

## Exercise 1 — debug_print ဖြင့် shape၊ dtype နှင့် NaN ကို ကြည့်ရှုခြင်း

**အဖြေ**

```python
batch = make_batch(3, 4)
clean = debug_print("input batch", batch)

injected = [row[:] for row in batch]
injected[1][2] = float("nan")
with_nan = debug_print("injected NaN", injected)
```

**Run ရလဒ်**

```
Exercise 1 — debug_print (nested list မှ shape၊ dtype၊ NaN ကို ကြည့်ရှုခြင်း)
  input batch: shape=(3, 4), dtype=float32, device=cpu, min=-2.0000, max=2.0000, mean=0.0208, has_nan=False
  element count : 12
  injected NaN: shape=(3, 4), dtype=float32, device=cpu, min=-2.0000, max=1.5000, mean=-0.1591, has_nan=True
[OK] exercise_1 — debug_print ဖြင့် shape၊ dtype၊ NaN ကို စစ်ဆေးပြီးပါသည်
```

**ရှင်းလင်းချက်** — `tensor_shape` သည် nested list ကို အပေါ်မှ အောက်သို့ လိုက်၍
`(3, 4)` ကို ရသည်။ `infer_dtype` သည် element များတွင် float ရှိသဖြင့် `float32` ဟု ပြန်သည်
(PyTorch ၏ default float dtype ကို ကိုယ်စားပြုသည်)။ mean သည် `0.25 / 12 = 0.0208` ဖြစ်သည်။
NaN ထည့်ပြီးနောက် min/max/mean ကို NaN မဟုတ်သည့် ၁၁ ခုအပေါ်တွင် တွက်သဖြင့်
max သည် `2.0` မှ `1.5` သို့ ကျပြီး mean သည် `-0.1591` ဖြစ်သည်; `has_nan=True` က
NaN ရှိကြောင်း သီးခြား အသိပေးသည်။ ဤအချက်သည် အရေးကြီးသည် — NaN တစ်ခုတည်းက
min/max တွက်ချက်မှုကို ဖျက်ဆီးနိုင်သည်; ထို့ကြောင့် `has_nan` ကို အရင် စစ်ရသည်။

## Exercise 2 — သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို ဖမ်းခြင်း

**အဖြေ**

```python
try:
    1.0 / 0.0
except ZeroDivisionError as exc:
    raised = type(exc).__name__

outputs = forward_pass([1.0, 2.0, float("inf"), -4.0], float("inf"))
report = nan_detector(outputs, step=500)
```

**Run ရလဒ်**

```
Exercise 2 — nan_detector (သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို ဖမ်းခြင်း)
  1.0 / 0.0 -> ZeroDivisionError: division by zero
  forward pass   : inputs=[1.0, 2.0, inf, -4.0], divisor=inf
  outputs        : [0.0, 0.0, nan, -0.0]
  step 500      : has_nan=True, nan_indices=[2], inf_indices=[]
[OK] exercise_2 — စားခြင်းမှ ဖြစ်သော NaN ကို ဖန်တီး၍ ဖမ်းပြီးပါသည်
```

**ရှင်းလင်းချက်** — NaN ကို ဖော်ပြခြင်း မဟုတ်ဘဲ **တကယ် run ၍** ထုတ်ထားသည်။ Pure Python
တွင် divisor သည် ကိန်းဂဏန်း `0.0` ဖြစ်ပါက `ZeroDivisionError: division by zero` မြှင့်သည်
(ပထမ လိုင်း)။ သို့သော် divisor သည် non-finite ဖြစ်သော `inf` ဖြစ်ပါက IEEE 754 အရ
`inf / inf` သည် exception မမြှင့်ဘဲ **NaN** ကို ပြန်သည် — ဤအချက်သည် AI ၏ ကိုယ်ပိုင်
loss/custom op တွင် သုညဖြင့် စားခြင်းကြောင့် NaN ရသည့် လမ်းကြောင်း ဖြစ်သည်။
`forward_pass` ၏ output တွင် `outputs[2]` သည် `nan` ဖြစ်ပြီး `1.0 / inf` သည် `0.0` ဖြစ်သည်။
`nan_detector` သည် `math.isnan` သုံး၍ index `2` ကို ရှာပြီး step `500` တွင် NaN ဖြစ်ကြောင်း
သတင်းပို့သည်။ တကယ့် training တွင် ဤ report သည် loss သည် မည်သည့် step တွင် ပျက်သည်ကို
ညွှန်ပြသည်; ထို့နောက် gradient တစ်ခုချင်းကို စစ်ရမည်။

## Exercise 3 — matmul shape မတိုက်ဆိုင်ခြင်းကို ကြိုတင် ဖမ်းခြင်း

**အဖြေ**

```python
for a_shape, b_shape in [((4, 784), (784, 256)), ((4, 784), (256, 10)), ((4,), (4, 4))]:
    result = check_shapes(a_shape, b_shape)

guard = check_shapes(tensor_shape([[1.0, 2.0], [3.0, 4.0]]), tensor_shape([[5.0, 6.0], [7.0, 8.0]]))
product = matmul([[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]])
```

**Run ရလဒ်**

```
Exercise 3 — check_shapes (matmul shape မတိုက်ဆိုင်ခြင်းကို ကြိုတင် ဖမ်းခြင်း)
  (4, 784) @ (784, 256) -> OK: shapes တိုက်ဆိုင်သည်
    expected output shape: (4, 256)
  (4, 784) @ (256, 10) -> REJECT: inner dimension မတိုက်ဆိုင်: a[1]=784 != b[0]=256
  (4,) @ (4, 4) -> REJECT: matmul အတွက် 2D shape နှစ်ခု လိုအပ်သည်
  guard  (2, 2) @ (2, 2) -> ok=True
  matmul (2, 2) @ (2, 2) = [[19.0, 22.0], [43.0, 50.0]]
[OK] exercise_3 — matmul shape များကို မြှောက်မီ စစ်ဆေးပြီးပါသည်
```

**ရှင်းလင်းချက်** — matmul ၏ လိုအပ်ချက်သည် `a[1] == b[0]` ဖြစ်သည်။ ပထမ case တွင်
`784 == 784` ဖြစ်သဖြင့် အတည်ပြု ခံရပြီး output shape သည် `(4, 256)` ဖြစ်သည်။ ဒုတိယ case
တွင် `784 != 256` ဖြစ်သဖြင့် မြှောက်မီ ငြင်းခံရသည် — မငြင်းပါက PyTorch သည် runtime တွင်
ကျရှုံးမည် ဖြစ်သည်။ တတိယ case တွင် shape သည် 2D မဟုတ်သဖြင့် ငြင်းခံရသည်။ ဤနည်းလမ်းသည်
bug ကို ၈ နာရီ ကြာသည့် training run ၏ အလယ်တွင် မတွေ့မီ၊ မြှောက်ခြင်း မတိုင်မီ အဆင့်တွင်
ဖမ်းသည်။ Guard အတည်ပြုပြီးမှ `matmul` ကို ခေါ်သဖြင့် ရလဒ်သည် `[[19.0, 22.0], [43.0, 50.0]]` ဖြစ်သည်။

## Exercise 4 — cProfile-style stats မှ hotspot ကို ရှာခြင်း

**အဖြေ**

```python
rank_functions(PROFILE_STATS, "cumtime", 5)
hottest_own_code(PROFILE_STATS, "tottime")
```

**Run ရလဒ်**

```
Exercise 4 — profile_hotspot (cProfile-style stats မှ နှေးဆုံး function ကို ရှာခြင်း)
  top 5 by cumtime:
    debug_tools.py:120(train_step)  ncalls=10000  tottime=0.4210  cumtime=12.5000
    ~/site-packages/torch/nn/modules/module.py:1501(_call_impl)  ncalls=10000  tottime=0.5120  cumtime=11.9000
    debug_tools.py:88(load_batch)  ncalls=10000  tottime=6.2100  cumtime=6.2400
    ~/site-packages/torch/nn/functional.py:2202(linear)  ncalls=10000  tottime=0.8800  cumtime=1.1200
    ~/site-packages/torch/autograd/__init__.py:200(backward)  ncalls=10000  tottime=0.0400  cumtime=0.9100
  own-code hotspot : debug_tools.py:88(load_batch)
    ncalls=10000  tottime=6.2100  cumtime=6.2400
  slowest overall  : debug_tools.py:120(train_step)  cumtime=12.5000
  hotspot share    : 49.7% of the slowest overall cumtime
[OK] exercise_4 — cProfile-style ဇယားမှ hotspot ကို ခွဲထုတ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — cumtime အလိုက် စီပါက `train_step` (12.5000) သည် ထိပ်တွင် ရှိသည် — ဤအချက်သည်
training loop တစ်ခုလုံးကို ကိုယ်စားပြုသောကြောင့် မျှော်လင့်ရသည့် အတိုင်း ဖြစ်သည်။ သို့သော်
**self time** (tottime) အလိုက် ကြည့်ပါက `load_batch` သည် `6.2100` ရှိပြီး `train_step` သည်
`0.4210` သာ ရှိသည် — ၄၉.၇ ရာခိုင်နှုန်းသည် data loading ဖြစ်သည်။ Source ၏ ဖော်ပြချက်အတိုင်း
ဤသည် profiling တွင် အဖြစ်အများဆုံး တွေ့ရှိချက် ဖြစ်သည်: ဖြေရှင်းချက်သည် GPU အသစ် မဟုတ်ဘဲ
DataLoader ၏ `num_workers > 0` ဖြစ်သည်။ `is_own_code` သည် `site-packages` နှင့် built-in frame များကို
ဖယ်သဖြင့် hotspot သည် ကိုယ်တိုင် ပြင်နိုင်သည့် code ဖြစ်ကြောင်း သေချာစေသည်။

## Exercise 5 — tracemalloc-style snapshot မှ နေရာကို ရှာခြင်း

**အဖြေ**

```python
memory_report(MEMORY_SNAPSHOT, 3)
top_allocation(MEMORY_SNAPSHOT)
format_size(51200000)      # "48.8 MiB"
```

**Run ရလဒ်**

```
Exercise 5 — memory_hotspot (tracemalloc-style snapshot မှ အများဆုံး နေရာကို ရှာခြင်း)
  data_loader.py:120: size=48.8 MiB, count=20, average=2.4 MiB
  data_loader.py:64: size=12.2 MiB, count=40, average=312.5 KiB
  train.py:210: size=3.9 MiB, count=1, average=3.9 MiB
  top allocation   : data_loader.py:120 -> 48.8 MiB in 20 allocations
  snapshot total   : 66.2 MiB over 5 sites
[OK] exercise_5 — tracemalloc-style snapshot မှ hotspot ကို ရှာပြီးပါသည်
```

**ရှင်းလင်းချက်** — Snapshot တွင် (location, size, count) သုံးခု ပါသည်။ `average` သည်
`size / count` ဖြစ်ပြီး `51200000 / 20 = 2560000` byte ဖြစ်သဖြင့် `2.4 MiB` ဖြစ်သည်။
`format_size` သည် ၁ MiB နှင့် အထက် ဖြစ်ပါက MiB ဖြင့်၊ ၁ KiB နှင့် အထက် ဖြစ်ပါက KiB ဖြင့်၊
ထို့အောက် ဖြစ်ပါက B ဖြင့် ပြသည် — `262144 / 1024 = 256.0` ဖြစ်သဖြင့် `256.0 KiB` ဖြစ်သည်။
အများဆုံး နေရာသည် `data_loader.py:120` ဖြစ်ပြီး ၄၈.၈ MiB ဖြစ်သည် — ဤအချက်သည် Exercise 4 ၏
`load_batch` hotspot နှင့် တိုက်ဆိုင်သည်။ Memory ပြဿနာကို ရှာသည့်အခါ ဤလိုင်းသည် code
မည်သည့် နေရာကို ဦးစွာ ပြင်ရမည်ကို ညွှန်ပြသည်။

## Exercise 6 — loss curve မှ overfit ကို ဆုံးဖြတ်ခြင်း

**အဖြေ**

```python
training_health_report(OVERFIT_HISTORY)
training_health_report(HEALTHY_HISTORY)
training_health_report(UNSTABLE_HISTORY)
```

**Run ရလဒ်**

```
Exercise 6 — training_health_report (loss curve မှ overfit ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း)
  overfit run:
    epoch 1: train_loss=2.3026, val_loss=2.2900
    epoch 2: train_loss=1.8200, val_loss=1.7800
    epoch 3: train_loss=1.3100, val_loss=1.4200
    epoch 4: train_loss=1.0200, val_loss=1.5100
    epoch 5: train_loss=0.8100, val_loss=1.6400
    epoch 6: train_loss=0.6200, val_loss=1.7900
    epoch 7: train_loss=0.5100, val_loss=1.9200
    epoch 8: train_loss=0.4300, val_loss=2.1100
    best val loss: 1.4200 at epoch 3
    verdict: overfitting
    reason : train loss ကျနေစဉ် val loss သည် epoch 3 ၏ 1.4200 မှ 2.1100 သို့ တက်လာသည်
  healthy run:
    epoch 1: train_loss=2.3026, val_loss=2.3100
    epoch 2: train_loss=1.9100, val_loss=1.9500
    epoch 3: train_loss=1.4200, val_loss=1.4900
    epoch 4: train_loss=1.0100, val_loss=1.1200
    epoch 5: train_loss=0.7800, val_loss=0.8900
    best val loss: 0.8900 at epoch 5
    verdict: healthy-learning
    reason : train loss နှင့် val loss နှစ်ခုလုံး ကျနေသည် (val 2.3100 -> 0.8900)
  unstable run:
    epoch 1: train_loss=2.3026, val_loss=2.3100
    epoch 2: train_loss=1.6100, val_loss=1.7000
    epoch 3: train_loss=nan, val_loss=nan
    epoch 4: train_loss=nan, val_loss=nan
    verdict: numerical-instability
    reason : NaN loss ကို epoch [3, 4] တွင် တွေ့သည် — learning rate၊ log(0) သို့မဟုတ် သုညဖြင့် စားခြင်းကို စစ်ရမည်
[OK] exercise_6 — loss curve မှ overfit ကို ဆုံးဖြတ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — overfit run တွင် train loss သည် `2.3026` မှ `0.4300` သို့ ကျနေသည်; သို့သော်
val loss သည် epoch ၃ တွင် အနိမ့်ဆုံး `1.4200` ကို ရပြီးနောက် `2.1100` အထိ တက်လာသည်။
ဤသည်သည် overfitting ၏ လက္ခဏာ ဖြစ်သည် — model သည် training data ကို အလွန်အကျွံ မှတ်မိလာပြီး
generalize မလုပ်နိုင်တော့ပါ။ healthy run တွင် နှစ်ခုလုံး ကျနေသဖြင့် `healthy-learning` ဖြစ်သည်။
unstable run တွင် NaN ကို epoch ၃ မှစ၍ တွေ့သဖြင့် `numerical-instability` ဟု ဆုံးဖြတ်သည် —
ဤအခြေအနေတွင် learning rate၊ `log(0)` နှင့် သုညဖြင့် စားခြင်းကို ဦးစွာ စစ်ရမည်။
ဆုံးဖြတ်ချက် အစဉ်သည် အရေးကြီးသည် — NaN ရှိပါက အခြား စစ်ဆေးမှု မလိုပါ။

## Lab အပြည့်အစုံ ၏ နောက်ဆုံးလိုင်း

```
[PASS] All 6/6 exercises passed successfully.
```

Exit code — `0`။ Run သုံးကြိမ်၏ output သည် တူညီသည် (deterministic; wall-clock time မပါပါ)။
