# Module 03 — GPU Setup & Cloud

> Training on CPU is fine for learning. Training for real needs a GPU.

**Type:** Build · **Languages:** Python · **Time:** ~40 min
**Prerequisites:** Phase 0, Lesson 01 (module 01 — Dev Environment)

## ရည်ရွယ်ချက်

ဤ module သည် AI training အတွက် GPU ကို **ရှာဖွေစစ်ဆေးခြင်း၊ ရွေးချယ်ခြင်း နှင့် တိုင်းတာခြင်း**
ကို သင်ပေးသည်။ ပြီးဆုံးပါက ဤအရာများကို လုပ်နိုင်ရမည် —

- `nvidia-smi` နှင့် PyTorch ၏ CUDA API ဖြင့် local GPU အခြေအနေကို စစ်ဆေးနိုင်ခြင်း
- Google Colab တွင် အခမဲ့ T4 GPU ကို ဖွင့်ပြီး cloud မှ experiment run နိုင်ခြင်း
- CPU နှင့် GPU ပေါ်တွင် matrix multiplication ကို နှိုင်းယှဉ်ပြီး speedup ကို တိုင်းတာနိုင်ခြင်း
- fp16 rule of thumb (parameter တစ်ခုလျှင် ၂ byte) ဖြင့် VRAM ထဲ ဝင်နိုင်သည့် အနိမ့်ဆုံး model အရွယ်အစားကို ခန့်မှန်းနိုင်ခြင်း

## လိုအပ်ချက် (Prerequisites)

- module 01 ပြီးစီးထားခြင်း (Python 3.11+ နှင့် terminal အခြေခံ)
- Python အခြေခံ — list၊ function၊ loop ကို ဖတ်နိုင်ခြင်း
- GPU သည် **မလိုအပ်ပါ** — GPU မရှိပါက Option 2 (Google Colab) route ကို လိုက်နိုင်သည်

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. Option 1: Local NVIDIA GPU
2. Option 2: Google Colab
3. Option 3: Cloud GPU
4. No GPU? No problem.
5. Build It: GPU vs CPU benchmark

## Exercise များ

| # | Exercise | လုပ်ဆောင်ချက် |
|---|---|---|
| 1 | nvidia-smi output ကို parse လုပ်ခြင်း | ဖမ်းယူထားသည့် ဇယားမှ GPU အမည်၊ total memory၊ driver version ကို ဖတ်သည် |
| 2 | fp16 rule of thumb | free VRAM မှ parameter အရေအတွက် အနီးစပ်ဆုံးကို တွက်သည် |
| 3 | CPU matmul အချိန်တိုင်းခြင်း | pure Python ဖြင့် သတ်မှတ် workload ကို တွက်၍ အချိန်တိုင်းသည် |
| 4 | speedup လိုင်း တည်ဆောက်ခြင်း | CPU/GPU timing နှစ်ခုမှ `Speedup: Nx` လိုင်းကို ဖော်မတ်ချသည် |
| 5 | local / cloud route ဆုံးဖြတ်ခြင်း | GPU ရှိ/မရှိ နှင့် VRAM ပမာဏအလိုက် route ကို ဆုံးဖြတ်သည် |
| 6 | GPU အစီရင်ခံစာ | device အချက်အလက်၊ fit ခန့်မှန်းချက် နှင့် အကြံပြုချက်ကို စုစည်းသည် |

## ဖိုင်စာရင်း

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ (problem → concept → နှိုင်းယှဉ်ချက် → configuration → cautions → self-check) |
| `exercise.md` | exercise ၆ ခု၏ လိုအပ်ချက်၊ အဆင့် နှင့် စစ်ဆေးနည်း |
| `solution.md` | အဖြေ ၆ ခု (run ရလဒ် အမှန်နှင့်တကွ) |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## Lab run နည်း

```bash
python3 modules/03_gpu_setup_and_cloud/lab.py
```

Lab သည် **offline simulation** ဖြစ်သည် — Python standard library သာ သုံးသည်၊ network၊ GPU၊ torch မလိုပါ။
nvidia-smi ဇယားသည် ဖမ်းယူထားသည့် နမူနာ fixture ဖြစ်သည်; မိမိ machine ၏ အမှန်တန်ဖိုးကို `nvidia-smi` ကို
ကိုယ်တိုင် run ၍ ရယူရမည်။

## Cautions

- ဤ module ၏ command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
- CUDA၊ driver နှင့် PyTorch build သည် တစ်ခုနှင့် တစ်ခု တိုက်ဆိုင်ရမည် — version အလိုက် ပြန်စစ်ရန် လိုသည်။
- Cloud GPU ကို အသုံးပြုပါက instance ကို **မမေ့ပိတ်ရ** — အချိန်အလိုက် ကုန်ကျစရိတ် တက်သည်။
