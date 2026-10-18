# AI Development Environment — Phase 00 (Setup & Tooling)

AI engineering ကို စတင်ရန် **ပတ်ဝန်းကျင် (environment) ကို တစ်ကြိမ်တည်း မှန်ကန်စွာ တည်ဆောက်ခြင်း** ကို
သင်ပေးသည့် လက်တွေ့ course ဖြစ်သည်။

ဤ course သည် [`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch)
(MIT) ၏ **Phase 00: Setup & Tooling** ရှိ lesson **၁၃ ခု** အတွက် မြန်မာဘာသာ လေ့လာရေး material ဖြစ်သည် —
source ၏ lesson တိုင်းအတွက် `explanation.md`၊ `exercise.md`၊ `solution.md` နှင့် ကိုယ်တိုင် run နိုင်သည့် `lab.py`
တစ်ခု ပါဝင်သည်။

## ဘယ်သူအတွက် ဖြစ်သလဲ

- AI engineering ကို စတင်လိုပြီး ကိုယ်ပိုင် machine တွင် ပတ်ဝန်းကျင် တည်ဆောက်ရန် လိုအပ်သူ
- Python 3.11+၊ Node.js 20+၊ Rust၊ Docker၊ GPU ကို ပထမဆုံး ထိတွေ့သူ
- command တိုင်း၏ လုပ်ဆောင်ချက်ကို ရှင်းလင်းချက်ဖြင့် လိုချင်သူ (command စာရင်း သီးသန့် မဟုတ်ပါ)

## လိုအပ်ချက် (Prerequisites)

- ကိုယ်ပိုင် machine (Linux၊ macOS သို့မဟုတ် WSL2) နှင့် terminal အခြေခံ အသုံးပြုနိုင်ခြင်း
- Python အခြေခံ အသုံးပြုနိုင်ခြင်း (variable၊ function၊ list၊ dict)
- GPU သည် **မလိုအပ်ပါ** — module 03 ပြတ်လျှင် cloud (Google Colab) route ကို လိုက်နိုင်သည်

## Module စာရင်း

| # | Module | Type | Time | Lab |
|---|---|---|---|---|
| 01 | [Dev Environment](modules/01_dev_environment/README.md) | Build | ~45 min | `modules/01_dev_environment/lab.py` |
| 02 | [Git & Collaboration](modules/02_git_and_collaboration/README.md) | Build | ~30 min | `modules/02_git_and_collaboration/lab.py` |
| 03 | [GPU Setup & Cloud](modules/03_gpu_setup_and_cloud/README.md) | Build | ~40 min | `modules/03_gpu_setup_and_cloud/lab.py` |
| 04 | [APIs & Keys](modules/04_apis_and_keys/README.md) | Build | ~30 min | `modules/04_apis_and_keys/lab.py` |
| 05 | [Jupyter Notebooks](modules/05_jupyter_notebooks/README.md) | Build | ~30 min | `modules/05_jupyter_notebooks/lab.py` |
| 06 | [Python Environments](modules/06_python_environments/README.md) | Build | ~35 min | `modules/06_python_environments/lab.py` |
| 07 | [Docker for AI](modules/07_docker_for_ai/README.md) | Build | ~60 min | `modules/07_docker_for_ai/lab.py` |
| 08 | [Editor Setup](modules/08_editor_setup/README.md) | Build | ~20 min | `modules/08_editor_setup/lab.py` |
| 09 | [Data Management](modules/09_data_management/README.md) | Build | ~45 min | `modules/09_data_management/lab.py` |
| 10 | [Terminal & Shell](modules/10_terminal_and_shell/README.md) | Learn | ~35 min | `modules/10_terminal_and_shell/lab.py` |
| 11 | [Linux for AI](modules/11_linux_for_ai/README.md) | Learn | ~30 min | `modules/11_linux_for_ai/lab.py` |
| 12 | [Debugging & Profiling](modules/12_debugging_and_profiling/README.md) | Build | ~45 min | `modules/12_debugging_and_profiling/lab.py` |
| 13 | [Python for AI Engineering](modules/13_python_for_ai_engineering/README.md) | Build | ~120 min | `modules/13_python_for_ai_engineering/lab.py` |

## ဖိုင်တည်ဆောက်ပုံ

```
AI-Dev-Environment-course/
├── README.md                 # ဤဖိုင်
├── COURSE_OUTLINE.md         # သင်ယူသည့် အစီအစဉ် နှင့် လေ့လာနည်း
├── MODULE_SPEC.md            # module တိုင်း၏ မဖြစ်မနေ ပါရမည့် subtopic နှင့် lab exercise ၆ ခု
├── WRITING_RULES.md          # အရေးအသား စည်းမျဉ်း
├── LABS_GUIDE.md             # lab များကို run စစ်နည်း
├── run_all_labs.py           # lab အားလုံး run စစ်သည့် runner
├── docker-compose.yml        # OPTIONAL — module 07 ၏ multi-service stack
├── requirements.txt          # OPTIONAL — lab များအတွက် မလိုအပ်
└── modules/
    ├── 01_dev_environment/
    │   ├── README.md         # module ၏ ရည်ရွယ်ချက်၊ subtopic၊ exercise စာရင်း
    │   ├── explanation.md    # အဓိက သင်ခန်းစာ
    │   ├── exercise.md       # exercise ၆ ခု
    │   ├── solution.md       # အဖြေ ၆ ခု (တကယ် run ရလဒ်နှင့်တကွ)
    │   └── lab.py            # exercise ၆ ခုကို assert ဖြင့် စစ်သည့် ကုဒ်
    └── ... 13
```

## လေ့ကျင့်နည်း

```bash
# ၁။ လက်တွေ့စစ်ခြင်း — module တိုင်း၏ lab ကို run ပါ
python3 run_all_labs.py
python3 run_all_labs.py --module 03 --verbose

# ၂။ သင်ခန်းစာ ဖတ်ခြင်း
#    modules/03_gpu_setup_and_cloud/explanation.md → explanation ဖတ် → exercise.md → ကိုယ်တိုင်လုပ် → solution.md နှင့် နှိုင်းယှဉ်
```

**အရေးကြီး** — ဤ course ၏ lab များသည် **offline နှင့် deterministic** ဖြစ်သည်။ Python standard library သာ သုံးသည်;
network၊ GPU၊ Docker မလိုပါ။ ထို့ကြောင့် class room မရှိဘဲ တစ်ဦးတည်း လေ့လာနိုင်သည်။

## Cautions

- ဤ course တွင် ဖော်ပြထားသည့် command များနှင့် version များသည် **version အလိုက် ပြောင်းလဲနိုင်သည်**။ run မီ
  မိမိ OS နှင့် Python/CUDA version အတွက် official documentation ကို စစ်ပါ။
- API key နှင့် token များကို ဤ repository တွင် လုံးဝ မသိမ်းရ။ `.env` ဖိုင်ကို `.gitignore` တွင် ထည့်ထားသည် —
  key တစ်ကြိမ်မျှ မဖော်ပြရ။
- မော်ဒယ် checkpoint နှင့် dataset ဖိုင်ကြီးများကို git တွင် မထည့်ရ (`*.pt`၊ `*.safetensors`၊ `data/` ကို `.gitignore` တွင် ပါသည်)။

## Source နှင့် ဆက်စပ်မှု

| အချက် | တန်ဖိုး |
|---|---|
| Source repository | https://github.com/rohitg00/ai-engineering-from-scratch |
| Phase folder | `phases/00-setup-and-tooling/` |
| Course site | https://aiengineeringfromscratch.com/ |
| License | MIT |
| Lesson အရေအတွက် | ၁၃ (01–13) |

ဤ course သည် source ၏ lesson များကို **မြန်မာဘာသာ ရှင်းလင်းချက် + ကိုယ်တိုင် run နိုင်သည့် lab** အဖြစ်
ပြန်လည် ရေးသားထားသည်။ Source ၏ မူရင်း lesson link များကို `COURSE_OUTLINE.md` တွင် ဖော်ပြထားသည်။
