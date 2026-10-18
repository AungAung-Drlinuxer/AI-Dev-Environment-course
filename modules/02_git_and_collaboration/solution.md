# Module 02 — Git & Collaboration: Solution

ဤဖိုင်ရှိ output အားလုံးသည် `lab.py` ကို တကယ် run ၍ ရသည့် ရလဒ် ဖြစ်သည်။

```bash
python3 modules/02_git_and_collaboration/lab.py
```

မှတ်ချက် — git command အမှန် (`git config`၊ `git add` စသည်) ကို ဤ solution တွင် run ခြင်း မရှိပါ။
ဤ course ၏ lab စည်းမျဉ်းအရ lab သည် offline ဖြစ်ရမည်။ ထို့ကြောင့် git လုပ်ငန်းစဉ်တိုင်းကို
`lab.py` က pure Python ဖြင့် တုပပြီး ထို ရလဒ်ကို ဤနေရာတွင် ဖော်ပြသည်။ Git CLI ကိုယ်တိုင် run
သည့်အခါ ရမည့် output ပုံစံကို command တစ်ခုစီ၏ အောက်တွင် ရေးထားသည်။ git version အလိုက်
output အသေးစိတ် ကွာနိုင်သဖြင့် version အလိုက် ပြန်စစ်ရန် လိုသည်။

---

## Exercise 1 — git identity ကို configure လုပ်ခြင်း

**Command**

```bash
git config --global user.name "Ko Aung"
git config --global user.email "aung@example.com"
git config --global --list
```

**`lab.py` မှ ရသည့် ရလဒ် (parse_git_config) — တကယ် run ရလဒ်**

```
======================================================================
Exercise 1 — parse_git_config — git identity ကို ဖတ်ခြင်း
======================================================================
-- ပြည့်စုံသည့် config --
parse လုပ်ပြီး key အရေအတွက် : 5
  core.editor            = vim
  init.defaultBranch     = main
  pull.rebase            = false
  user.email             = aung@example.com
  user.name              = Ko Aung
  စစ်ဆေးချက် user.name      : ရှိသည်
  စစ်ဆေးချက် user.email     : ရှိသည်
  identity ပြည့်စုံမှု      : True

-- မပြည့်စုံသည့် config --
parse လုပ်ပြီး key အရေအတွက် : 3
  core.editor            = nano
  init.defaultBranch     = main
  user.name              = (အလွတ်)
  စစ်ဆေးချက် user.name      : မရှိပါ
  စစ်ဆေးချက် user.email     : မရှိပါ
  identity ပြည့်စုံမှု      : False
  ပြဿနာ — user.name မရှိပါ
  ပြဿနာ — user.email မရှိပါ

[OK] exercise_1 — git config မှ identity ဖတ်ပြီး ပြည့်စုံမှု စစ်ခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — `git config --global` သည် `~/.gitconfig` ထဲ တန်ဖိုး နှစ်ခု ရေးသည်။
`lab.py` သည် `git config --list` ၏ output ကို `key=value` အလိုက် parse လုပ်သည်။ ပြည့်စုံသည့်
config တွင် `user.name` နှင့် `user.email` နှစ်ခုလုံး ရှိသဖြင့် `identity ပြည့်စုံမှု : True` ဖြစ်သည်။
မပြည့်စုံသည့် config တွင် ပြဿနာ နှစ်ခု ကို စာရင်းချသည်။ Git CLI တွင် `git config --global --list`
သည် `user.name=Ko Aung` နှင့် `user.email=aung@example.com` လိုင်း နှစ်လိုင်း ပြမည်။

---

## Exercise 2 — model checkpoint များကို ချန်လှပ်သည့် `.gitignore` တည်ဆောက်ခြင်း

**`.gitignore` အကြောင်းအရာ**

```
# Model checkpoints — ဤဖိုင်များသည် ကြီးမားသည်၊ ပြန် generate လုပ်နိုင်သည်
*.pt
*.pth
*.safetensors

# Secrets နှင့် ပတ်ဝန်းကျင်
.env
.venv/

# Generated / cache
__pycache__/
data/
wandb/
```

**`lab.py` မှ ရသည့် ရလဒ် (build_gitignore) — တကယ် run ရလဒ်**

```
pattern rule အရေအတွက် : 8

-- စမ်းသပ်သည့် path များ --
  [ignore:*.pt ] models/perceptron.pt
  [ignore:*.safetensors ] checkpoints/llama-3-8b.safetensors
  [ignore:*.pth ] models/old-weights.pth
  [track] src/train.py
  [track] README.md
  [track] requirements.txt
  [ignore:.env ] .env
  [ignore:.venv/ ] .venv/lib/python3.11/site-packages/torch/__init__.py
  [ignore:__pycache__/ ] __pycache__/train.cpython-311.pyc
  [ignore:data/ ] data/train.csv
  [ignore:wandb/ ] wandb/run-20260101/output.log

ignore ဖြစ်သည့် path : 8
track ဖြစ်သည့် path : 3

-- checkpoint extension တိုင်း ဖုံးလွှမ်းမှု --
  *.pt             → models/example.pt            : ignore
  *.pth            → models/example.pth           : ignore
  *.safetensors    → models/example.safetensors   : ignore
[OK] exercise_2 — .gitignore တည်ဆောက်ပြီး checkpoint ဖုံးလွှမ်းမှု စစ်ခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — extension သုံးမျိုးလုံး အတွက် path စမ်းသပ်မှု အောင်မြင်သည်။
`models/perceptron.pt`၊ `checkpoints/llama-3-8b.safetensors` နှင့် `models/old-weights.pth`
သည် ignore ဖြစ်သည်။ `src/train.py`၊ `README.md`၊ `requirements.txt` သည် track ဖြစ်နေဆဲ ဖြစ်သဖြင့်
source code များ တိုက်ရိုက် မထိခိုက်ပါ။ `.env` နှင့် `.venv/` လည်း ဖုံးလွှမ်းသည်။ Git CLI တွင်
ဖိုင်အလွတ်များ ဖန်တီးပြီး `git status` run လျှင် ထို checkpoint ဖိုင်များ untracked list တွင်
မပေါ်ပါ။

---

## Exercise 3 — add → commit → push နေ့စဉ် လုပ်ငန်းစဉ်

**Command**

```bash
git status
git add src/perceptron.py
git commit -m "Add perceptron implementation"
git push origin main
```

**`lab.py` မှ ရသည့် ရလဒ် (commit_workflow) — တကယ် run ရလဒ်**

```
branch : main

  [touch                 ] staged=[] local=0 remote=0 ahead=0
  [git add               ] staged=['src/perceptron.py'] local=0 remote=0 ahead=0
  [git commit            ] staged=[] local=1 remote=0 ahead=1
            → commit hash (ပုံစံစားသာ) : a3f9c21 Add perceptron implement
  [git push              ] staged=[] local=1 remote=1 ahead=0
            → commit 1 ခု origin/main သို့ ရောက်သည်

-- ဒုတိယ အလှည့် — commit နှစ်ခု တစ်ကြိမ်တည်း push --
  [git add               ] staged=['notebooks/02_git.ipynb', 'notes/git.md'] local=1 remote=1 ahead=0
  [git commit            ] staged=[] local=2 remote=1 ahead=1
  [git add               ] staged=['src/trainer.py'] local=2 remote=1 ahead=1
  [git commit            ] staged=[] local=3 remote=1 ahead=2
  push မလုပ်မီ ahead : 2
  [git push              ] staged=[] local=3 remote=3 ahead=0
            → commit 2 ခု origin/main သို့ ရောက်သည်

-- push မလိုသည့် အခြေအနေ --
  [git push (no-op)      ] staged=[] local=3 remote=3 ahead=0
            → push လုပ်ရန် commit မရှိပါ (origin/main up to date)

-- staged မရှိဘဲ commit လုပ်ရန် ကြိုးစားခြင်း --
  [git commit (skip)     ] staged=[] local=3 remote=3 ahead=0
            → staged မရှိသဖြင့် commit မဖြစ်ပါ
[OK] exercise_3 — add → commit → push လုပ်ငန်းစဉ် အခြေအနေ ပြခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — commit တစ်ခုစီသည် `ahead` ကို ၁ တိုးသည်။ `push` ပြီးလျှင် `ahead` ပြန်
သုည ဖြစ်သည် — local နှင့် remote တူညီသည်။ commit နှစ်ခု ရှိလျှင် `push` တစ်ကြိမ်ဖြင့် နှစ်ခုလုံး
ရောက်သည် (`ahead=2` → `0`)။ staged list အလွတ်ဖြစ်နေစဉ် `git commit` လုပ်လျှင် git သည်
"nothing to commit" ဖြင့် ရပ်သည် — ဤ lab တွင် ထို အခြေအနေကို `nothing_to_commit` အဖြစ်
ပြန်သည်။ Git CLI တွင် `git push origin main` ၏ output သည်
`<old>..<new>  main -> main` ကဲ့သို့ ဖြစ်မည်။

---

## Exercise 4 — branch ဖြင့် စမ်းသပ်၍ merge လုပ်ခြင်း

**Command**

```bash
git checkout -b experiment/new-optimizer
# ... ပြင်ဆင်မှု နှင့် commit ...
git checkout main
git merge experiment/new-optimizer
```

**`lab.py` မှ ရသည့် ရလဒ် (branch_experiment) — တကယ် run ရလဒ်**

```
-- အခြေအနေ ၁ — မတူညီသည့် key ကို ပြင်ခြင်း (conflict မဖြစ်) --
  base    : {'optimizer': 'sgd', 'lr': '0.01', 'epochs': '3'}
  branch  : {'optimizer': 'adam', 'lr': '0.01', 'epochs': '3'}
  main    : {'optimizer': 'sgd', 'lr': '0.001', 'epochs': '3'}
  merged  : {'optimizer': 'adam', 'lr': '0.001', 'epochs': '3'}
  status  : clean
  conflict: []

-- အခြေအနေ ၂ — key တူညီသည့် လိုင်းကို နှစ်ဖက် ပြင်ခြင်း (conflict) --
  base    : {'optimizer': 'sgd', 'lr': '0.01', 'epochs': '3'}
  branch  : {'optimizer': 'adam', 'lr': '0.01', 'epochs': '3'}
  main    : {'optimizer': 'rmsprop', 'lr': '0.01', 'epochs': '3'}
  merged  : {'optimizer': 'sgd', 'lr': '0.01', 'epochs': '3'}
  status  : conflict
  conflict: ['optimizer']
  လုပ်ဆောင်ရန် : conflict ဖြစ်သည့် key ကို လူက ရွေး၍ ['optimizer'] ကို ပြင်၊
               ပြီးနောက် `git add` + `git commit` ဖြင့် merge ကို အပြီးသတ်သည်

-- အခြေအနေ ၃ — main မပြောင်းလျှင် fast-forward --
  branch commit ရှိသည် : True
  fast-forward         : True
  merged               : {'optimizer': 'adam', 'lr': '0.01', 'epochs': '3'}
  status               : clean
[OK] exercise_4 — branch ဖန်တီး၊ merge နှင့် conflict ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — အခြေအနေ ၁ တွင် branch က `optimizer` ကို ပြင်၍ main က `lr` ကို ပြင်သဖြင့်
လိုင်း မတူညီပါ။ merge သည် conflict မရှိဘဲ နှစ်ဖက် ပြောင်းလဲမှုကို ပေါင်းသည် —
`{'optimizer': 'adam', 'lr': '0.001', 'epochs': '3'}`။ အခြေအနေ ၂ တွင် နှစ်ဖက်လုံး `optimizer`
ကို ပြင်သဖြင့် git သည် ဆုံးဖြတ်နိုင်ခြင်း မရှိပါ — `conflicts: ['optimizer']` ဖြစ်လာသည်။ ထိုအခါ
`base` တန်ဖိုး (`sgd`) ကို ယာယီထား၍ လူက ရွေးရမည်။ အခြေအနေ ၃ တွင် main ပေါ်၌ commit အသစ်
မရှိသဖြင့် fast-forward ဖြစ်သည် — merge commit မလိုပါ။ Git CLI တွင် `git merge` သည်
conflict ဖြစ်လျှင် `CONFLICT (content): Merge conflict in <file>` ဖြင့် ရပ်မည်။

---

## Exercise 5 — `git log --oneline` ဖြင့် history ဖတ်ခြင်း

**Command**

```bash
git log --oneline
git log --oneline -- phases/00-setup-and-tooling
git show --stat <hash>
```

**`lab.py` မှ ရသည့် ရလဒ် (read_log) — တကယ် run ရလဒ်**

```
-- git log --oneline --
  9f2c1ab Add lesson 13 python for AI engineering
  4d8e730 Add lesson 12 debugging and profiling
  b71a055 Add lesson 11 linux for AI
  c30f914 Fix typo in lesson 06 lockfile section
  7a62dec Add lesson 06 python environments
  1f0b8c2 Initial commit

commit စုစုပေါင်း : 6
အသစ်ဆုံး        : 9f2c1ab Add lesson 13 python for AI engineering
အဟောင်းဆုံး     : 1f0b8c2 Initial commit

-- commit တစ်ခုကို ကြည့်ခြင်း (git show --stat) --
  ရွေးသည့် commit : 9f2c1ab
  `git show --stat 9f2c1ab` ၏ ရလဒ် (ပုံစံစားသာ) :
     9f2c1ab Add lesson 13 python for AI engineering
     1 file changed, 118 insertions(+), 0 deletions(-)

-- path အလိုက် စစ်ထုတ်ခြင်း (git log --oneline -- <path>) --
  စစ်ထုတ်ပြီး commit အရေအတွက် : 5
    9f2c1ab Add lesson 13 python for AI engineering
    4d8e730 Add lesson 12 debugging and profiling
    b71a055 Add lesson 11 linux for AI
    c30f914 Fix typo in lesson 06 lockfile section
    7a62dec Add lesson 06 python environments
[OK] exercise_5 — git log --oneline ကို parse ပြီး အနှစ်ချုပ် ထုတ်ခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — `git log --oneline` သည် commit တစ်ခုလျှင် လိုင်းတစ်လိုင်း ပြသည်။
output ၏ ပထမလိုင်းသည် အသစ်ဆုံး commit ဖြစ်သည်။ `lab.py` ၏ `parse_log` သည် hash နှင့် subject
ကို ခွဲထုတ်သည်။ `summarize_log` သည် စုစုပေါင်း ၆ ခု၊ အသစ်ဆုံး `9f2c1ab`၊ အဟောင်းဆုံး
`1f0b8c2 Initial commit` ကို ပြသည်။ path keyword ဖြင့် စစ်ထုတ်လျှင် lesson အကြောင်းအရာ
commit ၅ ခု ကျန်သည် — `Initial commit` ကျန်ခဲ့သည်။ hash နှင့် `insertions` တန်ဖိုးများသည်
ပုံစံစားသာ ဖြစ်သည်။

---

## Exercise 6 — working tree အစီရင်ခံစာ ထုတ်ခြင်း

**Command**

```bash
git status --short
```

**`lab.py` မှ ရသည့် ရလဒ် (status_report) — တကယ် run ရလဒ်**

```
-- git status --short မှ entry များ --
   M  src/perceptron.py
  A/M notebooks/02_git.ipynb
  A/M notes/git.md
  ??  models/scratch.pt
   M  README.md
  ??  src/trainer.py
  UU  config.yaml

-- အုပ်စုအလိုက် --
  staged     (2) : ['notebooks/02_git.ipynb', 'notes/git.md']
  modified   (2) : ['README.md', 'src/perceptron.py']
  untracked  (2) : ['models/scratch.pt', 'src/trainer.py']
  unmerged   (1) : ['config.yaml']

entry စုစုပေါင်း         : 7
push ရန် အဆင်သင့်       : False
လုပ်ဆောင်ရမည့် အဆင့်    : merge conflict ကို ရှေးဦး ဖြေရှင်းရန် လိုသည်

-- conflict မရှိသည့် အခြေအနေ --
  staged : ['src/perceptron.py']
  ready  : True

-- staged မရှိသည့် အခြေအနေ --
  staged : []
  ready  : False
[OK] exercise_6 — untracked / modified / staged ခွဲထုတ်ပြီး push အဆင်သင့်မှု ဆုံးဖြတ်ခြင်း
```

**အဖြေ ရှင်းလင်းချက်** — entry ၇ ခုကို အုပ်စု ၄ ခု ခွဲထုတ်သည်။ `staged` ရှိသော်လည်း
`unmerged` (`config.yaml`) ရှိနေသဖြင့် `push ရန် အဆင်သင့် : False` ဖြစ်သည်။ လုပ်ဆောင်ရမည့်
အဆင့်မှာ conflict ကို ရှေးဦး ဖြေရှင်းခြင်း ဖြစ်သည်။ conflict မရှိဘဲ staged ရှိလျှင် (`True`) —
`git commit` → `git push` သို့ ဆက်နိုင်သည်။ staged မရှိလျှင် (`False`) — `git add` ဖြင့် ရှေးဦး စရမည်။
`models/scratch.pt` သည် untracked အဖြစ် ပေါ်နေသည် — `.gitignore` ကို အသုံးပြုလျှင် ဤ entry
ပျောက်သွားမည်။

---

## အနှစ်ချုပ်

```
[PASS] All 6/6 exercises passed successfully.
```

`lab.py` ၏ exit code သည် 0 ဖြစ်သည်။ exercise ခြောက်ခုလုံး၏ output ကို အထက်တွင် ဖော်ပြပြီး ဖြစ်သည်။
