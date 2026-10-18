# Module 05 — Exercise အဖြေများ

ဤဖိုင်တွင် exercise တိုင်း၏ အဖြေ နှင့် **တကယ် run ၍ ရရှိသည့် output** ကို ဖော်ပြသည်။ Exercise ၄၊ ၅၊ ၆ အတွက် `lab.py` ကို repo root မှ run ၍ ရလဒ်ကို ကူးထည့်ထားသည်။ Exercise ၄၊ ၅၊ ၆ သည် `.ipynb` ကို JSON အဖြစ် ဖတ်သည့်အတွက် Jupyter မလိုဘဲ offline စစ်နိုင်သည်။

## အတူတူ run ခဲ့သည့် command

```bash
python3 modules/05_jupyter_notebooks/lab.py
```

Exit code — `0`။

---

## Exercise 1 — JupyterLab ဖွင့်ပြီး `%timeit` ဖြင့် နှိုင်းယှဉ်ခြင်း

Notebook ထဲတွင် cell နှစ်ခုကို ရေးပြီး run ရသည် —

```python
# cell 1
import numpy as np
%timeit [x ** 2 for x in range(100000)]
```

```python
# cell 2
%timeit np.arange(100000) ** 2
```

`%timeit` သည် စာကြောင်းတိုင်းကို အကြိမ်များစွာ run ပြီး ပျမ်းမျှကို ပြသည်။ Output ပုံစံမှာ `N us +/- M us per loop` ဖြစ်သည်။ ဤတန်ဖိုးသည် machine၊ Python version နှင့် numpy version အလိုက် ပြောင်းလဲသည် — version အလိုက် ပြန်စစ်ရန် လိုသည်။

Offline စစ်နိုင်သည့် အလုပ်တူ နှိုင်းယှဉ်မှု (standard library) ကို `lab.py` ၏ exercise 4 တွင် ပြုလုပ်ထားသည်။ ထို run ၏ တကယ့် output —

```text
=== Exercise 4 — timeit_compare ===
Work: squares of 0..99999
  list comprehension : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဂဏန်းအဖြစ် မပြပါ
  append loop        : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဂဏန်းအဖြစ် မပြပါ
  တိုင်းတာနည်း        : JupyterLab တွင် `%timeit` ဖြင့် ကိုယ်တိုင် တိုင်းပါ
  identical results  : True
```

နည်းလမ်း နှစ်ခုသည် ရလဒ် တူညီကြောင်း (`True`) အတည်ပြုသည်။ အချိန် ကွာခြားချက်သည် ဤစက်တွင် သေးငယ်သည်၊ machine အလိုက် ပြောင်းလဲသည်။

---

## Exercise 2 — Code နှင့် Markdown Cell ရော၍ Restart & Run All စစ်ခြင်း

Notebook ဖွဲ့စည်းပုံ —

1. markdown — `# Sales exploration`
2. code — `import pandas as pd` / `df = pd.read_csv("sales.csv")`
3. code — `df.head()` (နောက်ဆုံး လိုင်း၊ rich table ပေါ်လာသည်)
4. code — `df.plot()` (plot သည် cell အောက်တွင် inline ပေါ်လာသည်)

ထို့နောက် Kernel > Restart & Run All ကို ရွေးသည်။ အောင်မြင်လျှင် cell တိုင်းတွင် counter ပေါ်ပြီး `[1]`၊ `[2]`၊ `[3]`၊ `[4]` အစဉ်လိုက် ဖြစ်သည်၊ error မပေါ်ပါ။ Cell တစ်ခုတွင် `NameError` ပေါ်လျှင် ၎င်းသည် အပေါ်တွင် မဖန်တီးရသေးသည့် variable ကို မှီခိုနေသည် — hidden state ဖြစ်သည်။

---

## Exercise 3 — `notebook_tips.py` ကို Colab GPU ဖြင့် Run ခြင်း

Runtime > Change runtime type > T4 GPU ကို ရွေးပြီး `notebook_tips.py` ၏ code ကို cell အလိုက် ကူးထည့်သည်။

```python
import torch
torch.cuda.is_available()
```

မျှော်မှန်းသည့် output — `True`။ Cell တိုင်း၏ section output —

```text
Notebook Tips - Key Patterns

=== Timing: List vs NumPy ===
List comprehension: ...s
NumPy:              ...s
Speedup:            ...x

=== Inline Plotting ===
Saved plot to notebook_plot.png
In a notebook, plt.show() displays this inline.

=== DataFrame Display ===
...
Best model: Neural Network
Fastest model: Linear Regression

=== Memory Usage ===
Array   1K elements:     0.01 MB
Array 100K elements:     0.80 MB
Array  10M elements:    80.00 MB

=== Magic Command Equivalents ===
...
```

Colab သည် ရပ်နားချိန် ပြည့်လျှင် session ကို ပိတ်သည်၊ ဖိုင်များ မတည်ရှိပါ။ ထို့ကြောင့် ရလဒ်ကို Drive သို့ save လုပ်ရသည် — `from google.colab import drive; drive.mount('/content/drive')`။

---

## Exercise 4 — `.ipynb` ကို JSON အဖြစ် ဖတ်၍ Cell ခွဲခြားခြင်းနှင့် Out-of-order ဖမ်းခြင်း

Sample notebook ကို ကိုယ်တိုင်ရေးသည့် code ဖြင့် scratch directory သို့ ရေးသည်။ တကယ့် ဖိုင် —

```text
PATH       <tmp>/sample.ipynb
SIZE_BYTES 1305
CELLS      7
TYPES      [('markdown', None), ('code', 1), ('code', 3), ('code', 2), ('code', 4), ('markdown', None), ('code', 5)]
```

`lab.py` ၏ exercise 1 နှင့် 2 output —

```text
=== Exercise 1 — read_notebook ===
nbformat: 4.5
Total cells: 7
  code     : 5
  markdown : 2
Code cells: 5
[OK] exercise_1 — cell count and types
=== Exercise 2 — execution_order_check ===
execution_count in file order: [1, 3, 2, 4, 5]
  index 2: execution_count 2 runs after 3 (out of order)
Out-of-order transitions: 1
Verdict: notebook was NOT run top to bottom. Use Kernel > Restart & Run All.
[OK] exercise_2 — out-of-order execution detected
```

အဓိပ္ပာယ် — `.ipynb` သည် JSON ဖြစ်သည်၊ `cells` array ထဲတွင် cell တိုင်း၏ `cell_type`၊ `source`၊ `execution_count` နှင့် `outputs` ပါဝင်သည်။ `execution_count` သည် file အစဉ်အတိုင်း `1, 3, 2, 4, 5` ဖြစ်သည့်အတွက် index 2 တွင် `2` သည် `3` နောက်တွင် run ကြောင်း ပေါ်လာသည် — out-of-order transition တစ်ခု ရှိသည်။

---

## Exercise 5 — Hidden State ခန့်မှန်းခြင်းနှင့် `%time`/`%timeit` ရွေးချယ်ခြင်း

`lab.py` ၏ exercise 3 output —

```text
=== Exercise 3 — hidden_state_scan ===
  code cell 4: uses ['losses', 'plt'] before any cell defines it
Cells at risk after 'Restart & Run All': 1
Verdict: hidden state. A deleted or reordered cell provided these names.
[OK] exercise_3 — hidden state estimated from dependencies
```

Cell 4 (`plt.plot(losses)`) သည် `plt` နှင့် `losses` ကို အသုံးပြုသည်၊ သို့သော် ထို အမည် နှစ်ခုကို အပေါ်ရှိ cell မည်သည့်ဟာမျှ မဖန်တီးပါ။ ထို့ကြောင့် kernel ကို restart ၍ အပေါ်မှ အောက်သို့ run လျှင် ထို cell သည် `NameError` ဖြင့် ကျရှုံးမည် — hidden state ဖြစ်သည်။

`%timeit` နှင့် `%%time` ရွေးချယ်ချက် —

| အလုပ် | Magic | အကြောင်းရင်း |
|---|---|---|
| စာကြောင်းတို microbenchmark | `%timeit` | အကြိမ်များစွာ run ၍ ပျမ်းမျှနှင့် စံလွဲမှု ပေးသည် |
| Training run၊ notebook cell တစ်ခုလုံး | `%%time` | တစ်ကြိမ်သာ run ၍ wall time ပေးသည် |

---

## Exercise 6 — Notebook နှင့် Script ခွဲခြားခြင်းနှင့် ကျန်းမာရေး အစီရင်ခံစာ

`lab.py` ၏ exercise 5 နှင့် 6 output —

```text
=== Exercise 5 — notebook_or_script ===
  code that runs on a schedule -> script
  code with a __main__ guard   -> script
  explain your work            -> notebook
  explore a dataset            -> notebook
  production code              -> script
  prototype a model            -> notebook
  quick experiments            -> notebook
  reusable utilities           -> script
  training pipeline            -> script
  visualize results            -> notebook
Notebook fit: 5   Script fit: 5
Rule: explore in notebooks, ship in scripts.
[OK] exercise_5 — notebook versus script decided per task
=== Exercise 6 — notebook_health_report ===
cells          : 7 (code 5, markdown 2)
execution order: 1 out-of-order transition(s)
hidden state   : 1 cell(s) at risk after restart
overall        : NEEDS FIX (Restart & Run All before sharing)
[OK] exercise_6 — notebook health report
```

နောက်ဆုံး လိုင်း —

```text
[PASS] All 6/6 exercises passed successfully.
```

Notebook တစ်ခုကို မျှဝေမီ စစ်ရမည့် အဆင့် သုံးဆင့် —

1. Kernel > Restart & Run All ကို run ပြီး `execution_count` အစဉ် မှန်/မမှန် စစ်ခြင်း (out-of-order execution)။
2. Cell တိုင်း အသုံးပြုသည့် variable သည် အပေါ်တွင် ဖန်တီးပြီး ဖြစ်/မဖြစ် စစ်ခြင်း (hidden state)။
3. Output တိုင်း လက်ရှိ code နှင့် ကိုက်ညီကြောင်း စစ်ခြင်း (stale output)။
