# Module 02 — Git & Collaboration: Exercise ၆ ခု

ဤ exercise များသည် `explanation.md` ဖတ်ပြီးနောက် လုပ်ရမည့် လက်တွေ့ လုပ်ငန်းများ ဖြစ်သည်။
Exercise ၁–၃ သည် git command အမှန် လိုအပ်သည်။ Exercise ၄–၆ ကို `lab.py` ဖြင့် offline
စစ်ဆေးနိုင်သည်။

```bash
python3 modules/02_git_and_collaboration/lab.py
```

---

## Exercise 1 — git identity ကို configure လုပ်ခြင်း

**လိုအပ်ချက်** — git commit တိုင်းတွင် မှန်ကန်သည့် အမည်နှင့် email ပါရမည်။ ကိုယ်ပိုင် machine တွင်
identity ကို တစ်ကြိမ်တည်း သတ်မှတ်ပြီး ပြန်ဖတ်စစ်ရမည်။

**လုပ်ရမည့် အဆင့်**

1. `git config --global user.name "Your Name"` ကို run ပါ။ `"Your Name"` ကို မိမိ၏ အမည်အမှန် ဖြင့် အစားထိုးပါ။
2. `git config --global user.email "you@example.com"` ကို run ပါ။
3. `git config --global --list` ကို run ပါ။
4. output မှ `user.name` နှင့် `user.email` ၏ တန်ဖိုးကို ဖတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — `git config --global user.name` သည် မိမိရေးထည့်သည့် အမည်ကို ပြန်ပြရမည်။
`--list` ၏ output တွင် `user.name=` နှင့် `user.email=` လိုင်း နှစ်လိုင်း ပါရမည်။ email တွင် `@`
နှင့် နောက်ဆုံး domain တွင် `.` ပါရမည်။ `user.name` သို့မဟုတ် `user.email` ပျောက်နေလျှင် commit
လုပ်သည့်အခါ git သည် အမည်တောင်းလာမည်။

---

## Exercise 2 — model checkpoint များကို ချန်လှပ်သည့် `.gitignore` တည်ဆောက်ခြင်း

**လိုအပ်ချက်** — repo root တွင် `.gitignore` တစ်ခု ဖန်တီးပြီး model checkpoint ဖိုင်များ
(`.pt`၊ `.pth`၊ `.safetensors`) ကို ချန်လှပ်ရမည်။ ထိုနောက် `git status` ဖြင့် ထို ဖိုင်များ
untracked list တွင် မပေါ်ခြင်းကို စစ်ရမည်။

**လုပ်ရမည့် အဆင့်**

1. repo root တွင် `.gitignore` ဖိုင် ဖန်တီးပါ။
2. extension တစ်ခုလျှင် pattern တစ်လိုင်း ရေးပါ — `*.pt`၊ `*.pth`၊ `*.safetensors`။
3. `.env`၊ `.venv/`၊ `__pycache__/`၊ `data/` ကို ထပ်ထည့်ပါ။
4. `touch model.pt weights.pth model.safetensors` ဖြင့် extension တစ်ခုစီအတွက် ဖိုင်အလွတ် ဖန်တီးပါ။
5. `git status` ကို run ပါ။

**အောင်မြင်မှု စစ်နည်း** — `git status` ၏ untracked list တွင် `model.pt`၊ `weights.pth`၊
`model.safetensors` တို့ **မပါရပါ**။ `.gitignore` ဖိုင် ကိုယ်တိုင်မှာမူ untracked အဖြစ် ပါလာမည်။
ဖိုင်တစ်ခု ပေါ်နေလျှင် ထို extension အတွက် pattern မှန်မမှန် ပြန်စစ်ပါ။

---

## Exercise 3 — add → commit → push နေ့စဉ် လုပ်ငန်းစဉ်

**လိုအပ်ချက်** — ဖိုင်တစ်ခု ဖန်တီး၊ commit လုပ်၊ remote သို့ push လုပ်သည့် အစီအစဉ်ကို အပြည့်
လုပ်ပြရမည်။ commit တစ်ခုလျှင် အလုပ်တစ်ခု သာ ပါရမည်။

**လုပ်ရမည့် အဆင့်**

1. `git status` ကို run ၍ မူလအခြေအနေ ကို မှတ်ပါ။
2. `echo "# Notes" > notes/git.md` ကဲ့သို့ ဖိုင်တစ်ခု ဖန်တီးပါ (folder လိုအပ်လျှင် `mkdir -p` ဖြင့် ရှေးဦး ဖန်တီးပါ)။
3. `git add notes/git.md` ကို run ပါ။
4. `git status` ကို ပြန် run ၍ ဖိုင်သည် "Changes to be committed" အောက်သို့ ရောက်ခြင်းကို စစ်ပါ။
5. `git commit -m "Add git lesson notes"` ကို run ပါ။
6. `git push origin main` ကို run ပါ (branch အမည်သည် မိမိ repo အလိုက် ကွာနိုင်သည်)။

**အောင်မြင်မှု စစ်နည်း** — step 6 ၏ output တွင် `main -> main` ကဲ့သို့ လိုင်း ပါရမည်။
ထိုနောက် `git status` သည် "nothing to commit, working tree clean" နှင့်
"Your branch is up to date with 'origin/main'" ကို ပြရမည်။ push reject ဖြစ်လျှင် `git pull`
လုပ်ပြီး ထပ် push လုပ်ပါ။

---

## Exercise 4 — branch ဖြင့် စမ်းသပ်၍ merge လုပ်ခြင်း

**လိုအပ်ချက်** — `main` ကို မထိဘဲ branch တစ်ခုတွင် ပြင်ဆင်ပြီး အောင်မြင်မှသာ merge လုပ်ရမည်။
conflict ဖြစ်သည့် အခြေအနေကိုလည်း ဖန်တီး၍ ဖြေရှင်းနိုင်ရမည်။

**လုပ်ရမည့် အဆင့်**

1. `git checkout -b experiment/new-optimizer` ကို run ပါ။
2. `git status` တွင် `On branch experiment/new-optimizer` ပြခြင်းကို စစ်ပါ။
3. ဖိုင်တစ်ခုကို ပြင်ပြီး `git add` + `git commit -m "Try adam optimizer"` လုပ်ပါ။
4. `git checkout main` ဖြင့် ပြန်ရွှေ့ပါ။
5. `git merge experiment/new-optimizer` ကို run ပါ။
6. conflict ဖြစ်လျှင် marker (`<<<<<<<`၊ `=======`၊ `>>>>>>>`) ကို ဖြေရှင်း၍ `git add` + `git commit` လုပ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — `git log --oneline --graph` တွင် branch လမ်းကြောင်း နှစ်လမ်း နှင့်
merge commit ပေါ်လာရမည်။ conflict ဖြစ်ခဲ့လျှင် marker အားလုံး ပျောက်ရမည် —
`grep -r "<<<<<<<" .` ဖြင့် စစ်နိုင်သည်။ `git status` သည် clean ဖြစ်ရမည်။

---

## Exercise 5 — `git log --oneline` ဖြင့် history ဖတ်ခြင်း

**လိုအပ်ချက်** — repo ၏ history ကို parse လုပ်နိုင်ရမည်။ commit တစ်ခုချင်း၏ hash နှင့် message ကို
စာရင်းချ၍ အသစ်ဆုံး၊ အဟောင်းဆုံး နှင့် path တစ်ခုကို ထိသည့် commit များကို ခွဲထုတ်နိုင်ရမည်။

**လုပ်ရမည့် အဆင့်**

1. `git log --oneline` ကို run ၍ output ကို ဖတ်ပါ။
2. `git log --oneline -- phases/00-setup-and-tooling` ဖြင့် ထို phase ကို ထိသည့် commit များကို စစ်ထုတ်ပါ။
3. commit တစ်ခု ရွေး၍ `git show --stat <hash>` ကို run ပါ။
4. `lab.py` ၏ `read_log` (Exercise 5) ကို run ၍ log စာသားကို parse လုပ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — parse လုပ်ပြီး commit စုစုပေါင်း သည် `git log --oneline` ၏ လိုင်းအရေအတွက်
နှင့် တူရမည်။ `git show --stat` ၏ output တွင် ပြောင်းသည့် ဖိုင်၊ insertion နှင့် deletion အရေအတွက်
ပါရမည်။ `lab.py` ၏ output တွင် `commit စုစုပေါင်း : 6` ပြရမည်။

---

## Exercise 6 — working tree အစီရင်ခံစာ ထုတ်ခြင်း

**လိုအပ်ချက်** — `git status --short` ၏ entry များကို untracked / modified / staged / unmerged
အုပ်စု ခွဲထုတ်ပြီး push ရန် အဆင်သင့် ဖြစ်/မဖြစ် ဆုံးဖြတ်ရမည်။

**လုပ်ရမည့် အဆင့်**

1. `git status --short` ကို run ပါ။
2. entry တိုင်းကို `?? ` (untracked)၊ ` M ` (modified)၊ `A `/`M ` (staged)၊ `UU` (unmerged) ဖြင့် ခွဲပါ။
3. `lab.py` ၏ `status_report` (Exercise 6) ကို run ပါ။
4. conflict (`UU`) ရှိလျှင် push မလုပ်ရဟု ဆုံးဖြတ်ပါ။

**အောင်မြင်မှု စစ်နည်း** — အုပ်စု တစ်ခုစီ၏ path စာရင်း သည် `git status --short` ၏ လိုင်းများနှင့်
ကိုက်ရမည်။ `unmerged` ရှိလျှင် `push ရန် အဆင်သင့် : False` ဖြစ်ရမည်။ conflict မရှိဘဲ staged
မရှိလျှင်လည်း `False` ဖြစ်ပြီး လုပ်ဆောင်ရမည့် အဆင့်သည် `git add` ဖြင့် စရမည်။
