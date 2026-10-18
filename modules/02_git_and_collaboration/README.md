# Module 02 — Git & Collaboration

ဤ module သည် version control ကို **အလုပ်လုပ်တတ်သည်အထိ** လေ့ကျင့်ပေးသည်။ ရည်ရွယ်ချက်မှာ git ၏
feature အားလုံးကို လေ့လာခြင်း မဟုတ်ပါ။ ဤ course အတွင်း နေ့စဉ် အသုံးပြုမည့် အနည်းဆုံး command စုဖြင့်
အလုပ်မှန်မှန် လုပ်နိုင်ရန် ဖြစ်သည်။

Source lesson ၏ ဖော်ပြချက်အတိုင်း — version control သည် ရွေးချယ်နိုင်သည့် အရာ မဟုတ်ပါ။ Experiment တိုင်း၊
model တိုင်း၊ ရေးသည့် lesson တိုင်းကို track လုပ်ရမည်။

## ရည်ရွယ်ချက် (Goal)

- git identity (`user.name`, `user.email`) ကို configure လုပ်နိုင်ခြင်း
- `git add` → `git commit` → `git push` နေ့စဉ် လုပ်ငန်းစဉ်ကို နားလည်ခြင်း
- `main` ကို မချိုးဘဲ စမ်းသပ်မှုအတွက် branch ဖန်တီး၊ merge လုပ်နိုင်ခြင်း
- model checkpoint နှင့် ဖိုင် binary ကြီးများကို ချန်လှပ်သည့် `.gitignore` ရေးနိုင်ခြင်း
- `git log --oneline` ဖြင့် commit history ကို ဖတ်နိုင်ခြင်း

## လိုအပ်ချက် (Prerequisites)

- Phase 0၊ Lesson 01 (Dev Environment) ပြီးစီးပြီး ဖြစ်ခြင်း
- terminal အခြေခံ အသုံးပြုနိုင်ခြင်း (`cd`၊ `ls`၊ `mkdir`)
- GitHub account တစ်ခု (Step 4 အတွက် လိုအပ်သည်)
- ဤ module ၏ command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။

## Subtopic စာရင်း

| # | Subtopic | အကြောင်းအရာ |
|---|---|---|
| 1 | Step 1: Configure git | `git config --global user.name` နှင့် `user.email` |
| 2 | Step 2: The daily workflow | `git status`၊ `git add`၊ `git commit -m`၊ `git push origin main` |
| 3 | Step 3: Branching for experiments | `git checkout -b`၊ `git checkout main`၊ `git merge` |
| 4 | Step 4: Working with this course repo | fork၊ `git clone`၊ `my-progress` branch၊ `git push` |

## Exercise စာရင်း (တစ်လိုင်းချင်း)

1. **Exercise 1 — git identity ကို configure လုပ်ခြင်း** — `git config --global` ဖြင့် အမည်နှင့် email သတ်မှတ်၍ ပြန်ဖတ်စစ်သည်။
2. **Exercise 2 — checkpoint များကို ချန်လှပ်သည့် `.gitignore`** — `*.pt`၊ `*.pth`၊ `*.safetensors` ကို ဖုံးလွှမ်းပြီး `git status` ဖြင့် စစ်သည်။
3. **Exercise 3 — နေ့စဉ် add / commit / push လုပ်ငန်းစဉ်** — commit တစ်ခုကို အဆင့်လိုက် ဖန်တီး၍ remote သို့ ပို့သည်။
4. **Exercise 4 — branch ဖြင့် စမ်းသပ်ခြင်း** — `experiment/` branch တွင် ပြင်ဆင်၊ merge လုပ်၍ conflict ဖြစ်/မဖြစ် ဆုံးဖြတ်သည်။
5. **Exercise 5 — `git log --oneline` ဖြင့် history ဖတ်ခြင်း** — commit စာရင်းကို parse လုပ်၍ lesson များ ဘယ်လိုတိုးလာသည်ကို ကြည့်သည်။
6. **Exercise 6 — working tree အစီရင်ခံစာ** — untracked / modified / staged / unmerged ကို ခွဲထုတ်၍ push အဆင်သင့်မှုကို ဆုံးဖြတ်သည်။

## ဖိုင်စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic နှင့် exercise စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ (sequence diagram နှင့် flow chart ၄ ခု အပါအဝင်) |
| `exercise.md` | လက်တွေ့ လုပ်ရမည့် exercise ၆ ခု |
| `solution.md` | exercise ၆ ခု၏ အဖြေ (run ရလဒ် အမှန်နှင့်တကွ) |
| `lab.py` | offline lab — `python3 modules/02_git_and_collaboration/lab.py` |

## Lab ကို run ခြင်း

```bash
python3 modules/02_git_and_collaboration/lab.py
```

Lab သည် git binary ကို မခေါ်ပါ။ လုပ်ငန်းစဉ်များကို Python ဖြင့် memory ထဲတွင် သရုပ်ဖော်သည်။
network၊ GPU၊ third-party package မလိုပါ။
