# Module 10 — Solution

ဤစာရှိ output အားလုံးသည် တကယ် run ရလဒ် ဖြစ်သည်။ Lab ကို ဤ command ဖြင့် run သည် —

```bash
python3 modules/10_terminal_and_shell/lab.py
```

- exit code — `0`
- နောက်ဆုံးလိုင်း — `[PASS] All 6/6 exercises passed successfully.`

Lab သည် `train.log` ကို temp directory တစ်ခုအတွင်း ရေးသည်။ ထို လမ်းကြောင်းသည် run တိုင်း
ပြောင်းလဲသည် (မိမိ machine ၏ temp directory)။ ဤစာတွင် ဖော်ပြသည့် လိုင်းအရေအတွက်၊ loss တန်ဖိုး
နှင့် အစီရင်ခံစာ အားလုံးသည် run တိုင်း တူညီသည်။

---

## Exercise 1 — Parse a training log

**အဖြေ** — Source lesson ၏ command ဖြင့် fake log ကို ဖန်တီးပြီး လိုင်းအရေအတွက်ကို ဦးစွာ စစ်သည်။

```bash
for i in $(seq 1 100); do echo "epoch $i loss: $(echo "scale=4; 1/$i" | bc)"; sleep 0.1; done > fake_train.log
tail -5 fake_train.log
wc -l fake_train.log
grep -c "epoch" fake_train.log
```

ရလဒ် —

```
--- tail -5 fake_train.log ---
epoch 96 loss: .0104
epoch 97 loss: .0103
epoch 98 loss: .0102
epoch 99 loss: .0101
epoch 100 loss: .0100
--- wc -l fake_train.log ---
100 fake_train.log
--- grep -c epoch ---
100
```

ထို ဖိုင်သည် လိုင်း ၁၀၀ နှင့် epoch ၁၀၀ လုံး ကိုက်ညီသည် — ထို့ကြောင့် ထို ဖိုင်တွင် parse မလုပ်နိုင်သည့်
လိုင်း မရှိပါ။ လက်တွေ့ log သည်မူ ထိုထက် ရှုပ်ထွေးသည်။ Lab ၏ `train.log` တွင် timestamp၊
learning rate၊ `ERROR` နှင့် `WARNING` လိုင်းများ ပါသည်။

Python လမ်းကြောင်း (`exercise_1` — `parse_training_log`) ရလဒ် —

```
exercise_1 - parse_training_log
  file      : train.log
  path      : <tmp>/train.log
  total lines: 106
  epoch records : 100
  level records : 5 (ERROR 2, WARNING 3)
  other records : 1
  first 3 epochs:
    epoch   1/100 lr 1.00e-04 loss 2.4420
    epoch   2/100 lr 1.00e-04 loss 2.3878
    epoch   3/100 lr 1.00e-04 loss 2.2373
  last 3 epochs:
    epoch  98/100 lr 1.00e-04 loss 0.0696
    epoch  99/100 lr 1.00e-04 loss 0.1077
    epoch 100/100 lr 1.00e-04 loss 0.0458
  unparsed line: '[2026-01-01 00:01:46] final_accuracy=0.8731'
[OK] exercise_1 - parsed 100 epoch records and 5 level records
```

ရှင်းလင်းချက် — လိုင်း ၁၀၆ လိုင်းကို အမျိုးအစား သုံးမျိုး ခွဲသည်။ epoch record ၁၀၀ ခု၊
`ERROR`/`WARNING` record ၅ ခု၊ နှင့် parse မလုပ်နိုင်သည့် လိုင်း ၁ လိုင်း
(`final_accuracy=0.8731`) ဖြစ်သည်။ `epoch records` အရေအတွက်သည် shell မှ `grep -c "epoch"` ၏
အဖြေနှင့် တူညီသည်။

---

## Exercise 2 — Filter lines with grep semantics

**အဖြေ** — Shell လမ်းကြောင်း —

```bash
grep -c "loss:" train.log
grep -v "ERROR" train.log | wc -l
grep -c "WARNING" train.log
grep -i "cuda" train.log | wc -l
grep "ERROR" train.log
grep -E "epoch (1|2|3)/" train.log
```

ရလဒ် —

```
100                    # grep -c "loss:"
104                    # grep -v "ERROR" | wc -l
3                      # grep -c "WARNING"
2                      # grep -i "cuda" | wc -l
[2026-01-01 00:00:39] ERROR - CUDA out of memory at step 592
[2026-01-01 00:01:18] ERROR - CUDA out of memory at step 1184
[2026-01-01 00:00:01] epoch 1/100 lr: 1.00e-04 loss: 2.4420
[2026-01-01 00:00:02] epoch 2/100 lr: 1.00e-04 loss: 2.3878
[2026-01-01 00:00:03] epoch 3/100 lr: 1.00e-04 loss: 2.2373
```

- `-c` သည် pattern ပါသည့် လိုင်း **အရေအတွက်** ကို ပြသည် — လိုင်းများကို မပြပါ။
- `-v` သည် မကိုက်ညီသည့် လိုင်းများကို ပြသည်။ လိုင်း ၁၀၆ မှ `ERROR` ၂ လိုင်း နုတ်လျှင် ၁၀၄ လိုင်း။
- `-i` သည် အကြီးအသေး မခွဲခြားစေသည့်အတွက် `cuda` သည် `CUDA` ကို တွေ့သည်။
- `-E` သည် `(1|2|3)` ကဲ့သို့ ကျယ်ပြန့်သည့် pattern ကို အသုံးပြုစေသည်။

Python လမ်းကြောင်း (`exercise_2` — `filter_lines`) ရလဒ် —

```
exercise_2 - filter_lines (grep semantics)
  grep 'loss:'            -> 100 lines
    first : [2026-01-01 00:00:01] epoch 1/100 lr: 1.00e-04 loss: 2.4420
    last  : [2026-01-01 00:01:45] epoch 100/100 lr: 1.00e-04 loss: 0.0458
  grep 'ERROR'            -> 2 lines
    [2026-01-01 00:00:39] ERROR - CUDA out of memory at step 592
    [2026-01-01 00:01:18] ERROR - CUDA out of memory at step 1184
  grep 'WARNING'          -> 3 lines
  grep -v 'ERROR|WARNING' -> 101 lines
  grep -E 'epoch (1|2|3)/' -> 3 lines
    [2026-01-01 00:00:01] epoch 1/100 lr: 1.00e-04 loss: 2.4420
    [2026-01-01 00:00:02] epoch 2/100 lr: 1.00e-04 loss: 2.3878
    [2026-01-01 00:00:03] epoch 3/100 lr: 1.00e-04 loss: 2.2373
  grep -i 'cuda'          -> 2 lines
[OK] exercise_2 - grep filtered 106 lines down to 100 loss lines
```

ရှင်းလင်းချက် — Python လမ်းကြောင်းရှိ `grep -v 'ERROR|WARNING'` သည် လိုင်းနှစ်မျိုးလုံးကို
ဖယ်ထုတ်သည့်အတွက် လိုင်း ၁၀၁ လိုင်း ရသည်။ shell တွင် `grep -v "ERROR|WARNING"` သည်
`-E` မပါလျှင် pipe ကို စာလုံးရိုးအဖြစ် ယူသည့်အတွက် ဤစာရှိ `-v` ဥပမာသည် `ERROR` တစ်မျိုးတည်း
ဖယ်သည့် ပုံစံကို သုံးထားသည်။ ဤအချက်သည် `-E` ၏ တန်ဖိုးကို ပြသည်။

---

## Exercise 3 — Run a pipeline

**အဖြေ** — Shell လမ်းကြောင်း —

```bash
cat train.log | grep "loss:" | awk '{print $NF}' | sort -n | head -5 > losses_sorted.txt
cat losses_sorted.txt
sort -n losses.txt | tail -5 >> losses_sorted.txt
cat losses_sorted.txt
```

ရလဒ် —

```
0.0458
0.0559
0.0683
0.0696
0.0806
```

ထို့နောက် `>>` ဖြင့် ထပ်ထည့်ပြီးနောက် —

```
0.0458
0.0559
0.0683
0.0696
0.0806
2.0468
2.1904
2.2373
2.3878
2.4420
```

`>` သည် ဖိုင်ကို အစမှ ပြန်ရေးသည်၊ `>>` သည် အဆုံးတွင် ထပ်ဖြည့်သည်။ ဤကြောင့် ဒုတိယ command ပြီးသည့်အခါ
လိုင်း ၅ လိုင်းစာ ပျောက်မသွားဘဲ လိုင်း ၁၀ လိုင်း ဖြစ်လာသည်။

Python လမ်းကြောင်း (`exercise_3` — `run_pipeline`) ရလဒ် —

```
exercise_3 - run_pipeline
  pipeline: cat train.log | grep 'loss:' | awk '{print $NF}' | sort -n | head -5 > losses_sorted.txt
    stage 1: cat train.log                      -> 106 lines
    stage 2: grep 'loss:'                       -> 100 lines
    stage 3: awk '{print $NF}'                  -> 100 lines
    stage 4: sort -n                            -> 100 lines
    stage 5: head -5                            ->   5 lines
    stage 6: > losses_sorted.txt                ->   5 lines
    stage 7: tail -5 >> losses_tail5.txt        ->   6 lines
  file losses_sorted.txt after redirect (>):
    0.0458
    0.0559
    0.0683
    0.0696
    0.0806
  file losses_tail5.txt after append (>>):
    2.0468
    2.1904
    2.2373
    2.3878
    2.4420
    # appended by >> losses_tail5.txt
[OK] exercise_3 - pipeline of 7 stages wrote 2 files
```

ရှင်းလင်းချက် — အဆင့် ၁ မှ ၅ အထိ လိုင်းအရေအတွက် လျော့ကျသွားသည် (၁၀၆ → ၁၀၀ → ၁၀၀ → ၁၀၀ → ၅)။
အဆင့် ၇ သည် `>>` ဖြင့် ထပ်ဖြည့်သည့်အတွက် ၅ လိုင်း အစား ၆ လိုင်း (ထပ်ဖြည့်သည့် အမှတ်အသားလိုင်း
အပါ) ဖြစ်သည်။

---

## Exercise 4 — Loss statistics

**အဖြေ** — Shell လမ်းကြောင်း —

```bash
grep "loss:" train.log | awk '{print $NF}' > losses.txt
wc -l losses.txt
sort -n losses.txt | head -5
sort -n losses.txt | tail -5
head -10 losses.txt | awk '{s+=$1} END {printf "head-10 mean: %.4f\n", s/NR}'
tail -10 losses.txt | awk '{s+=$1} END {printf "tail-10 mean: %.4f\n", s/NR}'
```

ရလဒ် —

```
100 losses.txt
0.0458
0.0559
0.0683
0.0696
0.0806
2.0468
2.1904
2.2373
2.3878
2.4420
head-10 mean: 2.0596
tail-10 mean: 0.0952
```

အဆုံး ၁၀ ခု၏ ပျမ်းမျှ (0.0952) သည် ပထမ ၁၀ ခု၏ ပျမ်းမျှ (2.0596) ထက် အလွန် ငယ်သည် —
training ကောင်းမွန်စွာ လျော့ကျလာကြောင်း သက်သေ ဖြစ်သည်။

Python လမ်းကြောင်း (`exercise_4` — `loss_statistics`) ရလဒ် —

```
exercise_4 - loss_statistics
  values        : 100
  min loss      : 0.0458 (epoch 100)
  max loss      : 2.4420 (epoch 1)
  mean loss     : 0.6414
  mean of head -10 : 2.0596
  mean of tail -10 : 0.0952
  tail -10 values :
    epoch  91 loss 0.1056
    epoch  92 loss 0.1431
    epoch  93 loss 0.0806
    epoch  94 loss 0.1182
    epoch  95 loss 0.0559
    epoch  96 loss 0.0937
    epoch  97 loss 0.1316
    epoch  98 loss 0.0696
    epoch  99 loss 0.1077
    epoch 100 loss 0.0458
  improvement head->tail: 1.9644
  final epoch loss from log: 0.0458
[OK] exercise_4 - loss dropped from 2.0596 to 0.0952 (mean tail -10)
```

ရှင်းလင်းချက် — `min loss` သည် `sort -n | head -5` ၏ ပထမတန်ဖိုး နှင့် တူညီသည်၊
`max loss` သည် `sort -n | tail -5` ၏ နောက်ဆုံးတန်ဖိုး နှင့် တူညီသည်။ `max loss` (2.4420) သည်
epoch ၁ တွင် ဖြစ်ပေါ်သည်၊ `min loss` (0.0458) သည် epoch ၁၀၀ တွင် ဖြစ်ပေါ်သည်။

---

## Exercise 5 — Build a tmux plan

**အဖြေ** — ဤ machine တွင် `tmux` install မလုပ်ထားသည်ကို ဦးစွာ စစ်သည် —

```
tmux: not installed on this machine
```

ထို့ကြောင့် command အစဉ်ကို (၁) source lesson ၏ `shell_aliases.sh` ရှိ `trainenv()` function ဖြင့်
နှင့် (၂) `lab.py` ၏ `exercise_5` ဖြင့် စစ်သည်။ `trainenv()` ကို တကယ် load လုပ်ကြည့်သည့် ရလဒ် —

```bash
bash -c 'source ./shell_aliases.sh; type trainenv'
```

```
trainenv is a function
trainenv ()
{
    local name="${1:-train}";
    tmux new-session -d -s "$name";
    tmux split-window -h -t "$name";
    tmux split-window -v -t "$name";
    tmux send-keys -t "$name:0.1" 'watch -n1 nvidia-smi' C-m;
    tmux send-keys -t "$name:0.2" 'htop' C-m;
    tmux select-pane -t "$name:0.0";
    tmux attach -t "$name"
}
```

Python လမ်းကြောင်း (`exercise_5` — `tmux_plan`) ရလဒ် —

```
exercise_5 - tmux_plan
  session: 'training' with 3 panes
    pane training:0.0 Training run   runs: python train.py --epochs 100 --lr 1e-4
    pane training:0.1 GPU monitor    runs: watch -n1 nvidia-smi
    pane training:0.2 Logs           runs: tail -f logs/experiment.log
  command sequence:
    1. tmux new-session -d -s training -n train
    2. tmux split-window -h -t training
    3. tmux split-window -v -t training
    4. tmux send-keys -t training:0.0 'python train.py --epochs 100 --lr 1e-4' C-m
    5. tmux send-keys -t training:0.1 'watch -n1 nvidia-smi' C-m
    6. tmux send-keys -t training:0.2 'tail -f logs/experiment.log' C-m
    7. tmux select-pane -t training:0.0
    8. tmux attach -t training
  key bindings (prefix Ctrl+B):
    Ctrl+B then "            split the window horizontally
    Ctrl+B then %            split the window vertically
    Ctrl+B then arrow key    move between panes
    Ctrl+B then d            detach; the session keeps running
  reattach later with: tmux attach -t training
  list sessions with : tmux ls
[OK] exercise_5 - built 8-command plan for 3 panes
```

`tmux` ကို install လုပ်ပြီးပါက command ၈ ခုကို အစဉ်လိုက် run လျှင် pane သုံးခုနှင့် program
သုံးခု ပြေးနေသည့် session တစ်ခု ရသည်။ `Ctrl+B` ထို့နောက် `d` ဖြင့် detach လုပ်ပြီး
`tmux attach -t training` ဖြင့် ပြန်ဝင်နိုင်သည်။

---

## Exercise 6 — Log operations report

**အဖြေ** — Shell လမ်းကြောင်း —

```bash
wc -l train.log
du -h train.log
ls -la train.log
grep -c "ERROR" train.log
grep -c "WARNING" train.log
```

ရလဒ် —

```
106 train.log
8.0K	train.log
-rw-rw-r-- 1 aungaung aungaung 6436 Oct 18 08:33 train.log
2
3
```

Python လမ်းကြောင်း (`exercise_6` — `log_ops_report`) ရလဒ် —

```
exercise_6 - log_ops_report
  ==================== operations report ====================
  log file          : train.log (6436 bytes)
  workspace         : <tmp>
  total lines       : 106
  epoch lines       : 100
  ERROR lines       : 2 -> CUDA out of memory at step 592; CUDA out of memory at step 1184
  WARNING lines     : 3
  other lines       : 1 -> '[2026-01-01 00:01:46] final_accuracy=0.8731'
  loss min / mean / max : 0.0458 / 0.6414 / 2.4420
  mean of tail -10 loss : 0.0952
  best epoch            : 100
  pipeline artifacts    : losses_sorted.txt, losses_tail5.txt
  tail artifact exists  : True
  tmux session plan     : 3 panes in 'training'
  verdict               : log readable, loss decreasing, 2 errors to review
  ==========================================================
[OK] exercise_6 - ops report over 106 lines, 2 errors, 3 warning
```

ရှင်းလင်းချက် — အစီရင်ခံစာရှိ `total lines` (၁၀၆) သည် `wc -l` ၏ အဖြေနှင့် တူညီသည်။
`ERROR lines` (၂) နှင့် `WARNING lines` (၃) သည်လည်း shell ၏ `grep -c` အဖြေများနှင့် တူညီသည်။
`mean of tail -10 loss` (0.0952) သည် `mean loss` (0.6414) ထက် ငယ်သည့်အတွက် စစ်ဆေးချက်
အောင်မြင်သည်။

Lab တစ်ခုလုံး၏ နောက်ဆုံးလိုင်း —

```
[PASS] All 6/6 exercises passed successfully.
```
