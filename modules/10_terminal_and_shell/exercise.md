# Module 10 — Exercise

exercise ၆ ခုလုံးသည် `modules/10_terminal_and_shell/lab.py` တွင် run နိုင်သည့် ပုံစံဖြင့် ရှိသည်။
exercise တိုင်းတွင် **shell လမ်းကြောင်း** (တကယ့် command) နှင့် **Python လမ်းကြောင်း** (`lab.py` ရှိ function)
နှစ်မျိုး ရှိသည်။ မိမိ machine တွင် `tmux`၊ `htop`၊ NVIDIA GPU မရှိပါက Python လမ်းကြောင်းကို သုံးနိုင်သည်။

exercise တိုင်းအတွက် စစ်ဆေးနည်း သုံးဆင့် —

1. Shell လမ်းကြောင်းဖြစ်ပါက command ကို ကိုယ်တိုင် run ၍ ရလဒ်ကို ကြည့်သည်။
2. Python လမ်းကြောင်းဖြစ်ပါက `python3 modules/10_terminal_and_shell/lab.py` ကို run ၍
   သက်ဆိုင်ရာ exercise ၏ `[OK]` လိုင်းကို စစ်သည်။
3. `solution.md` ရှိ ရလဒ်နှင့် နှိုင်းယှဉ်သည်။ ကွာခြားပါက ရိုက်ထည့်သည့် command မှန်မမှန် ပြန်စစ်သည်။

---

## Exercise 1 — Parse a training log

**လိုအပ်ချက်** — training log တစ်ခုကို ဖန်တီး၍ `epoch`၊ `loss` နှင့် `lr` တန်ဖိုးများကို တစ်လိုင်းချင်း
parse လုပ်နိုင်ရမည်။ ဖိုင်ထဲရှိ လိုင်းအားလုံးသည် epoch record မဟုတ်သည်ကို မှတ်ရမည် — WARNING၊ ERROR
နှင့် အခြား လိုင်းများ ရော ပါသည်။

**အဆင့်များ**

1. Source lesson သည် ဤ command ဖြင့် fake log ကို ဖန်တီးသည် —

   ```bash
   for i in $(seq 1 100); do echo "epoch $i loss: $(echo "scale=4; 1/$i" | bc)"; sleep 0.1; done > fake_train.log
   ```

2. `tail -5 fake_train.log` ဖြင့် လိုင်းပုံစံကို ဦးစွာ ကြည့်သည်။
3. `wc -l fake_train.log` ဖြင့် လိုင်းအရေအတွက် ကို မှတ်သည်။
4. `grep -c "epoch" fake_train.log` ဖြင့် epoch လိုင်း အရေအတွက် ကို စစ်သည်။
5. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_1` (`parse_training_log`) သည် `train.log` ကို
   ဖန်တီး၍ လိုင်းတိုင်းကို `epoch` record၊ `ERROR`/`WARNING` record နှင့် အခြား ဟူ၍ ခွဲသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- epoch record အရေအတွက်သည် `grep -c "epoch"` ၏ အဖြေနှင့် တူညီရမည်။
- ပထမ record ၏ epoch သည် ၁ ဖြစ်ရမည်၊ နောက်ဆုံး record ၏ epoch သည် စုစုပေါင်း အရေအတွက် ဖြစ်ရမည်။
- parse မလုပ်နိုင်သည့် လိုင်းများကို အရေအတွက် ဖြင့် ပြရမည် (ဖျောက်ထားခြင်း မပြုရ)။
- `lab.py` တွင် `[OK] exercise_1 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 2 — Filter lines with grep semantics

**လိုအပ်ချက်** — `grep` သည် pattern ကို **ရှာသည်** (စာလုံးတစ်ခုလုံး တိုက်ဆိုင်မှုသာ မဟုတ်)။
`-v`၊ `-E` နှင့် `-i` option သုံးမျိုး၏ အပြုအမူကို ရှင်းပြနိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း — `fake_train.log` ပေါ်တွင် ဤ command များကို run သည်။

   ```bash
   grep "loss" train.log
   grep -c "loss" train.log
   grep -v "ERROR" train.log | wc -l
   grep -E "epoch (1|2|3)/" train.log
   grep -i "cuda" train.log
   ```

2. ရလဒ် တစ်ခုစီ၏ လိုင်းအရေအတွက် ကို မှတ်သည်။ `-c` သည် pattern ပါသည့် လိုင်း အရေအတွက် ကို
   ပြသည်၊ `-v` သည် မကိုက်ညီသည့် လိုင်းများကို ပြသည်၊ `-E` သည် ပို၍ ကျယ်ပြန့်သည့်
   regular expression ကို အသုံးပြုစေသည်၊ `-i` သည် အကြီးအသေး မခွဲခြားစေသည်။
3. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_2` (`filter_lines`) သည် ထို ငါးမျိုးလုံးကို
   `re` module ဖြင့် တုပပြီး လိုင်းအရေအတွက် ကို နှိုင်းယှဉ်စစ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `grep -c "loss" train.log` ၏ အဖြေသည် `exercise_2` ၏ `grep 'loss:'` အရေအတွက်နှင့် တူရမည်။
- `-v` ဖြင့် ရရှိသည့် အရေအတွက်သည် `wc -l` နှင့် `grep -c` နှစ်ခု၏ ကွာခြားချက်နှင့် တူရမည်။
- `[OK] exercise_2 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 3 — Run a pipeline

**လိုအပ်ချက်** — pipe နှင့် redirect ကို ပေါင်းစပ်၍ အဆင့်လိုက် လုပ်ငန်းစဉ် တစ်ခုကို တည်ဆောက်ရမည်။
အဆင့်တိုင်းတွင် လိုင်းမည်မျှ ကျန်သည်ကို ဖော်ပြနိုင်ရမည်။

**အဆင့်များ**

1. လုပ်ငန်းစဉ် ကို run သည် —

   ```bash
   cat train.log | grep "loss:" | awk '{print $NF}' | sort -n | head -5 > losses_sorted.txt
   cat losses_sorted.txt
   ```

2. `awk '{print $NF}'` သည် လိုင်းတိုင်း၏ နောက်ဆုံး field ကို ယူသည် — ထို field သည် loss တန်ဖိုး
   ဖြစ်ရမည်။ မဖြစ်ပါက log ၏ လိုင်းပုံစံကို ပြန်စစ်ရမည်။
3. `>` နှင့် `>>` ၏ ကွာခြားချက်ကို ပြရန် ဤ command ကို ထပ်ထည့်သည် —

   ```bash
   sort -n losses.txt | tail -5 >> losses_sorted.txt
   cat losses_sorted.txt
   ```

4. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_3` (`run_pipeline`) သည် အဆင့် ၇ ခုကို
   တစ်ဆင့်ချင်း လုပ်ဆောင်ပြီး အဆင့်တိုင်း၏ လိုင်းအရေအတွက် ကို ပြသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- အဆင့်တိုင်း၏ လိုင်းအရေအတွက်သည် လျော့ကျသွားသည့် အစဉ်ဖြစ်ရမည် (မတူညီဘဲ သို့မဟုတ် တူညီနိုင်သည်)။
- `cat losses_sorted.txt` သည် အနိမ့်ဆုံး ၅ ခု အစဉ်လိုက် ဖြစ်ရမည်။
- `>>` ဖြင့် ထပ်ထည့်ပြီးနောက် ဖိုင်ရှိ လိုင်းအရေအတွက် တိုးလာရမည်၊ ယခင် လိုင်းများ မပျောက်ရ။
- `[OK] exercise_3 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 4 — Loss statistics

**လိုအပ်ချက်** — loss တန်ဖိုးများမှ အနိမ့်ဆုံး၊ အမြင့်ဆုံး၊ ခန့်မှန်း ပျမ်းမျှ၊ နှင့် အဆုံး ၁၀ ခု၏
ပျမ်းမျှကို တွက်ရမည်။ ထို့အပြင် training ကောင်းမွန်စွာ လျော့ကျလာသည်ကို ခိုင်လုံစွာ ပြနိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း —

   ```bash
   grep "loss:" train.log | awk '{print $NF}' > losses.txt
   wc -l losses.txt
   head -3 losses.txt
   tail -3 losses.txt
   sort -n losses.txt | head -5
   sort -n losses.txt | tail -5
   ```

2. ပထမ ၁၀ ခု၏ ပျမ်းမျှ နှင့် အဆုံး ၁၀ ခု၏ ပျမ်းမျှကို နှိုင်းယှဉ်သည်။
3. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_4` (`loss_statistics`) သည် အရေအတွက်၊
   အနိမ့်ဆုံး၊ အမြင့်ဆုံး၊ ပျမ်းမျှ၊ `tail -10` ၏ ပျမ်းမျှ နှင့် ကောင်းမွန်လာသည့် ပမာဏကို ပြသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `wc -l losses.txt` ၏ အဖြေသည် epoch အရေအတွက် နှင့် တူရမည်။
- `sort -n losses.txt | head -5` ၏ ပထမတန်ဖိုးသည် `exercise_4` ၏ `min loss` နှင့် တူရမည်။
- `sort -n losses.txt | tail -5` ၏ နောက်ဆုံးတန်ဖိုးသည် `max loss` နှင့် တူရမည်။
- `mean of tail -10` သည် `mean of head -10` ထက် **ငယ်ရမည်** (loss လျော့ကျမှု၏ သက်သေ)။
- `[OK] exercise_4 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 5 — Build a tmux plan

**လိုအပ်ချက်** — pane သုံးခု ပါသော `tmux` session တစ်ခုအတွက် command အစဉ်ကို ရေးရမည်။
pane ၁ — training run၊ pane ၂ — GPU monitor၊ pane ၃ — log tail။ နောက်ဆုံးတွင် session ကို attach
လုပ်ရမည်။

**အဆင့်များ**

1. `tmux new -s training` ဖြင့် session ဖန်တီးသည်။ မရှိပါက `tmux -V` ဖြင့် install ဖြစ်/မဖြစ် စစ်သည်။
2. `Ctrl+B` ထို့နောက် `"` ဖြင့် အလျားလိုက် ခွဲသည်၊ `Ctrl+B` ထို့နောက် `%` ဖြင့် ဒေါင်လိုက် ခွဲသည်။
3. pane တိုင်းတွင် သက်ဆိုင်ရာ program ကို run သည် — `python train.py --epochs 100 --lr 1e-4`၊
   `watch -n1 nvidia-smi` နှင့် `tail -f logs/experiment.log`။
4. script ဖြင့် လုပ်လိုပါက source lesson ၏ `shell_aliases.sh` ရှိ `trainenv()` function ကို
   ကြည့်ပါ — ထို function သည် `tmux new-session -d`၊ `split-window -h`၊ `split-window -v`၊
   `send-keys` နှင့် `attach` ကို အစဉ်လိုက် ခေါ်သည်။
5. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_5` (`tmux_plan`) သည် command ၈ ခု ပါသော စာရင်း၊
   pane သုံးခု၏ အလုပ်များ နှင့် ကီး binding များကို ပြီးစီး စစ်ဆေးသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `tmux ls` သည် session အမည်ကို ပြရမည်။
- `Ctrl+B` ထို့နောက် `d` ဖြင့် detach လုပ်ပြီး `tmux attach -t training` ဖြင့် ပြန်ဝင်လျှင်
   pane သုံးခုလုံး ဆက်လက် ပြေးနေရမည်။
- စာရင်းတွင် `new-session` ၁ ခု၊ `split-window` ၂ ခု၊ `send-keys` ၃ ခု နှင့် `attach` ၁ ခု
   ပါရမည်။
- `[OK] exercise_5 — ...` လိုင်း ထွက်ရမည်။
- မှတ်ချက် — ဤ machine တွင် `tmux` install မလုပ်ထားပါက `lab.py` သည် command များကို
   စာရင်းအဖြစ်သာ စစ်သည်။

---

## Exercise 6 — Log operations report

**လိုအပ်ချက်** — အထက်ပါ အဆင့် အားလုံး၏ ရလဒ်ကို အစီရင်ခံစာ တစ်ခုအဖြစ် စုစည်းရမည်။
အစီရင်ခံစာတွင် ဖိုင် အရွယ်အစား၊ လိုင်းအရေအတွက် အမျိုးအစားအလိုက်၊ loss စာရင်းအင်း၊
error အရေအတွက်၊ ဖန်တီးထားသည့် ဖိုင်များ နှင့် tmux session အခြေအနေ ပါရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း —

   ```bash
   ls -la train.log
   du -h train.log
   wc -l train.log
   grep -c "ERROR" train.log
   grep -c "WARNING" train.log
   ```

2. `df -h` နှင့် `du -sh ./*` ဖြင့် disk အခြေအနေကို ထည့်သည် (training data သည် disk ကို
   လျင်မြန်စွာ ဖြည့်သည်)။
3. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_6` (`log_ops_report`) သည် အစီရင်ခံစာ ကို
   print ၍ `mean of tail -10 < mean loss` ဖြစ်ခြင်းကို စစ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- အစီရင်ခံစာရှိ `total lines` သည် `wc -l` ၏ အဖြေနှင့် တူရမည်။
- `ERROR lines` အရေအတွက်သည် `grep -c "ERROR"` ၏ အဖြေနှင့် တူရမည်။
- `exercise_3` ဖန်တီးခဲ့သည့် ဖိုင်နှစ်ခုလုံး ရှိနေရမည်။
- နောက်ဆုံးတွင် `[PASS] All 6/6 exercises passed successfully.` လိုင်း ထွက်ရမည်။
