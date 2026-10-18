# Module 03 — Exercise

Exercise တိုင်းကို `modules/03_gpu_setup_and_cloud/lab.py` တွင် သက်ဆိုင်ရာ `exercise_N()`
function အဖြစ် implement လုပ်ထားသည်။ `python3 modules/03_gpu_setup_and_cloud/lab.py` ကို run ပါ။
Lab သည် offline ဖြစ်သည် — Python standard library သာ သုံးသည်; network၊ GPU၊ torch မလိုပါ။

## Exercise 1 — nvidia-smi output ကို parse လုပ်ခြင်း

**လိုအပ်ချက်** — ဖမ်းယူထားသည့် `nvidia-smi` ဇယားမှ GPU အမည်၊ total memory နှင့် driver version ကို ဖတ်ရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ `parse_nvidia_smi(text)` ကို ရေးသည်။ `Driver Version:` နောက်ရှိ version ကို regex ဖြင့် ဖတ်သည်။
၂။ `|   0  <GPU အမည်>  ...` ပုံစံ လိုင်းမှ နာမည်ကို ဖတ်သည် (အနည်းဆုံး space ၂ ခုဖြင့် ခွဲထားသည့် အကွက်ကို ယူသည်)။
၃။ `1234MiB / 24564MiB` ပုံစံမှ used နှင့် total ကို ဖတ်ပြီး free = total − used ကို တွက်သည်။
၄။ MiB ကို byte အဖြစ် `1024 * 1024` ဖြင့် ပြောင်းသည် (နောက် exercise များအတွက်)။

**အောင်မြင်မှု စစ်နည်း** — GPU အမည်သည် `NVIDIA` ဖြင့် စရမည်၊ `total_mib` သည် 24564 ဖြစ်ရမည်၊
`free_mib == total_mib - used_mib` ဖြစ်ရမည်။ Output တွင် `[OK] exercise_1` ပေါ်ရမည်။

## Exercise 2 — fp16 rule of thumb ဖြင့် model fit တွက်ခြင်း

**လိုအပ်ချက်** — parameter တစ်ခုလျှင် ၂ byte ဆိုသည့် rule of thumb ဖြင့် အနီးစပ်ဆုံး အနိမ့်ဆုံး model အရွယ်အစားကို တွက်ရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ Exercise 1 မှ `free_bytes` ကို ယူသည်။
၂။ `params = free_bytes / 2` ဖြင့် parameter အရေအတွက်ကို တွက်သည်။
၃။ `params / 1e9` ဖြင့် billion parameters အဖြစ် ပြသည်။
၄။ နမူနာ margin (၁၀%) ဖြင့် လျှော့ထားသည့် တန်ဖိုးကိုလည်း ပြသည် — activation၊ gradient နှင့် CUDA context အတွက် ဖြစ်သည်။

**အောင်မြင်မှု စစ်နည်း** — `bytes_per_parameter == 2` ဖြစ်ရမည်၊ `params_at_2_bytes == free_bytes / 2` ဖြစ်ရမည်၊
24 GB class အတွက် billion parameter အရေအတွက်သည် 10 နှင့် 14 ကြား ရှိရမည်။ Output တွင် `[OK] exercise_2` ပေါ်ရမည်။

## Exercise 3 — CPU matmul ကို run ၍ အချိန်တိုင်းခြင်း

**လိုအပ်ချက်** — CPU matmul ကို pure Python ဖြင့် အတိအကျ တွက်၍ သတ်မှတ် workload အတွက် အချိန်ကို တိုင်းရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ `make_matrix(size)` ဖြင့် deterministic matrix တစ်ခု တည်ဆောက်သည် (`random` မသုံးရ)။
၂။ `matmul_naive(a, b)` ဖြင့် i → p → j အစဉ်အတိုင်း တွက်သည်။
၃။ `time.perf_counter()` ဖြင့် ပတ်လည် အချိန်ကို တိုင်းသည်။
၄။ ရလဒ်၏ checksum (element အားလုံး၏ ပေါင်းလဒ်) နှင့် output shape ကို ပြသည်။
၅။ `matmul_transposed(a, b)` ဟူသော ဒုတိယ လွတ်လပ်သည့် နည်းလမ်းဖြင့် တွက်၍ ရလဒ် နှစ်ခု တူ/မတူ စစ်သည်။

**အောင်မြင်မှု စစ်နည်း** — နည်းလမ်း နှစ်ခု၏ ရလဒ် တူရမည်၊ output shape သည် `64x64` ဖြစ်ရမည်၊
အချိန်သည် သုည ထက် ကြီးရမည်။ Output တွင် `[OK] exercise_3` ပေါ်ရမည်။

## Exercise 4 — CPU နှင့် GPU speedup လိုင်း တည်ဆောက်ခြင်း

**လိုအပ်ချက်** — ပေးထားသည့် CPU နှင့် GPU timing နှစ်ခုမှ speedup ကို တွက်၍ source ၏ format အတိုင်း ဖော်မတ်ချရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ `speedup = cpu_time / gpu_time` ကို တွက်သည်။
၂။ `CPU matrix multiply: {cpu_time:.3f}s`၊ `GPU matrix multiply: {gpu_time:.3f}s` လိုင်း နှစ်လိုင်း ထုတ်သည်။
၃။ `Speedup: {speedup:.0f}x` လိုင်းကို source အတိုင်း ထုတ်သည်။
၄။ လိုင်း သုံးလိုင်းကို စုစည်း၍ ပြသည်။

**အောင်မြင်မှု စစ်နည်း** — `speedup == cpu_time / gpu_time` ဖြစ်ရမည်၊ လိုင်းသည် `x` ဖြင့် ဆုံးရမည်။
Output တွင် `[OK] exercise_4` ပေါ်ရမည်။

## Exercise 5 — local သို့မဟုတ် cloud route ဆုံးဖြတ်ခြင်း

**လိုအပ်ချက်** — local GPU ရှိ/မရှိ နှင့် VRAM ပမာဏအလိုက် `local` သို့မဟုတ် `cloud` route ကို ဆုံးဖြတ်ရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ Input သုံးမျိုးကို စမ်းသည် — GPU မရှိ၊ GPU ရှိပြီး VRAM လုံလောက်၊ GPU ရှိပြီး VRAM မလုံလောက်။
၂။ GPU မရှိပါက `cloud` (Google Colab အခမဲ့ T4) ကို ဆုံးဖြတ်သည်။
၃။ `vram_gb >= required_vram_gb` ဖြစ်ပါက `local`၊ မဟုတ်ပါက `cloud` ကို ဆုံးဖြတ်သည်။
၄။ ဆုံးဖြတ်ချက် တိုင်းအတွက် အကြောင်းပြချက် လိုင်းကို ရေးသည်။

**အောင်မြင်မှု စစ်နည်း** — ရလဒ် သုံးခုသည် `cloud`၊ `local`၊ `cloud` အစဉ်အတိုင်း ဖြစ်ရမည်။
Output တွင် `[OK] exercise_5` ပေါ်ရမည်။

## Exercise 6 — GPU အစီရင်ခံစာ ထုတ်ခြင်း

**လိုအပ်ချက်** — device အချက်အလက်၊ fit ခန့်မှန်းချက် နှင့် အကြံပြုချက်ကို အစီရင်ခံစာ တစ်ခုအဖြစ် စုစည်းရမည်။

**လုပ်ရမည့်အဆင့်**

၁။ Exercise 1၊ 2၊ 3၊ 5 ၏ ရလဒ်များကို input အဖြစ် ယူသည်။
၂။ `=== GPU Report ===` ခေါင်းစဉ်အောက်တွင် device အမည်၊ driver version၊ VRAM total/free၊ fp16 fit၊
   matmul checksum နှင့် route ကို လိုင်းလိုက် ပြသည်။
၃။ Route အလိုက် နောက်တစ်ဆင့် (`pip install torch ...` သို့မဟုတ် Colab T4 ရွေးခြင်း) ကို ထည့်သည်။

**အောင်မြင်မှု စစ်နည်း** — အစီရင်ခံစာတွင် `=== GPU Report ===` ပါရမည်၊ GPU အမည် ပါရမည်၊
route ပါရမည်၊ လိုင်း ၉ လိုင်း အနည်းဆုံး ရှိရမည်။ Output တွင် `[OK] exercise_6` ပေါ်ရမည်။
နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ပေါ်ရမည်။
