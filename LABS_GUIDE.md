# LABS_GUIDE — AI Development Environment

ဤ course ၏ lab အားလုံးကို မည်သို့ run စစ်မည်ကို ရှင်းပြသည်။

## အမြန် စတင်ခြင်း

```bash
cd ~/Documents/AI-Dev-Environment-course

# module အားလုံး၏ lab ကို တစ်ကြိမ်တည်း run စစ်ခြင်း
python3 run_all_labs.py

# module တစ်ခုသာ
python3 modules/03_gpu_setup_and_cloud/lab.py
python3 run_all_labs.py --module 03 --verbose
```

လက်ရှိ run ရလဒ် — **၁၃ module / ၇၈ exercise / `[SUCCESS]`** (တစ်စက္ကန့်အောက်)။

## Lab များ၏ အာမခံချက်（Guarantees）

- **Offline** — network၊ API key၊ dataset download မလိုပါ။
- **Standard library သာ** — တတိယပါတီ package တစ်ခုမျှ မလိုပါ။
- **Deterministic** — lab တိုင်း ကို အကြိမ်များစွာ run လျှင် output သည် byte တူညီသည်။ မော်ဒယ်နှင့် မော်ဒယ်သင်တန်း
  ကိန်းဂဏန်းများ (ဥပမာ အချိန်တိုင်းတာမှု) ကို တိုင်းတာသော်လည်း print မထုတ်ပါ — စက်အလိုက် ကွာခြားသဖြင့်
  ဖတ်သူကိုယ်တိုင် တိုင်းရန် ညွှန်ထားသည်။
- **GPU၊ Docker မလို** — သက်ဆိုင်သည့် module များသည် အဆိုပါ စနစ်များ၏ အပြုအမူကို Python ဖြင့် တုပပြီး
  ဆုံးဖြတ်ချက် logic ကို စစ်သည်။

## Exercise တစ်ခုစီသည် မည်သို့ ပြီးစီးကြောင်း ပြသလဲ

Lab တိုင်းတွင် `def exercise_1()` မှ `def exercise_6()` အထိ ရှိပြီး၊ exercise တိုင်းသည်
`assert` ဖြင့် စစ်ဆေးချက်များ ပြီးနောက် `[OK] exercise_N — <အတိုချုပ်>` လိုင်းကို print သည်။
နောက်ဆုံးလိုင်းသည် `[PASS] All 6/6 exercises passed successfully.` ဖြစ်ပြီး exit code သည် 0 ဖြစ်သည်။

## Module တစ်ခုစီ၏ exercise များ

### 01_dev_environment — Dev Environment

1. exercise_1 — tool manifest compared against Python 3.11+ and Node.js 20+
2. exercise_2 — 16 components classified into system, packages, runtimes, AI libraries
3. exercise_3 — required and optional probes listed for beginner, node and rust routes
4. exercise_4 — .env parsed; keys reported as SET, EMPTY or MISSING with values hidden
5. exercise_5 — matmul shape and dtype checked; CPU-only backend confirmed
6. exercise_6 — every probe aggregated; exit code decided as 0

### 02_git_and_collaboration — Git & Collaboration

1. exercise_1 — git config မှ identity ဖတ်ပြီး ပြည့်စုံမှု စစ်ခြင်း
2. exercise_2 — .gitignore တည်ဆောက်ပြီး checkpoint ဖုံးလွှမ်းမှု စစ်ခြင်း
3. exercise_3 — add → commit → push လုပ်ငန်းစဉ် အခြေအနေ ပြခြင်း
4. exercise_4 — branch ဖန်တီး၊ merge နှင့် conflict ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း
5. exercise_5 — git log --oneline ကို parse ပြီး အနှစ်ချုပ် ထုတ်ခြင်း
6. exercise_6 — untracked / modified / staged ခွဲထုတ်ပြီး push အဆင်သင့်မှု ဆုံးဖြတ်ခြင်း

### 03_gpu_setup_and_cloud — GPU Setup & Cloud

1. exercise_1 — nvidia-smi ဇယားမှ device အချက်အလက် ဖတ်ပြီးပါသည်
2. exercise_2 — fp16 fit ခန့်မှန်းချက် တွက်ချက်ပြီးပါသည်
3. exercise_3 — matmul အချိန်တိုင်းတာပြီး နည်းလမ်း နှစ်ခု တိုက်ဆိုင်စစ်ပြီးပါသည်
4. exercise_4 — CPU/GPU speedup လိုင်း ဖော်မတ်ချပြီးပါသည်
5. exercise_5 — local/cloud route ဆုံးဖြတ်ပြီးပါသည်
6. exercise_6 — GPU အစီရင်ခံစာ ထုတ်ပြီးပါသည်

### 04_apis_and_keys — APIs & Keys

1. exercise_1 - .env parsed, key names listed without values
2. exercise_2 - secret masked to a short prefix and suffix
3. exercise_3 - messages payload built as a dict
4. exercise_4 - response text and token usage extracted
5. exercise_5 - 401/403/429/5xx mapped to an action
6. exercise_6 - offline API call simulated and reported

### 05_jupyter_notebooks — Jupyter Notebooks

1. exercise_1 — cell count and types
2. exercise_2 — out-of-order execution detected
3. exercise_3 — hidden state estimated from dependencies
4. exercise_4 — two implementations timed
5. exercise_5 — notebook versus script decided per task
6. exercise_6 — notebook health report

### 06_python_environments — Python Environments

1. exercise_1 - parsed pyproject.toml base deps and 2 optional groups
2. exercise_2 - lockfile pin check found missing and unpinned entries
3. exercise_3 - caught pip/conda mix-up and confirmed env isolation
4. exercise_4 - classified 5 torch/driver CUDA combinations
5. exercise_5 - split conflicting projects into 4 environments
6. exercise_6 - setup report passed all 8 checks

### 07_docker_for_ai — Docker for AI

1. exercise_1 — instruction ၁၃ ခု၊ layer ၁၂ ခု နှင့် base image ကို parse လုပ်ပြီးပါသည်
2. exercise_2 — base image ၄ မျိုး၏ အရွယ်အစားနှင့် tooling ကွာခြားချက်ကို ဇယားဖြင့် ပြပြီးပါသည်
3. exercise_3 — GPU flag၊ volume mount ၃ ခုနှင့် port mapping ပါသော run command ကို တည်ဆောက်ပြီးပါသည်
4. exercise_4 — service စာရင်း၊ depends_on နှင့် QDRANT_URL endpoint ကို parse လုပ်ပြီးပါသည်
5. exercise_5 — ai-dev မှ http://qdrant:6333/collections သို့ ရောက်နိုင်ကြောင်း စစ်ပြီးပါသည်
6. exercise_6 — image ၏ layer၊ package နှင့် port အစီရင်ခံစာကို ထုတ်ပြီးပါသည်

### 08_editor_setup — Editor Setup

1. exercise_1 — settings.json key ၅ ခုကို စစ်ဆေးပြီးပါပြီ
2. exercise_2 — extension စာရင်း ၈ ခုကို နှိုင်းယှဉ်ပြီးပါပြီ
3. exercise_3 — SSH host entry လိုင်း ၅ လိုင်း တည်ဆောက်ပြီးပါပြီ
4. exercise_4 — format-on-save မူဝါဒ 5 မျိုးအတွက် ဆုံးဖြတ်ပြီးပါပြီ
5. exercise_5 — editor ၄ ခုကို လိုအပ်ချက် ၅ မျိုးနှင့် အဆင့်သတ်ပြီးပါပြီ
6. exercise_6 — setup အစီရင်ခံစာ (5/5) ထုတ်ပြီးပါပြီ

### 09_data_management — Data Management

1. exercise_1 - read a CSV file as a list of records
2. exercise_2 - streaming and loading peak memory compared
3. exercise_3 - 70/15/15 split with a fixed seed
4. exercise_4 - CSV/JSON/Parquet/Arrow trade-offs applied
5. exercise_5 - large-file policy applied to weights and data
6. exercise_6 - dataset report printed

### 10_terminal_and_shell — Terminal & Shell

1. exercise_1 - parsed 100 epoch records and 5 level records
2. exercise_2 - grep filtered 106 lines down to 100 loss lines
3. exercise_3 - pipeline of 7 stages wrote 2 files
4. exercise_4 - loss dropped from 2.0596 to 0.0952 (mean tail -10)
5. exercise_5 - built 8-command plan for 3 panes
6. exercise_6 - ops report over 106 lines, 2 errors, 3 warning

### 11_linux_for_ai — Linux for AI

1. exercise_1 — converted 6 modes between symbolic and octal
2. exercise_2 — diagnosed 3 denials and listed 3 fixes
3. exercise_3 — reported 3 file systems and 6 du entries
4. exercise_4 — built a 6-step apt plan for 8 packages
5. exercise_5 — tabulated 8 macOS-to-Linux differences
6. exercise_6 — operations report over 3 denials and 3 file systems

### 12_debugging_and_profiling — Debugging & Profiling

1. exercise_1 — debug_print ဖြင့် shape၊ dtype၊ NaN ကို စစ်ဆေးပြီးပါသည်
2. exercise_2 — စားခြင်းမှ ဖြစ်သော NaN ကို ဖန်တီး၍ ဖမ်းပြီးပါသည်
3. exercise_3 — matmul shape များကို မြှောက်မီ စစ်ဆေးပြီးပါသည်
4. exercise_4 — cProfile-style ဇယားမှ hotspot ကို ခွဲထုတ်ပြီးပါသည်
5. exercise_5 — tracemalloc-style snapshot မှ hotspot ကို ရှာပြီးပါသည်
6. exercise_6 — loss curve မှ overfit ကို ဆုံးဖြတ်ပြီးပါသည်

### 13_python_for_ai_engineering — Python for AI Engineering

1. exercise_1 — Record dataclass and CSV loader
2. exercise_2 — seeded train and test split
3. exercise_3 — mini-batch generator
4. exercise_4 — dot product, mean and standardizer
5. exercise_5 — shared list, mutable default and used-up generator
6. exercise_6 — speed and memory measurement report

## Optional — တကယ့် service များနှင့် လေ့ကျင့်ခြင်း

`docker-compose.yml` သည် module 07 ၏ multi-service stack (AI container + Qdrant vector database) ကို
ဒေသအတွင်း run ရန် ဖြစ်သည်။ Lab များသည် ဤဖိုင် မလိုဘဲ အလုပ်လုပ်သည်။

```bash
docker compose up -d qdrant
docker compose run --rm ai-dev python -c "import torch; print(torch.__version__)"
```

GPU ကို container အတွင်းသုံးလိုပါက host တွင် NVIDIA Container Toolkit လိုအပ်သည်။
Image tag များနှင့် `torch` version များသည် အချိန်နှင့်အမျှ ပြောင်းလဲသဖြင့် run မီ မိမိ driver/CUDA version နှင့်
ကိုက်ညီကြောင်း စစ်ရမည်။

တကယ့် library များ (torch, datasets, jupyterlab, anthropic, numpy) ဖြင့် လေ့ကျင့်လိုပါက
`requirements.txt` တွင် ဖော်ပြထားသည့် package များကို မိမိ virtual environment တွင် install လုပ်ပါ။

## ချို့ယွင်းမှု ဖြေရှင်းခြင်း（Troubleshooting）

| လက္ခဏာ | အကြောင်းရင်း | ဖြေရှင်းနည်း |
|---|---|---|
| `No lab.py found` | မှားသော directory မှ run ခြင်း | repository root မှ `python3 run_all_labs.py` run ပါ |
| Module တစ်ခု `FAIL` | ထို lab ပြင်ဆင်ထား | `python3 modules/<folder>/lab.py` ဖြင့် run ၍ traceback ကို ဖတ်ပါ |
| Python version နိမ့်ခြင်း | ဤ course သည် Python 3.11+ ကို ရည်ရွယ်သည် | `python3 --version` စစ်ပြီး အသစ်သော interpreter သုံးပါ |
| Docker service မစတင်ခြင်း | port 6333 အသုံးပြုနေသည် | `docker compose down` ပြီး ပြန်စပါ |
