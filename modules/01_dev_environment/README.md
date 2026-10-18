# Module 01 — Dev Environment

Source lesson — [`phases/00-setup-and-tooling/01-dev-environment`](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F01-dev-environment)
(`rohitg00/ai-engineering-from-scratch`, MIT)။ Type — Build · Python, Node.js, Rust · ~45 min။

## ရည်ရွယ်ချက်

AI engineering အတွက် ပတ်ဝန်းကျင် တစ်ခုသည် **အလွှာ ၄ လွှာ** (system → packages → runtimes → AI libraries)
ဖြင့် တည်ဆောက်ထားသည်။ ဤ module သည် ထို အလွှာ များကို **အောက်မှ အပေါ်သို့** အစဉ်လိုက် တည်ဆောက်နည်း၊
toolchain တိုင်းကို version ဖြင့် စစ်နည်း၊ မိမိ hardware နှင့် တိုက်ဆိုင်သည့် PyTorch build ကို ရွေးနည်း၊
နှင့် စတင်လိုသည့် route အတွက် လိုအပ်သည့် အရာကိုသာ စစ်သည့် preflight ကို run နည်း ကို သင်ပေးသည်။
နောက်ဆုံးတွင် ပထမဆုံး test tensor operation တစ်ခုကို run ပြီး environment အခြေအနေကို အစီရင်ခံစာ
အဖြစ် ထုတ်နိုင်ရမည်။

## လိုအပ်ချက် (Prerequisites)

- ကိုယ်ပိုင် machine (Linux၊ macOS သို့မဟုတ် Windows + WSL2) နှင့် terminal အခြေခံ အသုံးပြုနိုင်ခြင်း
- Python အခြေခံ (variable၊ function၊ list၊ dict) နှင့် `python3 <file>` run နိုင်ခြင်း
- GPU မလိုအပ်ပါ — Step 6 ရှိ CPU လမ်းကြောင်းကို လိုက်နိုင်သည်
- Lab အတွက် ဘာ install မှ မလိုအပ်ပါ (standard library သာ)

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

| အစဉ် | Subtopic | အကျဉ်းချုပ် |
|---|---|---|
| 1 | Step 1: System Foundation | OS၊ shell၊ git၊ editor နှင့် GPU driver — အလွှာ ၁ |
| 2 | Step 2: Python with uv | `uv` ဖြင့် Python install၊ virtual environment နှင့် package |
| 3 | Step 3: Node.js with pnpm | `fnm` ဖြင့် Node.js install၊ `pnpm` နှင့် `unzip` လိုအပ်ချက် |
| 4 | Step 4: Rust | `rustup` ဖြင့် `rustc` နှင့် `cargo` |
| 5 | Step 5: Julia (Optional) | `juliaup` ဖြင့် Julia — ရွေးချယ်နိုင်သည် |
| 6 | Step 6: GPU Setup (If You Have One) | CUDA ရှိသည့် PyTorch build နှင့် macOS ၏ MPS လမ်းကြောင်း |
| 7 | Step 7: Verify the route you want to start | `verify.py` ၏ route preflight နှင့် next lesson command |

## Exercise တစ်လိုင်းချင်း

| # | Exercise | တစ်လိုင်း ရည်ရွယ်ချက် |
|---|---|---|
| 1 | `check_toolchain` | Tool manifest ကို Python 3.11+၊ Node.js 20+ နှင့် နှိုင်းယှဉ်ပြီး ပြုပြင် command ပြခြင်း |
| 2 | `classify_layer` | Component ၁၆ ခုကို အလွှာ ၄ လွှာ ထဲ ခွဲခြားခြင်း |
| 3 | `verify_route` | `beginner`၊ `node`၊ `rust` route အတွက် required/optional probe စာရင်း ထုတ်ခြင်း |
| 4 | `read_env_file` | `.env` ကို parse လုပ်ပြီး key ရှိ/မရှိကို value မပြဘဲ စစ်ခြင်း |
| 5 | `tensor_probe` | torch ၏ test tensor operation ကို pure Python ဖြင့် တုပြီး shape/dtype စစ်ခြင်း |
| 6 | `setup_report` | စစ်ဆေးချက် အားလုံး စုစည်းပြီး exit code ဆုံးဖြတ်ခြင်း |

Exercise ဖော်ပြချက် အပြည့်အစုံသည် `exercise.md` တွင် ရှိသည်; အဖြေနှင့် တကယ် run ရလဒ်သည်
`solution.md` တွင် ရှိသည်။

## ဖိုင်စာရင်း

| ဖိုင် | အလုပ်တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — အလွှာ ၄ လွှာ၊ Step 1–7၊ သတိပြုချက်၊ self-check |
| `exercise.md` | Exercise ၆ ခု — လိုအပ်ချက်၊ အဆင့်၊ အောင်မြင်မှု စစ်နည်း |
| `solution.md` | Exercise ၆ ခု၏ အဖြေ (တကယ် run ရလဒ်နှင့်တကွ) |
| `lab.py` | Offline lab — `def exercise_1()` မှ `def exercise_6()` အထိ |

## Lab ကို run ခြင်း

```bash
# repository root မှ run ပါ
python3 modules/01_dev_environment/lab.py   # [PASS] All 6/6 exercises passed successfully. -> exit 0
python3 run_all_labs.py --module 01         # course runner မှ အတူတကွ စစ်ခြင်း
```

## အရေးကြီး

command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
ဤ course တွင် ဖော်ပြထားသည့် version အများစု (ဥပမာ `uv python install 3.12`၊ `fnm install 22`၊
`--index-url https://download.pytorch.org/whl/cu124`) သည် **version အလိုက် ပြန်စစ်ရန် လိုသည်**။
API key ကို `.env` ဖိုင်တွင် သိမ်းပြီး output သို့မဟုတ် git တွင် လုံးဝ မဖော်ပြရ။
