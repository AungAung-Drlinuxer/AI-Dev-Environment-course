# Module 03 — Solution

အောက်ပါ ရလဒ် အားလုံးသည် `python3 modules/03_gpu_setup_and_cloud/lab.py` ကို တကယ် run ၍
ရသည့် output ဖြစ်သည်။ Hand-computed တန်ဖိုး မဟုတ်ပါ။

နမူနာ fixture ၏ အခြေခံ — `24564MiB` total၊ `1234MiB` used၊ ထို့ကြောင့် free သည်
`24564 - 1234 = 23330MiB` ဖြစ်သည်။

## Exercise 1 — nvidia-smi output ကို parse လုပ်ခြင်း

**အဖြေ**

```python
device = parse_nvidia_smi(SAMPLE_NVIDIA_SMI)
```

**Run ရလဒ်**

```
Exercise 1 — parse_nvidia_smi (nvidia-smi ဇယားမှ device အချက်အလက် ဖတ်ခြင်း)
  driver version : 550.54.14
  gpu name       : NVIDIA GeForce RTX 4090
  memory used    : 1234 MiB / 24564 MiB
  memory free    : 23330 MiB
  total bytes    : 25757220864
[OK] exercise_1 — nvidia-smi ဇယားမှ device အချက်အလက် ဖတ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — `25757220864 = 24564 * 1024 * 1024` ဖြစ်သည်။ Parser သည် driver version ကို
`Driver Version:` နောက်မှ၊ GPU အမည်ကို `|   0  ...` လိုင်းမှ၊ memory ကို `...MiB / ...MiB` ပုံစံမှ
ဖတ်သည်။ Assert များသည် အမည်သည် `NVIDIA` ဖြင့် စခြင်း၊ total သည် 24564 ဖြစ်ခြင်း၊
`free == total - used` ဖြစ်ခြင်းကို စစ်သည်။

## Exercise 2 — fp16 rule of thumb ဖြင့် model fit တွက်ခြင်း

**အဖြေ**

```python
fit = fp16_model_fit(device["free_bytes"])   # free_bytes = 24463278080
```

**Run ရလဒ်**

```
Exercise 2 — fp16_model_fit (fp16 rule of thumb ဖြင့် model အရွယ်အစား တွက်ခြင်း)
  free VRAM            : 24463278080 bytes
  bytes per parameter  : 2 (fp16)
  est. max params      : 12.23B parameters
  lab margin (10%)     : 11.01B parameters
[OK] exercise_2 — fp16 fit ခန့်မှန်းချက် တွက်ချက်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — `23330 MiB = 24463278080` byte ဖြစ်သည်။ fp16 တွင် parameter တစ်ခုလျှင် ၂ byte
ဖြစ်သဖြင့် `24463278080 / 2 = 12231639040` parameter ရသည်။ ဤအရေအတွက်ကို `1e9` ဖြင့် စားပါက
`12.23B` ဖြစ်သည်။ နမူနာ margin ၁၀% ဖြင့် `24463278080 * 0.9 / 2 / 1e9 = 11.01B` ရသည်။
Source ၏ quiz အဖြေနှင့် နှိုင်းယှဉ်ပါက 24 GB ကို 2 ဖြင့် စားသည့် အနီးစပ်ဆုံး တန်ဖိုးသည် `12.0B`
ဖြစ်သည် — ဤ lab သည် အတိအကျ `free` VRAM ကို သုံးသဖြင့် `12.23B` ရသည်။ နှစ်ခုလုံး "အနီးစပ်ဆုံး" ဖြစ်သည်။

## Exercise 3 — CPU matmul ကို run ၍ အချိန်တိုင်းခြင်း

**အဖြေ**

```python
result = benchmark_matmul(64)
```

**Run ရလဒ်**

```
Exercise 3 — benchmark_matmul (pure Python matmul ကို အချိန်တိုင်းခြင်း)
  workload        : 64x64 @ 64x64
  output shape    : 64x64
  checksum        : 583
  multiply ops    : 262144
  elapsed seconds : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဤနေရာတွင် ဂဏန်းအဖြစ် မပြပါ
[OK] exercise_3 — matmul အချိန်တိုင်းတာပြီး နည်းလမ်း နှစ်ခု တိုက်ဆိုင်စစ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — Workload သည် `64x64` matrix နှစ်ခု ဖြစ်သဖြင့် multiply operation
`64 * 64 * 64 = 262144` ရှိသည်။ Checksum (element အားလုံး၏ ပေါင်းလဒ်) သည် `583` ဖြစ်သည်။
`elapsed seconds` သည် စက်၏ အလုပ်ပေါ်မူတည်၍ run တိုင်း အနည်းငယ် ပြောင်းလဲသဖြင့် lab က တိုင်းတာချက်ကို `assert result["seconds"] > 0` ဖြင့်သာ စစ်ပြီး ဂဏန်းအဖြစ် ပုံနှိပ်မထုတ်ပါ။ JupyterLab တွင် `%timeit` ဖြင့် ကိုယ်တိုင် တိုင်းနိုင်သည်။
Assert သည် အရေးကြီးသည့် အချက်ကို စစ်သည် — `matmul_naive` နှင့် `matmul_transposed` ဟူသော
နည်းလမ်း နှစ်ခု၏ ရလဒ်သည် တူရမည်။ ဤစစ်ဆေးချက်သည် timing အပေါ် မမှီခိုသဖြင့်
ရလဒ်သည် deterministic ဖြစ်သည်။

## Exercise 4 — CPU နှင့် GPU speedup လိုင်း တည်ဆောက်ခြင်း

**အဖြေ**

```python
result = speedup_line(cpu_time=8.312, gpu_time=0.041)
```

**Run ရလဒ်**

```
Exercise 4 — speedup_line (supplied timings မှ speedup လိုင်း ဖော်မတ်ချခြင်း)
  CPU matrix multiply: 8.312s
  GPU matrix multiply: 0.041s
  Speedup: 203x
  speedup value   : 202.7317
[OK] exercise_4 — CPU/GPU speedup လိုင်း ဖော်မတ်ချပြီးပါသည်
```

**ရှင်းလင်းချက်** — `8.312 / 0.041 = 202.73170731707316` ဖြစ်သည်။ Source သည် `:.0f` format ကို
သုံးသဖြင့် `203` ဖြစ်သည်။ ထို့ကြောင့် လိုင်းသည် `Speedup: 203x` ဖြစ်သည်။ Source ၏ Build It
နှင့် `code/gpu_check.py` နှစ်ခုလုံးသည် ဤ format ကို သုံးသည်။

## Exercise 5 — local သို့မဟုတ် cloud route ဆုံးဖြတ်ခြင်း

**အဖြေ**

```python
cases = [(False, 0.0, 12.0), (True, 24.0, 12.0), (True, 8.0, 12.0)]
decisions = [cloud_decision(*case) for case in cases]
```

**Run ရလဒ်**

```
Exercise 5 — cloud_decision (availability အချက်အလက်မှ route ဆုံးဖြတ်ခြင်း)
  local_gpu=False, vram=0GB, required=12GB -> cloud
    reason: local NVIDIA GPU မရှိပါ — Google Colab (အခမဲ့ T4) သို့မဟုတ် cloud GPU ကို သုံးရမည်
  local_gpu=True, vram=24GB, required=12GB -> local
    reason: local VRAM 24 GB သည် လိုအပ်သည့် 12 GB ကို ဖုံးလွှမ်းနိုင်သည်
  local_gpu=True, vram=8GB, required=12GB -> cloud
    reason: local VRAM 8 GB သည် လိုအပ်သည့် 12 GB အတွက် မလုံလောက်ပါ — model သည် VRAM ထဲ မဝင်နိုင်ပါ
[OK] exercise_5 — local/cloud route ဆုံးဖြတ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — အခြေအနေ တစ်ခုတွင် GPU မရှိသဖြင့် cloud ဖြစ်သည်။ ဒုတိယ အခြေအနေတွင်
24 GB သည် required 12 GB ထက် ကြီးသဖြင့် local ဖြစ်သည်။ တတိယ အခြေအနေတွင် 8 GB သည်
required 12 GB ထက် ငယ်သဖြင့် cloud ဖြစ်သည်။ Assert သည် `cloud`၊ `local`၊ `cloud` အစဉ်ကို စစ်သည်။

## Exercise 6 — GPU အစီရင်ခံစာ ထုတ်ခြင်း

**အဖြေ**

```python
report = gpu_report(device, fit, decisions[1], bench)
```

**Run ရလဒ်**

```
Exercise 6 — gpu_report (စစ်ဆေးချက် အားလုံး၏ အစီရင်ခံစာ)
  === GPU Report ===
  device            : NVIDIA GeForce RTX 4090
  driver version    : 550.54.14
  vram total/free   : 24564 MiB / 23330 MiB
  fp16 max params   : ~12.23B parameters
  with lab margin   : ~11.01B parameters
  cpu matmul 64x64  : shape 64x64, checksum 583
  route             : local
  recommendation    : local VRAM 24 GB သည် လိုအပ်သည့် 12 GB ကို ဖုံးလွှမ်းနိုင်သည်
  next step         : pip install torch torchvision torchaudio (CUDA build) ကို run ပါ
[OK] exercise_6 — GPU အစီရင်ခံစာ ထုတ်ပြီးပါသည်
```

**ရှင်းလင်းချက်** — အစီရင်ခံစာသည် Exercise 1၊ 2၊ 3 နှင့် 5 ၏ ရလဒ်များကို စုစည်းသည်။
Route သည် `local` ဖြစ်သဖြင့် နောက်တစ်ဆင့်သည် CUDA build ပါသည့် PyTorch install ဖြစ်သည်။
Route သည် `cloud` ဖြစ်ပါက နောက်တစ်ဆင့်လိုင်းသည် Google Colab တွင်
`Runtime > Change runtime type > T4 GPU` ရွေးခြင်းသို့ ပြောင်းသည်။

## Lab အပြည့်အစုံ ၏ နောက်ဆုံးလိုင်း

```
[PASS] All 6/6 exercises passed successfully.
```

Exit code — `0`။
