# Module 05 — Exercise များ

Exercise ၆ ခု ရှိသည်။ အဖြေကို မကြည့်မီ ကိုယ်တိုင် ပြုလုပ်ရသည်။ Exercise ၄၊ ၅၊ ၆ အတွက် `lab.py` ကို run ၍ အလုပ်လုပ်ကြောင်း စစ်ရသည်။

---

## Exercise 1 — JupyterLab ဖွင့်ပြီး `%timeit` ဖြင့် နှိုင်းယှဉ်ခြင်း

**လိုအပ်ချက်**
- Terminal ရှိခြင်း၊ Python 3 install လုပ်ထားခြင်း။
- Source lesson ၏ Exercise 1 ကို လိုက်နာရသည် — list comprehension နှင့် numpy ကို အလုပ်တူ အရွယ် 100,000 ဖြင့် နှိုင်းယှဉ်ရသည်။

**လုပ်ရမည့် အဆင့်**
1. Terminal ထဲတွင် `pip install jupyterlab` ကို run ပြီး၊ ထို့နောက် `jupyter lab` ကို run ပါ။ Browser တွင် JupyterLab ပေါ်လာသည်။
2. Notebook အသစ် တစ်ခု ဖန်တီးပါ။ Cell တစ်ခုတွင် `%timeit [x ** 2 for x in range(100000)]` ကို ရေးပြီး run ပါ။
3. Cell အသစ် တစ်ခုတွင် `%timeit np.random.randn(100000)` အမျိုးအစား အလုပ်တူ numpy version ကို `import numpy as np` ဖြင့် တွဲ run ပါ။
4. Cell နှစ်ခု၏ ပျမ်းမျှ အချိန်နှင့် စံလွဲမှုကို မှတ်ပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- Cell နှစ်ခုလုံးတွင် `us` သို့မဟုတ် `ms` ယူနစ်ဖြင့် ပျမ်းမျှ အချိန် ပေါ်လာရသည်။
- Cell နှစ်ခုသည် အလုပ်တူ (element အရေအတွက် တူ) ကို တိုင်းကြောင်း သေချာရသည်။ မဟုတ်လျှင် နှိုင်းယှဉ်မှုသည် တရားမမျှတပါ။
- Version အလိုက် ရလဒ် တန်ဖိုး ပြောင်းလဲနိုင်သည် — version အလိုက် ပြန်စစ်ရန် လိုသည်။

---

## Exercise 2 — Code နှင့် Markdown Cell ရော၍ Restart & Run All စစ်ခြင်း

**လိုအပ်ချက်**
- Source lesson ၏ Exercise 2 ကို လိုက်နာရသည် — markdown နှင့် code cell ရော၍ CSV load၊ dataframe ပြသ၊ chart plot။
- `pandas` နှင့် matplotlib install လုပ်ထားခြင်း။

**လုပ်ရမည့် အဆင့်**
1. Notebook အသစ်တွင် ပထမ cell ကို markdown လုပ်ပြီး ခေါင်းစဉ် ရေးပါ။
2. ဒုတိယ cell တွင် `pd.read_csv` ဖြင့် data ဖတ်ပါ။
3. တတိယ cell တွင် dataframe ကို cell၏ နောက်ဆုံး လိုင်းအဖြစ် ထားပါ — rich table ပေါ်လာသည်။
4. စတုတ္ထ cell တွင် `df.plot()` သို့မဟုတ် matplotlib ဖြင့် plot ပါ။
5. Kernel > Restart & Run All ကို ရွေးပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- Restart & Run All ပြီးနောက် cell တိုင်းတွင် execution counter တွင် နံပါတ် ပေါ်ရသည် (`[1]`၊ `[2]` အစဉ်လိုက်)။
- Cell တိုင်းတွင် error မပေါ်ရသည်။
- Cell တစ်ခုတွင် error ပေါ်လျှင် ထို cell သည် အပေါ်မှ variable ကို မှီခိုနေသည် — hidden state ဖြစ်သည်။

---

## Exercise 3 — `notebook_tips.py` ကို Colab GPU ဖြင့် Run ခြင်း

**လိုအပ်ချက်**
- Source ၏ `code/notebook_tips.py` ဖိုင် (lesson extras)။
- Google account (Colab အခမဲ့ tier)။

**လုပ်ရမည့် အဆင့်**
1. https://colab.research.google.com သို့ သွားပါ။
2. Runtime > Change runtime type > T4 GPU (အခမဲ့) ကို ရွေးပါ။
3. `notebook_tips.py` ၏ code ကို cell အလိုက် ကူးထည့်ပါ။
4. Cell အသစ်တွင် `import torch` နှင့် `torch.cuda.is_available()` ကို run ပါ။
5. ဖိုင်ထဲမှ function တိုင်း၏ section ကို run ပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- `torch.cuda.is_available()` သည် `True` ပြန်ရသည်။
- `notebook_tips.py` ၏ function တိုင်း (timing၊ plotting၊ dataframe၊ memory၊ magic equivalents) ၎င်း၏ section ကို print ရသည်။
- Colab session သည် ရပ်နားချိန် ပြည့်လျှင် ဖိုင်များ မတည်ရှိကြောင်း သတိထားရသည် — Drive သို့ save လုပ်ပါ။

---

## Exercise 4 — `.ipynb` ကို JSON အဖြစ် ဖတ်၍ Cell ခွဲခြားခြင်းနှင့် Out-of-order ဖမ်းခြင်း

**လိုအပ်ချက်**
- `lab.py` ကို run နိုင်ခြင်း (standard library သာ)။ Jupyter မလိုအပ်ပါ။

**လုပ်ရမည့် အဆင့်**
1. Repo root မှ `python3 modules/05_jupyter_notebooks/lab.py` ကို run ပါ။
2. Exercise 1 ၏ output တွင် cell စုစုပေါင်း၊ code cell အရေအတွက်နှင့် markdown cell အရေအတွက်ကို ဖတ်ပါ။
3. Exercise 2 ၏ output တွင် `execution_count` စာရင်းနှင့် out-of-order transition အရေအတွက်ကို ဖတ်ပါ။
4. `lab.py` ထဲမှ `build_sample_notebook()` နှင့် `load_notebook()` function ကို ဖတ်၍ `.ipynb` သည် JSON ဖြစ်ကြောင်း အတည်ပြုပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- Exercise 1 သည် `Total cells: 7` နှင့် `code : 5`၊ `markdown : 2` ကို ပြရသည်။
- Exercise 2 သည် `execution_count in file order: [1, 3, 2, 4, 5]` နှင့် `Out-of-order transitions: 1` ကို ပြရသည်။
- Exit code သည် 0 ဖြစ်ရသည်။

---

## Exercise 5 — Hidden State ခန့်မှန်းခြင်းနှင့် `%time`/`%timeit` ရွေးချယ်ခြင်း

**လိုအပ်ချက်**
- Exercise 4 ပြီးစီးထားခြင်း။

**လုပ်ရမည့် အဆင့်**
1. `lab.py` ၏ Exercise 3 output တွင် restart & run all လုပ်လျှင် ကျရှုံးမည့် cell နှင့် ၎င်း အသုံးပြုသည့် variable စာရင်းကို ဖတ်ပါ။
2. Exercise 4 output တွင် list comprehension နှင့် append loop နှစ်မျိုး၏ အချိန်ကို ဖတ်ပါ။
3. Notebook ထဲတွင် microbenchmark အတွက် `%timeit` ကို၊ training run အတွက် `%%time` ကို မည်သည့်အခါ ရွေးရမည်ကို အတိုချုပ် ရေးပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- Exercise 3 သည် `uses ['losses', 'plt'] before any cell defines it` ကို ပြရသည်။
- Exercise 4 သည် `identical results : True` ကို ပြရသည် (နည်းလမ်း နှစ်ခုသည် အလုပ်တူ ဖြစ်ကြောင်း)။
- ရေးထားသည့် ရှင်းလင်းချက်သည် "များစွာ run ၍ ပျမ်းမျှ = `%timeit`" နှင့် "တစ်ကြိမ် = `%%time`" ကို မှန်ကန်စွာ ခွဲခြားရသည်။

---

## Exercise 6 — Notebook နှင့် Script ခွဲခြားခြင်းနှင့် ကျန်းမာရေး အစီရင်ခံစာ

**လိုအပ်ချက်**
- Exercise 4 နှင့် 5 ပြီးစီးထားခြင်း။

**လုပ်ရမည့် အဆင့်**
1. `lab.py` ၏ Exercise 5 output တွင် အလုပ် တစ်ခုချင်းစီအတွက် notebook/script ဆုံးဖြတ်ချက်ကို ဖတ်ပါ။
2. Exercise 6 output တွင် cell အရေအတွက်၊ execution order၊ hidden state နှင့် overall verdict ကို ဖတ်ပါ။
3. Notebook တစ်ခုကို မျှဝေမီ စစ်ရမည့် အဆင့် သုံးဆင့်ကို စာရင်းပြုစုပါ။

**အောင်မြင်မှု စစ်ဆေးနည်း**
- Exercise 5 သည် `Notebook fit: 5` နှင့် `Script fit: 5` ကို ပြရသည်။
- Exercise 6 သည် `overall : NEEDS FIX (Restart & Run All before sharing)` ကို ပြရသည်။
- Lab သည် အဆုံးတွင် `[PASS] All 6/6 exercises passed successfully.` ကို print ရသည်။
