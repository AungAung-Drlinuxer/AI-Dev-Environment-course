# Module 06 — Python Environments

## ရည်ရွယ်ချက် (goal)

ဤ module သည် **AI project တိုင်းအတွက် သီးခြား Python ပတ်ဝန်းကျင် တည်ဆောက်ခြင်း** ကို သင်ပေးသည်။
သင်ပြီးဆုံးသည့်အခါ ဖတ်သူသည် ဤအချက်များကို လုပ်နိုင်ရမည်။

- `uv`၊ `venv` သို့မဟုတ် `conda` ဖြင့် သီးခြား virtual environment ဖန်တီးနိုင်ခြင်း
- optional dependency group ပါသည့် `pyproject.toml` ရေးနိုင်ခြင်း
- ပြန်လည် ဖန်တီးနိုင်မှု (reproducibility) အတွက် lockfile ထုတ်နိုင်ခြင်း
- global install၊ pip နှင့် conda ရောနှောခြင်း၊ CUDA version မကိုက်ညီခြင်း ဟူသည့် အမှား သုံးမျိုးကို
  ရှာဖွေ ပြင်ဆင်နိုင်ခြင်း
- dependency ပဋိပက္ခ ရှိသည့် project များအတွက် per-phase environment strategy ချမှတ်နိုင်ခြင်း

## လိုအပ်ချက် (prerequisites)

- Module 01 (Dev Environment) ပြီးဆုံးထားခြင်း — Python 3.11+ နှင့် `uv` install လုပ်ထားခြင်း
- terminal အခြေခံ အသုံးပြုနိုင်ခြင်း (`cd`၊ environment variable၊ pipe)
- Python အခြေခံ အသုံးပြုနိုင်ခြင်း (module၊ package၊ import အဓိပ္ပာယ် သိခြင်း)
- GPU သည် **မလိုအပ်ပါ** — CUDA အခန်းများသည် version နှိုင်းယှဉ်ခြင်း သဘောတရားသာ ဖြစ်သည်

**သတိ** — command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
ဤ module တွင် ဖော်ပြသည့် package version များသည် source lesson ၏ ဥပမာ တန်ဖိုးများ ဖြစ်သည်။ မိမိ machine
အတွက် တကယ့် version ကို ချိန်ညှိရန် လိုအပ်သည့်အခါ "version အလိုက် ပြန်စစ်ရန် လိုသည်" ဟု မှတ်ထားသည်။

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. Option 1: `uv venv` (Recommended)
2. Option 2: `venv` (Built-in)
3. Option 3: `conda` (When You Need It)
4. For This Course: Per-Phase Strategy
5. `pyproject.toml` Basics
6. Lockfiles
7. Common Mistakes
8. 1. Installing globally
9. 2. Mixing pip and conda
10. 3. Forgetting to activate
11. 4. Committing `.venv` to git
12. 5. CUDA version mismatch

## Lab exercise ၆ ခု (တစ်လိုင်းစီ)

| # | Exercise | အတိုချုပ် |
|---|---|---|
| 1 | `parse_pyproject` | `pyproject.toml` မှ အခြေခံ dependency နှင့် optional group များကို ဖတ်ခြင်း |
| 2 | `check_lockfile` | lockfile ရှိ pinned version များသည် manifest နှင့် ပြည့်စုံ/မပြည့်စုံ စစ်ခြင်း |
| 3 | `env_isolation_check` | environment နှစ်ခု၏ package စာရင်းကို နှိုင်းယှဉ်ပြီး pip/conda ရောနှောမှုကို ဖမ်းခြင်း |
| 4 | `torch_cuda_matrix` | torch ၏ CUDA build နှင့် driver CUDA version တိုက်ဆိုင်မှုကို ဆုံးဖြတ်ခြင်း |
| 5 | `phase_env_strategy` | ဆန့်ကျင်ဘက် dependency ရှိသည့် project များကို environment များသို့ ခွဲခြားခြင်း |
| 6 | `env_setup_report` | အထက်ပါ စစ်ဆေးချက် အားလုံး၏ အစီရင်ခံစာ နှင့် exit code ဆုံးဖြတ်ခြင်း |

Lab ကို run ခြင်း —

```bash
python3 modules/06_python_environments/lab.py
```

Lab သည် **offline နှင့် deterministic** ဖြစ်သည်။ Python standard library သာ သုံးသည်။ network၊ `pip`၊
`conda`၊ environment ဖန်တီးခြင်း မလိုအပ်ပါ။ exercise တိုင်းသည် ကိုယ်ပိုင် ရလဒ်ကို လူဖတ်နိုင်သည့် လိုင်းများဖြင့်
ပြပြီး နောက်ဆုံးတွင် `[PASS] All 6/6 exercises passed successfully.` ကို print ၍ exit code 0 ဖြင့် ပြီးသည်။

## ဖိုင် စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic စာရင်း၊ exercise စာရင်း၊ ဖိုင် စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — ပြဿနာ၊ သဘောတရား၊ နည်းလမ်း နှိုင်းယှဉ်ချက်၊ လက်တွေ့ command၊ သတိထားရမည့် အချက်၊ self-check |
| `exercise.md` | လေ့ကျင့်ခန်း ၆ ခု — လိုအပ်ချက်၊ အဆင့်၊ အောင်မြင်မှု စစ်ဆေးနည်း |
| `solution.md` | လေ့ကျင့်ခန်း ၆ ခု၏ အဖြေ နှင့် တကယ် run ရလဒ် |
| `lab.py` | လေ့ကျင့်ခန်း ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် ကုဒ် |

## ဆက်စပ် ဖတ်ရန်

- Source lesson — <https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F06-python-environments>
- သဘောတရား အသေးစိတ် — `explanation.md`
- လေ့ကျင့်ခန်း — `exercise.md` → ကိုယ်တိုင် လုပ်ပြီး `solution.md` နှင့် နှိုင်းယှဉ်ပါ
