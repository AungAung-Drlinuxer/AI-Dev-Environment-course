# Module 10 — Terminal & Shell

**Type:** Learn · **Time:** ~35 min · **Prerequisites:** Phase 0, Lesson 01

## ရည်ရွယ်ချက်

ဤ module သည် AI အလုပ်အတွက် လိုအပ်သည့် terminal ကျွမ်းကျင်မှုကို သင်ပေးသည်။ ပြီးစီးပါက —

- pipe၊ redirect နှင့် `grep` ဖြင့် training log ကို စစ်ထုတ် စီမံနိုင်မည်။
- training နှင့် GPU monitor ကို တစ်ပြိုင်နက် လည်ပတ်စေသည့် pane များစွာ ပါသော `tmux` session ကို
  ဖန်တီး၍ detach/reattach လုပ်နိုင်မည်။
- `htop`၊ `nvtop` နှင့် `nvidia-smi` ဖြင့် resource အခြေအနေကို ကြည့်ရှုနိုင်မည်။
- `ssh`၊ `scp` နှင့် `rsync` ဖြင့် ဒေသတွင်း နှင့် remote machine အကြား ဖိုင်များကို ရွှေ့နိုင်မည်။

## လိုအပ်ချက် (Prerequisites)

- ကိုယ်ပိုင် machine (Linux၊ macOS သို့မဟုတ် WSL2) နှင့် terminal တစ်ခု။
- Phase 0 ၏ Lesson 01 (Dev Environment) ကို ပြီးစီးထားခြင်း။
- Python အခြေခံ (variable၊ function၊ list၊ dict၊ `import`) — `lab.py` ကို ဖတ်ရန်။
- GPU သည် **မလိုအပ်ပါ**။ `nvidia-smi` နှင့် `nvtop` အခန်းများသည် GPU ရှိသူအတွက် ဖြစ်သည်။

## Subtopic စာရင်း

1. Step 1 — Know your shell (`$SHELL`၊ history ရှာခြင်း၊ လုပ်ငန်းစဉ် ထိန်းချုပ်သည့် ကီးများ)
2. Step 2 — Piping and redirects (`|`၊ `>`၊ `>>`၊ `2>`၊ `2>&1`)
3. Step 3 — Background processes (`&`၊ `nohup`၊ `jobs`၊ `fg`၊ `kill`)
4. Step 4 — tmux (session၊ pane၊ detach/reattach)
5. Step 5 — Monitoring with `htop` and `nvtop` (`nvidia-smi` အပါ)
6. Step 6 — SSH for remote GPU boxes (`ssh`၊ `scp`၊ `rsync`၊ `~/.ssh/config`၊ port forwarding)
7. Step 7 — Useful aliases for AI work (`gpu`၊ `killtraining`၊ `ae`၊ `watchloss`)
8. Step 8 — Common AI terminal patterns (`tee`၊ `diff <()`၊ `find | xargs`၊ `df -h`၊ `du -sh`)

အနှစ်ချုပ် — ဤ module သည် **Learn** အမျိုးအစား ဖြစ်သည်။ ဖတ်ရန် သင်ခန်းစာ၏ အဓိကအပိုင်းသည်
`explanation.md` ဖြစ်ပြီး `lab.py` သည် ထို command များ၏ လုပ်ဆောင်ချက်ကို Python ဖြင့် တုပပြသည်။

## Exercise တစ်လိုင်းချင်း

1. **Exercise 1 — Parse a training log** — `epoch`/`loss` လိုင်းများကို regular expression ဖြင့် ဖတ်၍
   record အရေအတွက် နှင့် ဖိုင်အမျိုးအစားအလိုက် ခွဲခြားသည် (`parse_training_log`)။
2. **Exercise 2 — Filter lines with grep semantics** — `grep`၊ `grep -v`၊ `grep -E`၊ `grep -i` ၏
   အလုပ်လုပ်ပုံကို လိုင်းစစ်ထုတ်မှုအဖြစ် တုပသည် (`filter_lines`)။
3. **Exercise 3 — Run a pipeline** — `cat | grep | awk | sort | head > file` ကို အဆင့်လိုက် ချိတ်၍
   `>` နှင့် `>>` ၏ ကွာခြားချက်ကို ပြသည် (`run_pipeline`)။
4. **Exercise 4 — Loss statistics** — `tail -10` နှင့် စာရင်းအင်းဖြင့် loss ၏ အနိမ့်၊ အမြင့်၊ ပျမ်းမျှကို
   အနှစ်ချုပ်သည် (`loss_statistics`)။
5. **Exercise 5 — Build a tmux plan** — pane သုံးခု ပါသော session တစ်ခုအတွက် tmux command အစဉ်ကို
   တည်ဆောက်သည် (`tmux_plan`)။
6. **Exercise 6 — Log operations report** — အထက်ပါ အဆင့်များ၏ ရလဒ်ကို အစီရင်ခံစာ တစ်ခုအဖြစ်
   စုစည်းသည် (`log_ops_report`)။

## ဖိုင်စာရင်း

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic စာရင်း၊ exercise စာရင်း၊ ဖိုင်စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ (Step 1–8၊ figure ၃ ခု၊ ဇယားများ၊ သတိထားရမည့် အချက်များ၊ self-check ၅ ခု) |
| `exercise.md` | exercise ၆ ခု — လိုအပ်ချက်၊ အဆင့်များ၊ အောင်မြင်မှု စစ်ဆေးနည်း |
| `solution.md` | အဖြေ ၆ ခု — တကယ် run ရလဒ် နှင့်တကွ |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## Lab ကို run ခြင်း

```bash
# repository root မှ
python3 modules/10_terminal_and_shell/lab.py
```

ဤ lab သည် **standard library သာ** သုံးသည်။ network၊ GPU၊ Docker၊ `tmux` မလိုအပ်ပါ။
ရလဒ်သည် **deterministic** ဖြစ်သည် — fake training log ကို formula ဖြင့် တည်ဆောက်သည်။

**သတိ** — command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
