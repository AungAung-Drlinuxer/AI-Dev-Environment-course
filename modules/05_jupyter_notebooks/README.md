# Module 05 — Jupyter Notebooks

**အမျိုးအစား:** Build · **ဘာသာစကား:** Python · **အချိန်:** ~30 min
**Source lesson:** `phases/00-setup-and-tooling/05-jupyter-notebooks/docs/en.md`
**Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F05-jupyter-notebooks

## ရည်ရွယ်ချက် (Goal)

Notebook သည် AI engineering ၏ လက်တွေ့စမ်းသပ်ခုံ (lab bench) ဖြစ်သည်။ ဤ module ပြီးဆုံးပါက ဖတ်သူသည် —

1. JupyterLab၊ Jupyter Notebook သို့မဟုတ် VS Code ၏ Jupyter extension ကို install လုပ်ပြီး launch လုပ်နိုင်မည်။
2. magic command (`%timeit`၊ `%%time`၊ `%matplotlib inline`) ဖြင့် benchmark လုပ်ခြင်းနှင့် inline ပြသခြင်းကို ပြုလုပ်နိုင်မည်။
3. Notebook နှင့် script ကို မည်သည့်အလုပ်အတွက် သုံးရမည်ကို ခွဲခြားပြီး "explore in notebooks, ship in scripts" လုပ်ငန်းစဉ်ကို ကျင့်သုံးနိုင်မည်။
4. Notebook ၏ trap များဖြစ်သည့် out-of-order execution၊ hidden state နှင့် stale output ကို ဖမ်းဆီးပြီး ဖြေရှင်းနိုင်မည်။

## လိုအပ်ချက် (Prerequisites)

- Phase 0 ၏ Lesson 01 (Dev Environment) — Python ကို install လုပ်ပြီး `python3` ကို command line မှ run နိုင်ခြင်း။
- Terminal (command line) အခြေခံ — directory ပြောင်းခြင်း၊ command run ခြင်း။
- ဤ module ၏ lab အတွက် Python 3 သာ လိုအပ်သည် — Jupyter သို့မဟုတ် တတိယပါတီ package မလိုအပ်ပါ။

> command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။

## Subtopic စာရင်း (Source ၏ အစဉ်အတိုင်း)

| # | Subtopic | အနှစ်ချုပ် |
|---|---|---|
| 1 | Step 1: Pick your interface | JupyterLab / Jupyter Notebook / VS Code + Jupyter extension |
| 2 | Step 2: Keyboard shortcuts that matter | command mode နှင့် edit mode ၏ key များ |
| 3 | Step 3: Cell types | code cell နှင့် markdown cell |
| 4 | Step 4: Magic commands | `%timeit`၊ `%%time`၊ `%matplotlib inline`၊ `!`၊ `%env` |
| 5 | Step 5: Display rich output inline | dataframe ဇယား၊ plot၊ `display(Image(...))` |
| 6 | Step 6: Google Colab | cloud notebook၊ free GPU၊ Drive mount၊ timeout |
| 7 | Notebooks vs Scripts: When to use which | "explore in notebooks, ship in scripts" |
| 8 | Common traps | out-of-order execution၊ hidden state၊ memory leak |
| 9 | Further Reading | JupyterLab Docs၊ Colab FAQ၊ notebook tips |

## Exercise တစ်လိုင်းချင်း

1. **Exercise 1 — Notebook ကို interface တစ်ခုဖြင့် ဖွင့်ပြီး `%timeit` နှိုင်းယှဉ်ခြင်း** — list comprehension နှင့် numpy ကို နှိုင်းယှဉ်သည်။
2. **Exercise 2 — Code cell နှင့် markdown cell ရော၍ Restart & Run All စစ်ခြင်း** — အပေါ်မှ အောက်သို့ အလုပ်လုပ်ကြောင်း အတည်ပြုသည်။
3. **Exercise 3 — `notebook_tips.py` ကို Colab သို့ ကူးထည့်ပြီး GPU ဖြင့် run ခြင်း** — `torch.cuda.is_available()` စစ်သည်။
4. **Exercise 4 — `.ipynb` ကို JSON အဖြစ် ဖတ်၍ cell အရေအတွက်၊ အမျိုးအစား ခွဲခြင်းနှင့် out-of-order ဖမ်းခြင်း** — lab ၏ exercise_1/2 ကို run သည်။
5. **Exercise 5 — Hidden state ကို variable မှီခိုမှုမှ ခန့်မှန်းခြင်းနှင့် `%time`/`%timeit` ကို ရွေးချယ်ခြင်း** — lab ၏ exercise_3/4 ကို run သည်။
6. **Exercise 6 — Notebook နှင့် script ကို အလုပ်အလိုက် ခွဲခြားပြီး ကျန်းမာရေး အစီရင်ခံစာ ထုတ်ခြင်း** — lab ၏ exercise_5/6 ကို run သည်။

## ဖိုင်စာရင်း (File table)

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic စာရင်း၊ exercise နှင့် ဖိုင်စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — problem → concept → comparison → configuration → cautions → self-check |
| `exercise.md` | Exercise ၆ ခု (`## Exercise N — <title>`) |
| `solution.md` | Exercise ၆ ခုစီ၏ အဖြေ နှင့် တကယ့် run ရလဒ် |
| `lab.py` | Standard library သာ သုံး၍ offline run နိုင်သည့် exercise ၆ ခု |

## Lab ကို run ခြင်း

```bash
python3 modules/05_jupyter_notebooks/lab.py
```

Lab သည် မည်သည့် package မှ မလိုအပ်ပါ။ ၎င်းသည် `.ipynb` ဖိုင်ကို ယာယီ directory တွင် ရေးပြီး JSON အဖြစ် ပြန်ဖတ်ကာ cell အမျိုးအစား၊ execution အစဉ်၊ hidden state၊ အချိန်တိုင်းတာချက် နှင့် notebook/script ဆုံးဖြတ်ချက်ကို အစီရင်ခံသည်။
