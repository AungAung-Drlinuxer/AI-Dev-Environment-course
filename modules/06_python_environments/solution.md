# Solution — Module 06 (Python Environments)

ဤ ဖိုင်ရှိ output အားလုံးသည် တကယ် run ၍ ရရှိသည့် ရလဒ်များ ဖြစ်သည်။ run သည့် command မှာ —

```bash
python3 modules/06_python_environments/lab.py
```

environment —

```
Python 3.14.7
tomllib importable: tomllib
```

Lab တစ်ခုလုံး၏ နောက်ဆုံး လိုင်း —

```
[OK] exercise_6 - setup report passed all 8 checks

[PASS] All 6/6 exercises passed successfully.
```

Exit code —

```
EXIT=0
```

---

## Exercise 1 — `pyproject.toml` ဖတ်ခြင်း

**နည်းလမ်း** — `PYPROJECT_DEMO` စာသားကို `tempfile.TemporaryDirectory()` ထဲရှိ `pyproject.toml` သို့
ရေးပြီး `tomllib.loads()` ဖြင့် parse လုပ်သည်။ `[project]` မှ `name`၊ `version`၊ `requires-python`၊
`dependencies` ကို ဖတ်ပြီး `[project.optional-dependencies]` မှ group များကို ဖတ်သည်။
`split_requirement()` သည် `"numpy>=1.26"` ကဲ့သို့ စာသားကို `("numpy", ">=1.26")` အဖြစ် ခွဲသည် —
ပထမဆုံး package အမည် အက္ခရာ မဟုတ်သည့် character တွင် ဖြတ်သည့် နည်းလမ်း ဖြစ်သည်။ `tomllib` သည်
Python 3.11 မှ စ၍ standard library တွင် ပါသည်။

**တကယ့် output**

```
=== Exercise 1 - parse pyproject.toml ===
file                  : <tmp>/pyproject.toml
project name          : ai-engineering-from-scratch
project version       : 0.1.0
requires-python       : >=3.11
base dependencies     : 4
   - numpy>=1.26            name=numpy
   - matplotlib>=3.8        name=matplotlib
   - jupyter>=1.0           name=jupyter
   - scikit-learn>=1.4      name=scikit-learn
optional groups       : 2
   - llm    -> anthropic>=0.39, openai>=1.50
   - torch  -> torch>=2.3, torchvision>=0.18
extra install commands:
   uv pip install -e ".[llm]"
   uv pip install -e ".[torch]"
[OK] exercise_1 - parsed pyproject.toml base deps and 2 optional groups
```

**အဖြေ** — အခြေခံ dependency ၄ ခုနှင့် optional group ၂ ခု (`torch`၊ `llm`) ရှိသည်။ group တိုင်းကို
`uv pip install -e ".[group]"` ဖြင့် သီးခြား install လုပ်နိုင်သည်။

---

## Exercise 2 — Lockfile ၏ pinned entry များကို စစ်ဆေးခြင်း

**နည်းလမ်း** — `parse_lockfile()` သည် lockfile ကို လိုင်းလိုက် ဖတ်သည်။ `#` ဖြင့် စသည့် လိုင်းနှင့် ကွက်လပ်
လိုင်းများကို ကျော်သည်။ `==` ပါသည့် လိုင်းကို `pinned` dict ထဲ ထည့်ပြီး `==` မပါသည့် လိုင်းကို `unpinned`
စာရင်းထဲ ထည့်သည်။ `check_lockfile()` သည် manifest ၏ အခြေခံ dependency နှင့် optional group အားလုံးမှ
package အမည်များကို စုပြီး pinned dict နှင့် နှိုင်းယှဉ်သည်။ `missing` နှင့် `unpinned` နှစ်ခုလုံး အလွတ်ဖြစ်ပါက
reproducible ဟု ဆုံးဖြတ်သည်။

**တကယ့် output**

```
=== Exercise 2 - check lockfile against the manifest ===
requirements.lock (good)
   pinned entries        : 8
   manifest names        : 8
   missing from lockfile : none
   not in manifest       : none
   unpinned entries      : none
   reproducible          : YES
requirements.lock (bad)
   pinned entries        : 3
   manifest names        : 8
   missing from lockfile : ['matplotlib', 'openai', 'scikit-learn', 'torch', 'torchvision']
   not in manifest       : none
   unpinned entries      : ['matplotlib']
   reproducible          : NO
[OK] exercise_2 - lockfile pin check found missing and unpinned entries
```

**အဖြေ** — `good` lockfile တွင် pinned entry ၈ ခု ရှိသည်၊ manifest ၏ အမည် ၈ ခုလုံးနှင့် ကိုက်ညီသဖြင့်
reproducible = `YES` ဖြစ်သည်။ `bad` lockfile တွင် `matplotlib` သည် version မပါဘဲ ရေးထားသဖြင့် unpinned
ဖြစ်ပြီး `matplotlib`၊ `openai`၊ `scikit-learn`၊ `torch`၊ `torchvision` သည် လုံးဝ မပါသဖြင့် reproducible = `NO`
ဖြစ်သည်။ ဤ lockfile မှ install လုပ်ပါက machine တိုင်းတွင် မတူညီသည့် version များ ရောက်နိုင်သည်။

---

## Exercise 3 — Environment နှစ်ခု၏ package စာရင်း နှိုင်းယှဉ်ခြင်း

**နည်းလမ်း** — environment နှစ်ခု၏ package dict မှ `set` သုံးခု (`only_a`၊ `only_b`၊ `shared`) ကို တွက်သည်။
`shared` အတွင်းရှိ package တိုင်းကို version တူ/မတူ ခွဲသည်။ ထို့နောက် env B ၏ manager သည် `conda` ဖြစ်ပါက
`installers` ဇယားမှ `pip` ဟု မှတ်ထားသည့် package များကို ရှာသည် — ဤအရာသည် conda ၏ dependency
tracking ကို ထိခိုက်သည့် ရောနှောမှု ဖြစ်သည်။

**တကယ့် output**

```
=== Exercise 3 - compare the package sets of two environments ===
environment A         : .venv (manager=uv, 4 packages)
environment B         : myenv (manager=conda, 4 packages)
only in A             : matplotlib, torch, transformers
only in B             : diffusers, pytorch, requests
in both, same version : numpy
in both, different    : none
isolation             : CONFIRMED (each environment holds its own copy)
pip over conda in B   : numpy, requests
verdict               : MIX-UP - conda env B holds pip installs; let conda manage them
[OK] exercise_3 - caught pip/conda mix-up and confirmed env isolation
```

**အဖြေ** — environment နှစ်ခုသည် ကိုယ်ပိုင် package ကို ကိုယ်စီ ထားသဖြင့် isolation သည် CONFIRMED ဖြစ်သည်။
version ကွာသည့် package မရှိသဖြင့် environment နှစ်ခုကြား ပဋိပက္ခ မရှိပါ။ သို့သော် `myenv` ထဲတွင် `numpy`
နှင့် `requests` ကို pip ဖြင့် install လုပ်ထားသဖြင့် verdict သည် MIX-UP ဖြစ်သည်။ ဖြေရှင်းနည်းမှာ ထို package
နှစ်ခုကို conda ဖြင့် ပြန်လည် install လုပ်ခြင်း (`conda install numpy requests`) ဖြစ်သည်။

---

## Exercise 4 — torch CUDA build နှင့် driver တိုက်ဆိုင်မှု ဆုံးဖြတ်ခြင်း

**နည်းလမ်း** — `compare_cuda()` သည် version စာသား နှစ်ခုကို integer tuple အဖြစ် ပြောင်းသည်။
`tuple[0]` (major version) မတူပါက ချက်ချင်း `False` ကို ပြန်သည် — source ဖော်ပြသည့် "CUDA 11.8 builds
don't work with CUDA 12.x drivers (and vice versa)" ဟူသည့် အချက်ကို ဤနေရာတွင် ကိုယ်စားပြုသည်။
major version တူပါက `torch <= driver` ဖြစ်/မဖြစ် စစ်သည် — source ၏ "PyTorch CUDA version must be <=
driver CUDA version" ဟူသည့် စည်းမျဉ်း ဖြစ်သည်။

**တကယ့် output**

```
=== Exercise 4 - torch CUDA build vs driver CUDA version ===
torch CUDA     driver CUDA    verdict  reason
--------------------------------------------------------------------------
12.4           12.4           OK       torch CUDA 12.4 <= driver CUDA 12.4
12.1           12.4           OK       torch CUDA 12.1 <= driver CUDA 12.4
12.4           12.1           FAIL     torch CUDA 12.4 is newer than driver CUDA 12.1
11.8           12.4           FAIL     major version mismatch (torch CUDA 11.8 vs driver CUDA 12.4)
11.8           11.8           OK       torch CUDA 11.8 <= driver CUDA 11.8
command to read the two values:
   nvidia-smi
   python -c "import torch; print(torch.version.cuda)"
mismatching combinations: 2 of 5
   rebuild for: uv pip install torch --index-url <cuda12.1 wheel index>
   rebuild for: uv pip install torch --index-url <cuda12.4 wheel index>
[OK] exercise_4 - classified 5 torch/driver CUDA combinations
```

**အဖြေ** — အတွဲ ၅ ခုအနက် ၂ ခု မကိုက်ညီပါ။ `torch CUDA 12.4` နှင့် `driver CUDA 12.1` အတွဲသည် torch
ပိုင်း ပိုသစ်သဖြင့် မကိုက်ညီပါ။ `11.8` နှင့် `12.4` အတွဲသည် major version မတူသဖြင့် မကိုက်ညီပါ။
ဖြေရှင်းနည်းမှာ driver နှင့် ကိုက်ညီသည့် CUDA build အတွက် PyTorch ကို ပြန်လည် install လုပ်ခြင်း ဖြစ်သည်။
wheel index URL သည် version အလိုက် ပြောင်းလဲနိုင်သဖြင့် run မီ official documentation ကို စစ်ရမည်။

---

## Exercise 5 — Project များကို environment များသို့ ခွဲခြားခြင်း

**နည်းလမ်း** — `plan_environments()` သည် project တိုင်း၏ requirement စာရင်းကို `{package: version_spec}` dict
အဖြစ် ပြောင်းသည်။ requirement set တူညီသည့် project များကို group တစ်ခုတည်းတွင် ထည့်သည်။ requirement
မရှိသည့် project သည် `base (.venv)` group သို့ ဝင်သည်။ `find_conflicts()` သည် package တစ်ခုကို version
ကွာသည့် spec ဖြင့် လိုအပ်သည့် project အတွဲများကို ရှာသည်။

**တကယ့် output**

```
=== Exercise 5 - per-phase environment strategy ===
projects
   phases/00-setup-and-tooling    (no extra dependency)
   phases/04-neural-networks      torch==2.4.0
   phases/05-cnns                 torch==2.4.0
   phases/08-transformers         torch==2.1.0
   phases/11-llm-apis             anthropic>=0.39
plan: 4 environments
   env-1        torch==2.4.0                                         phases/04-neural-networks, phases/05-cnns
   env-2        torch==2.1.0                                         phases/08-transformers
   env-3        anthropic>=0.39                                      phases/11-llm-apis
   base (.venv) shared lightweight base                              phases/00-setup-and-tooling
environments that hold torch: env-1, env-2
conflicts detected
   torch  phases/04-neural-networks needs ==2.4.0 but phases/08-transformers needs ==2.1.0
   torch  phases/05-cnns needs ==2.4.0 but phases/08-transformers needs ==2.1.0
resolution                   : 4 environment groups for 5 projects
[OK] exercise_5 - split conflicting projects into 4 environments
```

**အဖြေ** — phase ၅ ခုအတွက် environment ၄ ခု ရသည်။ phase 04 နှင့် 05 သည် PyTorch environment ကို မျှဝေသည် —
requirement set တူညီသောကြောင့် ဖြစ်သည်။ phase 08 သည် torch 2.1.0 လိုအပ်သဖြင့် ကိုယ်ပိုင် environment ရသည်။
phase 11 သည် torch မလိုအပ်ဘဲ API SDK သာ လိုအပ်သဖြင့် ကိုယ်ပိုင် environment ရသည်။ phase 00 သည်
shared base environment သို့ ဝင်သည်။ ပဋိပက္ခ ၂ ခု (04–08 နှင့် 05–08) ကို ဖမ်းမိပြီး environment ခွဲခြားခြင်းဖြင့်
ဖြေရှင်းထားသည်။

---

## Exercise 6 — Environment setup အစီရင်ခံစာ ထုတ်ခြင်း

**နည်းလမ်း** — exercise 1–5 ၏ function များကို ပြန်လည် ခေါ်ပြီး `(label, ok, detail)` tuple စာရင်း ၈ ခု
တည်ဆောက်သည်။ `ok` မဟုတ်သည့် အရေအတွက်ကို `failures` အဖြစ် ရေတွက်သည်။ `failures == 0` ဖြစ်ပါက
exit code 0 ဖြစ်သည်။

**တကယ့် output**

```
=== Exercise 6 - environment setup report ===
   [PASS] manifest pyproject.toml readable 4 base dependencies
   [PASS] optional groups declared         torch, llm
   [PASS] lockfile pins every name         8 pinned entries
   [PASS] unsafe lockfile detected         1 unpinned, 5 missing
   [PASS] environment isolation            no shared package versions to resolve
   [PASS] pip/conda mix-up scan            2 pip installs in a conda env
   [PASS] torch CUDA build vs driver       torch CUDA 12.1 <= driver CUDA 12.4
   [PASS] environment plan built           4 environments for 5 projects
checks: 8, failures: 0, exit code: 0
[OK] exercise_6 - setup report passed all 8 checks
```

**အဖြေ** — စစ်ဆေးချက် ၈ ခု အားလုံး `PASS` ဖြစ်သဖြင့် exit code 0 ဖြစ်သည်။ အစီရင်ခံစာသည် ဤအချက်
သုံးမျိုးကို တစ်ပြိုင်နက် ပြသည် — manifest ဖတ်နိုင်ခြင်း၊ lockfile သည် ပြန်လည် ဖန်တီးနိုင်မှု ရှိ/မရှိ၊
environment အစီအစဉ် ကိုက်/မကိုက်။ ဤဖွဲ့စည်းပုံကို CI တွင် တိုက်ရိုက် သုံးနိုင်သည် — exit code သည် တကယ့်
အခြေအနေကို ကိုယ်စားပြုသဖြင့် ဖြစ်သည်။

---

## လေ့ကျင့်ခန်း အားလုံး၏ နောက်ဆုံး လိုင်း

```
[PASS] All 6/6 exercises passed successfully.
```
