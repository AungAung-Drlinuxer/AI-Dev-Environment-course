# Exercise — Module 06 (Python Environments)

ဤ လေ့ကျင့်ခန်း ၆ ခုအတွက် ကုဒ်သည် `lab.py` တွင် `def exercise_1()` မှ `def exercise_6()` အထိ ရှိသည်။
လေ့ကျင့်ခန်း တိုင်းတွင် — လိုအပ်ချက်၊ လုပ်ရမည့် အဆင့်၊ အောင်မြင်မှုကို စစ်သည့် နည်းလမ်း ဟူသည့် အပိုင်း
သုံးပိုင်း ပါသည်။ Lab အားလုံးသည် offline ဖြစ်သည်။ network၊ `pip`၊ `conda` နှင့် environment ဖန်တီးခြင်း
မလိုအပ်ပါ။

**Lab ကို run ခြင်း**

```bash
python3 modules/06_python_environments/lab.py
```

---

## Exercise 1 — `pyproject.toml` ဖတ်ခြင်း

**လိုအပ်ချက်**
`pyproject.toml` တစ်ခုကို parse လုပ်ပြီး အခြေခံ dependency စာရင်း၊ optional dependency group စာရင်း၊
`requires-python` တန်ဖိုးနှင့် group တိုင်းအတွက် install command ကို ထုတ်ပြရမည်။ Standard library ၏
`tomllib` ကို သုံးရမည်။ `pyproject.toml` ဖိုင်ကို `tempfile.TemporaryDirectory()` ထဲတွင် ရေးရမည်။

**လုပ်ရမည့် အဆင့်**
1. `PYPROJECT_DEMO` စာသားကို temporary directory ထဲရှိ `pyproject.toml` သို့ ရေးပါ။
2. `tomllib.loads()` ဖြင့် parse ပြီး `[project]` နှင့် `[project.optional-dependencies]` ကို ဖတ်ပါ။
3. `name`၊ `version`၊ `requires-python` ကို print ပါ။
4. dependency တိုင်းကို package အမည်နှင့်အတူ စာရင်း ဖော်ပြပါ။
5. group တိုင်းအတွက် `uv pip install -e ".[group]"` command ကို ထုတ်ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
အခြေခံ dependency ၄ ခု (`numpy`၊ `matplotlib`၊ `jupyter`၊ `scikit-learn`) နှင့် optional group ၂ ခု
(`torch`၊ `llm`) ကို တွေ့ရမည်။ `lab.py` က `assert` ဖြင့် group အမည်များနှင့် package အမည်များကို စစ်သည်။
နောက်ဆုံးလိုင်းတွင် `[OK] exercise_1 — parsed pyproject.toml base deps and 2 optional groups` ကို တွေ့ရမည်။

---

## Exercise 2 — Lockfile ၏ pinned entry များကို စစ်ဆေးခြင်း

**လိုအပ်ချက်**
lockfile တစ်ခုကို parse လုပ်ပြီး manifest (`pyproject.toml`) ၏ package အမည် တိုင်းအတွက် အတိအကျ
pinned entry ရှိ/မရှိ ဆုံးဖြတ်ရမည်။ Pinned မဟုတ်သည့် entry များနှင့် manifest တွင် မပါသည့် entry များကိုလည်း
ခွဲထုတ် ပြရမည်။ နောက်ဆုံးတွင် lockfile သည် ပြန်လည် ဖန်တီးနိုင်မှု (reproducible) ရှိ/မရှိ ဆုံးဖြတ်ရမည်။

**လုပ်ရမည့် အဆင့်**
1. lockfile ကို လိုင်းလိုက် ဖတ်ပါ။ `#` ဖြင့် စသည့် လိုင်းနှင့် ကွက်လပ် လိုင်းများကို ကျော်ပါ။
2. `name==version` ပုံစံ လိုင်းများကို pinned entry အဖြစ် သိမ်းပါ။ `==` မပါသည့် လိုင်းများကို
   unpinned စာရင်းထဲ ထည့်ပါ။
3. manifest ၏ အခြေခံ dependency နှင့် optional group အားလုံးမှ package အမည်များကို စုပါ။
4. pinned entry မရှိသည့် အမည်များကို `missing` အဖြစ် ခွဲထုတ်ပါ။
5. `good` lockfile နှင့် `bad` lockfile နှစ်ခုကို နှိုင်းယှဉ်၍ ရလဒ်ကို print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
`good` lockfile တွင် pinned entry ၈ ခု ရှိပြီး missing/unpinned မရှိသဖြင့် reproducible = `YES` ဖြစ်သည်။
`bad` lockfile တွင် `matplotlib` unpinned ဖြစ်ပြီး `matplotlib`၊ `openai`၊ `scikit-learn`၊ `torch`၊
`torchvision` သည် missing ဖြစ်သဖြင့် reproducible = `NO` ဖြစ်သည်။ `lab.py` က ဤတန်ဖိုး နှစ်ခုလုံးကို `assert` ဖြင့် စစ်သည်။

---

## Exercise 3 — Environment နှစ်ခု၏ package စာရင်း နှိုင်းယှဉ်ခြင်း

**လိုအပ်ချက်**
Environment နှစ်ခု၏ `{package: version}` စာရင်းကို နှိုင်းယှဉ်ပြီး — A တွင်သာရှိသည့် package၊ B တွင်သာရှိသည့်
package၊ version တူညီသည့် package၊ version ကွာသည့် package ကို ခွဲထုတ်ရမည်။ ထို့အပြင် conda environment
တစ်ခုအတွင်း pip ဖြင့် install လုပ်ထားသည့် package များကို ဖမ်းရမည်။

**လုပ်ရမည့် အဆင့်**
1. `.venv` (manager = `uv`) နှင့် `myenv` (manager = `conda`) ဟူသည့် environment နှစ်ခုကို dict အနေဖြင့် သတ်မှတ်ပါ။
2. `set` လုပ်ဆောင်ချက်များဖြင့် `only_a`၊ `only_b`၊ `shared` ကို တွက်ပါ။
3. `shared` အတွင်း version တူသည့် အုပ်စုနှင့် version ကွာသည့် အုပ်စုကို ခွဲပါ။
4. env B သည် conda ဖြစ်ပါက ၎င်းအတွင်းရှိ pip-installed package များကို စစ်ပါ။
5. ရလဒ်ကို print ပြီး verdict လိုင်း (MIX-UP သို့မဟုတ် CLEAN) ကို ထုတ်ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
`only_a` တွင် `matplotlib`၊ `torch`၊ `transformers` ပါပြီး `only_b` တွင် `diffusers`၊ `pytorch`၊ `requests`
ပါရမည်။ version ကွာသည့် package မရှိသဖြင့် isolation သည် CONFIRMED ဖြစ်သည်။ env B တွင် `numpy` နှင့်
`requests` သည် pip ဖြင့် install လုပ်ထားသဖြင့် verdict သည် MIX-UP ဖြစ်ရမည်။ `lab.py` က ဤတန်ဖိုး အားလုံးကို စစ်သည်။

---

## Exercise 4 — torch CUDA build နှင့် driver တိုက်ဆိုင်မှု ဆုံးဖြတ်ခြင်း

**လိုအပ်ချက်**
(torch CUDA version၊ driver CUDA version) အတွဲ ၅ ခုအတွက် ကိုက်ညီ/မကိုက်ညီ ဆုံးဖြတ်သည့် function
တစ်ခု ရေးရမည်။ စည်းမျဉ်းမှာ — major version မတူပါက မကိုက်ညီဟု သတ်မှတ်သည်။ major version တူပါက
torch ၏ CUDA version သည် driver ၏ CUDA version ထက် မကြီးရပါ။ မကိုက်ညီသည့် အတွဲတိုင်းအတွက်
မည်သည့် လုပ်ဆောင်ချက် လိုသည်ကို ဖော်ပြရမည်။

**လုပ်ရမည့် အဆင့်**
1. version စာသားကို `.` ဖြင့် ခွဲ၍ integer tuple အဖြစ် ပြောင်းပါ။
2. major version (`tuple[0]`) ကို အရင် နှိုင်းယှဉ်ပါ။ မတူပါက `False` ကို ပြန်ပါ။
3. major version တူပါက tuple နှိုင်းယှဉ်ခြင်းဖြင့် `torch <= driver` ဖြစ်/မဖြစ် စစ်ပါ။
4. အတွဲ ၅ ခုကို ဇယား အနေဖြင့် print ပါ — torch CUDA၊ driver CUDA၊ ဆုံးဖြတ်ချက်၊ အကြောင်းရင်း။
5. မကိုက်ညီသည့် အတွဲများအတွက် လိုအပ်သည့် လုပ်ဆောင်ချက်ကို စာရင်း ဖော်ပြပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
`(12.4, 12.4)`၊ `(12.1, 12.4)`၊ `(11.8, 11.8)` သည် OK ဖြစ်ပြီး `(12.4, 12.1)` နှင့် `(11.8, 12.4)` သည်
FAIL ဖြစ်ရမည်။ မကိုက်ညီသည့် အတွဲ အရေအတွက်သည် ၅ ခုအနက် ၂ ခု ဖြစ်ရမည်။

---

## Exercise 5 — Project များကို environment များသို့ ခွဲခြားခြင်း

**လိုအပ်ချက်**
Course ၏ phase ၅ ခုအတွက် လိုအပ်သည့် dependency စာရင်း ရှိသည်။ ဤ project များကို environment အရေအတွက်
အနည်းဆုံးဖြစ်စေသည့် အစီအစဉ်အဖြစ် ခွဲရမည်။ requirement set တူညီသည့် project များသာ environment ကို
မျှဝေသည်။ requirement မရှိသည့် project သည် shared base environment သို့ ဝင်သည်။ ပဋိပက္ခ ဖြစ်သည့်
(ဥပမာ torch version ကွာသည့်) project နှစ်ခုကို environment တစ်ခုတည်းတွင် မထားရ။

**လုပ်ရမည့် အဆင့်**
1. project တိုင်း၏ `requires` စာရင်းကို `{package: version_spec}` dict အဖြစ် ပြောင်းပါ။
2. requirement set တူညီသည့် project များကို group တစ်ခုတည်းတွင် ထည့်ပါ။
3. requirement မရှိသည့် project များကို `base (.venv)` group တွင် ထည့်ပါ။
4. Package တစ်ခုကို version ကွာသည့် spec နှစ်မျိုးဖြင့် လိုအပ်သည့် project အတွဲများကို ရှာ၍
   conflict စာရင်း ထုတ်ပါ။
5. environment တိုင်း၏ အမည်၊ requirement နှင့် project စာရင်းကို print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
environment ၄ ခု ရမည် — `env-1` (`torch==2.4.0`၊ phases 04 နှင့် 05)၊ `env-2` (`torch==2.1.0`၊ phase 08)၊
`env-3` (`anthropic>=0.39`၊ phase 11)၊ `base (.venv)` (phase 00)။ torch conflict ၂ ခု (04 နှင့် 08၊ 05 နှင့် 08)
ကို တွေ့ရမည်။

---

## Exercise 6 — Environment setup အစီရင်ခံစာ ထုတ်ခြင်း

**လိုအပ်ချက်**
အထက်ပါ လေ့ကျင့်ခန်း ၁–၅ ၏ စစ်ဆေးချက်များကို ခေါ်ယူ၍ `PASS`/`FAIL` စာရင်း တစ်ခုအဖြစ် စုစည်းရမည်။
FAIL တစ်ခုမျှ မရှိပါက exit code 0 ကို ဆုံးဖြတ်ရမည်။

**လုပ်ရမည့် အဆင့်**
1. `pyproject.toml` ဖတ်နိုင်/မဖတ်နိုင် နှင့် optional group အရေအတွက်ကို စစ်ပါ။
2. `good` lockfile သည် reproducible ဖြစ်ခြင်းနှင့် `bad` lockfile ကို ဖမ်းမိခြင်းကို စစ်ပါ။
3. Environment isolation နှင့် pip/conda mix-up စစ်ဆေးချက်ကို ထည့်ပါ။
4. torch CUDA စစ်ဆေးချက်နှင့် environment plan အရေအတွက်ကို ထည့်ပါ။
5. `(label, ok, detail)` tuple စာရင်း တစ်ခုအဖြစ် စုစည်း၍ လိုင်းလိုက် print ပါ။
6. `failures` အရေအတွက်မှ exit code ကို တွက်ပြီး print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း**
စစ်ဆေးချက် ၈ ခု အားလုံး `PASS` ဖြစ်ရမည်၊ `failures: 0` နှင့် `exit code: 0` ဖြစ်ရမည်။ Lab တစ်ခုလုံး၏
နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ကို တွေ့ရမည်။

---

## လက်တွေ့ အပိုင်း (optional)

အထက်ပါ လေ့ကျင့်ခန်းများသည် offline ဖြစ်သည်။ မိမိ machine တွင် တကယ် စမ်းလိုပါက ဤ command များကို
run နိုင်သည် (source lesson ၏ `option 1` နှင့် `option 2` အတိုင်း)။

```bash
uv venv
source .venv/bin/activate
which python            # .venv/bin/python ကို ပြရမည်
uv pip install -e ".[torch]"
nvidia-smi
python -c "import torch; print(torch.version.cuda)"
```

`which python` သည် `/usr/bin/python` ကို ပြပါက environment သည် active မဖြစ်သေးပါ — အဆင့် ၂ ကို ပြန်စစ်ပါ။
