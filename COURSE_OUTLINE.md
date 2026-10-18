# Course Outline — AI Development Environment (Phase 00 · Setup & Tooling)

Source — [`rohitg00/ai-engineering-from-scratch`](https://github.com/rohitg00/ai-engineering-from-scratch) ၏
**Phase 00: Setup & Tooling** (lesson ၁၃ ခု၊ MIT)။ အောက်ပါ စာရင်းသည် အသုံးပြုသူ ပေးခဲ့သည့် စာရင်း
(lesson 01–12) နှင့် source တွင် အမှန်တကယ် ရှိသည့် 13 ခုမြောက်
`13-python-for-ai-engineering` ကို ပေါင်းထားသည်။

## သင်ယူသည့် ပန်းတိုင်

1. AI engineering အတွက် ပတ်ဝန်းကျင်ကို **အလွှာ ၄ လွှာ** (system → packages → runtimes → AI libraries) အနေဖြင့် နားလည်ပြီး အစဉ်လိုက် တည်ဆောက်နိုင်ခြင်း
2. Python၊ Node.js၊ Rust toolchain နှင့် virtual environment များကို ထပ်တလဲလဲ တည်ဆောက်နိုင်သည့် (reproducible) အဆင့်တွင် ထားနိုင်ခြင်း
3. GPU ကို စစ်ဆေးခြင်း၊ CPU နှင့် GPU ကို နှိုင်းယှဉ်ခြင်း၊ VRAM အလိုက် မော်ဒယ် အရွယ်ကို ခန့်မှန်းနိုင်ခြင်း
4. API key ကို လုံခြုံစွာ ထိန်းသိမ်းခြင်း၊ SDK နှင့် raw HTTP ကို နှိုင်းယှဉ်၍ debugging လုပ်နိုင်ခြင်း
5. Notebook၊ environment၊ container၊ editor ကို အလုပ်အမျိုးအစားအလိုက် ရွေးချယ်နိုင်ခြင်း
6. Dataset ကို load / stream / cache လုပ်ခြင်း၊ split ကို seed ဖြင့် ထပ်တလဲလဲ ရနိုင်အောင် လုပ်ခြင်း
7. Terminal၊ Linux၊ permission၊ လော့ဂ်စစ်ထုတ်ခြင်း၊ အဝေးမှ machine ကို ချိတ်ဆက်ခြင်း
8. ကျရှုံးမှု မပေးဘဲ မှားယွင်းသည့် ရလဒ် ထုတ်သည့် bug များ (NaN loss၊ shape mismatch၊ data leakage၊ wrong device) ကို ဖမ်းနိုင်ခြင်း
9. Python idioms နှင့် **တိတ်ဆိတ်စွာ မှားသည့် အမှား ၃ မျိုး** (shared list၊ mutable default၊ used-up generator) ကို သိရှိခြင်း

## Lesson စာရင်း

| # | Lesson | အမျိုးအစား | Module folder | Source |
|---|---|---|---|---|
| 01 | Dev Environment | Build · Python, Node.js, Rust · ~45 min | `modules/01_dev_environment/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F01-dev-environment) |
| 02 | Git & Collaboration | Build · ~30 min | `modules/02_git_and_collaboration/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F02-git-and-collaboration) |
| 03 | GPU Setup & Cloud | Build · Python · ~40 min | `modules/03_gpu_setup_and_cloud/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F03-gpu-setup-and-cloud) |
| 04 | APIs & Keys | Build · Python · ~30 min | `modules/04_apis_and_keys/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F04-apis-and-keys) |
| 05 | Jupyter Notebooks | Build · Python · ~30 min | `modules/05_jupyter_notebooks/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F05-jupyter-notebooks) |
| 06 | Python Environments | Build · Python · ~35 min | `modules/06_python_environments/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F06-python-environments) |
| 07 | Docker for AI | Build · Docker · ~60 min | `modules/07_docker_for_ai/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F07-docker-for-ai) |
| 08 | Editor Setup | Build · ~20 min | `modules/08_editor_setup/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F08-editor-setup) |
| 09 | Data Management | Build · Python · ~45 min | `modules/09_data_management/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F09-data-management) |
| 10 | Terminal & Shell | Learn · ~35 min | `modules/10_terminal_and_shell/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F10-terminal-and-shell) |
| 11 | Linux for AI | Learn · ~30 min | `modules/11_linux_for_ai/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F11-linux-for-ai) |
| 12 | Debugging & Profiling | Build · Python · ~45 min | `modules/12_debugging_and_profiling/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F12-debugging-and-profiling) |
| 13 | Python for AI Engineering | Build · Python · ~120 min | `modules/13_python_for_ai_engineering/` | [link](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F13-python-for-ai-engineering) |

### Lesson 13 — source ၏ ဖော်ပြချက်

> Most code in this course uses the same small set of Python idioms. Learn that set here, before the math and model lessons depend on it.

`[Build · Python · ~120 min](https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F13-python-for-ai-engineering)`

## လေ့လာသည့် အစီအစဉ် (၄ ပတ်)

| ပတ် | Module | ပန်းတိုင် |
|---|---|---|
| ပတ် ၁ | 01, 02, 03 | toolchain၊ git၊ GPU — ပတ်ဝန်းကျင် အခြေခံ ပြီးစီးခြင်း |
| ပတ် ၂ | 04, 05, 06 | API key၊ notebook၊ environment — လက်တွေ့ အလုပ်လုပ်နိုင်သည့် အခြေအနေ |
| ပတ် ၃ | 07, 08, 09 | Docker၊ editor၊ data — စီမံကိန်း အလုပ်အတွက် အဆင်သင့် |
| ပတ် ၄ | 10, 11, 12, 13 | terminal၊ Linux၊ debugging၊ Python idioms — ကျွမ်းကျင်မှု အဆင့် |

## Module တိုင်း၏ လေ့လာနည်း

1. `README.md` — ရည်ရွယ်ချက် နှင့် လိုအပ်ချက်
2. `explanation.md` — subtopic တိုင်းကို အစမှ ဖတ်ခြင်း (command တိုင်း၏ လုပ်ဆောင်ချက် အပါအဝင်)
3. `lab.py` run ၍ အရင်စစ်ခြင်း — `python3 modules/<folder>/lab.py`
4. `exercise.md` — ကိုယ်တိုင် လုပ်ခြင်း (အဖြေကို မကြည့်မီ)
5. `solution.md` — အဖြေ နှင့် တကယ့် output နှင့် နှိုင်းယှဉ်ခြင်း
6. self-check မေးခွန်းများကို ဖြေ၍ အခန်း ပြီးစီးကြောင်း အတည်ပြုခြင်း
