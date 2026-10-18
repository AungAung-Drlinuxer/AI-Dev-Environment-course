# Module 12 — Debugging & Profiling

> အဆိုးဆုံး AI bug များသည် crash မဖြစ်ပါ။ ၎င်းတို့သည် အမှိုက်အပေါ်တွင် တိတ်ဆိတ်စွာ train လုပ်ပြီး လှပသည့် loss curve ကို တင်ပြသည်။

**Type:** Build · **Languages:** Python · **Time:** ~60 min
**Prerequisites:** Phase 0, Lesson 01 (module 01 — Dev Environment) နှင့် PyTorch အခြေခံ

## ရည်ရွယ်ချက်

ဤ module သည် AI code ၏ **တိတ်ဆိတ်စွာ ကျရှုံးသည့် bug များ** ကို ရှာဖွေသည့်
debugging နှင့် profiling နည်းလမ်းများကို သင်ပေးသည်။ ပြီးဆုံးပါက ဤအရာများကို လုပ်နိုင်ရမည် —

- သတ်မှတ်ချက် ပြည့်မီသည့်အခါသာ ရပ်တန့်သည့် conditional `breakpoint()` နှင့် `debug_print` helper ဖြင့်
  training အလယ်တွင် tensor ၏ shape၊ dtype နှင့် NaN တန်ဖိုးများကို ကြည့်ရှုနိုင်ခြင်း
- `cProfile`၊ `line_profiler` နှင့် `tracemalloc` ဖြင့် training loop ကို profile လုပ်၍ bottleneck ကို ရှာနိုင်ခြင်း
- AI code တွင် အဖြစ်များသည့် bug များကို ဖမ်းနိုင်ခြင်း — shape mismatch၊ NaN loss၊ data leakage နှင့် wrong-device tensor
- TensorBoard ဖြင့် loss curve၊ weight histogram နှင့် gradient distribution ကို ကြည့်ရှုနိုင်ခြင်း

## လိုအပ်ချက် (Prerequisites)

- module 01 ပြီးစီးထားခြင်း (Python 3.11+ နှင့် terminal အခြေခံ)
- Python အခြေခံ — list၊ dict၊ function၊ loop နှင့် `try/except` ကို ဖတ်နိုင်ခြင်း
- PyTorch အခြေခံ အသိရှိခြင်း (tensor၊ forward pass၊ loss၊ gradient) — ဤ module ၏ code များ
  `breakpoint()` နှင့် TensorBoard ကို သရုပ်ပြသည့်အခါ PyTorch ကို သုံးသည်
- GPU သည် **မလိုအပ်ပါ** — ဤ module ၏ `lab.py` သည် standard library သာ သုံးသည့် offline lab ဖြစ်သည်

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. Part 1: Print Debugging (Yes, It Works)
2. Part 2: Python Debugger (pdb and breakpoint)
3. Part 3: Python Logging
4. Part 4: Timing Code Sections
5. Part 5: cProfile and line_profiler
6. Part 6: Memory Profiling
7. Part 7: Common AI Bugs and How to Catch Them
8. Part 8: TensorBoard Basics
9. Part 9: VS Code Debugger

## Exercise များ

| # | Exercise | လုပ်ဆောင်ချက် |
|---|---|---|
| 1 | `debug_print` | nested list ကို tensor အဖြစ် ယူ၍ shape၊ dtype၊ min/max/mean နှင့် NaN ကို ကြည့်သည် |
| 2 | `nan_detector` | သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို တကယ် ဖန်တီး၍ step အလိုက် ဖမ်းသည် |
| 3 | `check_shapes` | matmul shape မတိုက်ဆိုင်ခြင်းကို မြှောက်မီ ကြိုတင် ဖမ်းသည် |
| 4 | `profile_hotspot` | cProfile-style stats ဇယားမှ အချိန်အများဆုံး function ကို ရှာသည် |
| 5 | `memory_hotspot` | tracemalloc-style snapshot မှ အများဆုံး allocate လုပ်သည့် နေရာကို ရှာသည် |
| 6 | `training_health_report` | loss curve ဇယားမှ overfit ဖြစ်/မဖြစ် ဆုံးဖြတ်သည် |

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
python3 modules/12_debugging_and_profiling/lab.py
```

Lab သည် **offline simulation** ဖြစ်သည် — Python standard library သာ သုံးသည်; network၊ GPU၊
torch၊ line_profiler နှင့် TensorBoard မလိုပါ။ Nested list ကို tensor အဖြစ် ကိုယ်စားပြုပြီး
cProfile ၏ stats ဇယား နှင့် tracemalloc ၏ snapshot ကို ဖမ်းယူထားသည့် fixture အဖြစ် ထည့်ထားသည်။
ထို fixture များ၏ တန်ဖိုးကို မိမိ run မှ ကိုယ်တိုင် ရယူရမည်။

## Cautions

- ဤ module ၏ command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
- `line_profiler`၊ `memory_profiler` နှင့် `tensorboard` တို့ကို `pip` ဖြင့် သီးခြား install လုပ်ရသည် —
  version အလိုက် ပြန်စစ်ရန် လိုသည်။
- `breakpoint()` သည် Python 3.7 မှစ၍ built-in function ဖြစ်သည်။ ထို့ကြောင့် `import pdb` မလိုပါ။
- Data leakage စစ်ဆေးခြင်းသည် model ၏ accuracy မြင့်လွန်းသည့်အခါ ပထမဆုံး လုပ်ရမည့် အဆင့် ဖြစ်သည်။
