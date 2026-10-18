# Module 11 — Exercise

exercise ၆ ခုလုံးသည် `modules/11_linux_for_ai/lab.py` တွင် run နိုင်သည့် ပုံစံဖြင့် ရှိသည်။
exercise တိုင်းတွင် **shell လမ်းကြောင်း** (တကယ့် Linux machine ပေါ်ရှိ command) နှင့်
**Python လမ်းကြောင်း** (`lab.py` ရှိ function) နှစ်မျိုး ရှိသည်။

မိမိ machine တွင် `sudo`၊ `apt` သို့မဟုတ် NVIDIA GPU မရှိပါက Python လမ်းကြောင်းကို သုံးနိုင်သည်။
Python လမ်းကြောင်း အဆင့် ၃ ဆင့် —

1. `python3 modules/11_linux_for_ai/lab.py` ကို repository root မှ run သည်။
2. သက်ဆိုင်ရာ exercise ၏ `[OK] exercise_N — ...` လိုင်းကို စစ်သည်။
3. `solution.md` ရှိ တကယ် run ရလဒ်နှင့် နှိုင်းယှဉ်သည်။ ကွာခြားပါက ရိုက်ထည့်သည့် command မှန်/မမှန်
   ပြန်စစ်သည်။

---

## Exercise 1 — Permission bits

**လိုအပ်ချက်** — `ls -l` ၏ mode string (`-rwxr-xr--`) နှင့် `chmod` ၏ octal mode (`754`) ကို အပြန်အလှန်
ပြောင်းနိုင်ရမည်။ symbolic change (`u+x`၊ `go-w`၊ `a+x`) ကို mode တစ်ခု အပေါ် ကျင့်သုံးနိုင်ရမည်။
`r` = ၄၊ `w` = ၂၊ `x` = ၁ ဖြစ်သည်ကို ကိုယ်တိုင် တွက်နိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း — ဖိုင် တစ်ခု ဖန်တီး၍ mode ကို ဖတ်သည်။

   ```bash
   touch train.sh
   ls -l train.sh          # -rw-r--r-- 1 user group 0 ... train.sh
   chmod +x train.sh       # Make a script executable
   ls -l train.sh          # -rwxr-xr-x
   chmod 644 config.yaml
   chmod 755 deploy.sh
   chmod 600 private.key
   ```

2. `ls -l` ၏ ပထမ ၁၀ စာလုံးကို ခွဲသည် — ပထမ ၁ လုံးသည် ဖိုင် အမျိုးအစား (`-` ဖိုင်၊ `d` directory)၊
   ကျန် ၉ လုံးသည် သုံးစု (user၊ group၊ other) ဖြစ်သည်။
3. octal ကို စုတစ်ခုစီ တွက်သည် — `rwx` = ၄+၂+၁ = ၇၊ `r-x` = ၄+၀+၁ = ၅၊ `r--` = ၄ ဖြစ်သဖြင့်
   `-rwxr-xr--` = `754`။
4. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_1` (`permission_bits`) သည် mode ၆ ခုကို octal အဖြစ်
   ပြောင်း၍ octal မှ symbolic သို့ ပြန်ပြောင်းကာ အလှည့်အပြန်လည် တူညီမှုကို စစ်သည်။
   symbolic change ၄ ခုကိုလည်း တွက်ပြသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `chmod +x train.sh` ပြီးနောက် `ls -l` သည် `-rwxr-xr-x` (= `755`) ဖြစ်ရမည်။
- `lab.py` ၏ round trip (`octal` မှ ပြန်ပြောင်းရလဒ်) သည် mode အရင်းနှင့် လိုင်းတိုင်း "same" ဖြစ်ရမည်။
- `a+x` ကို `-rw-r--r--` အပေါ် ကျင့်သုံးပါက `-rwxr-xr-x` (= `755`) ရရမည်။
- `[OK] exercise_1 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 2 — Diagnose "Permission denied"

**လိုအပ်ချက်** — `ls -la` output မှ mode၊ owner နှင့် group ကို ဖတ်၍ မည်သည့် permission class
(user၊ group၊ other) က ဆုံးဖြတ်သည်ကို ရှာနိုင်ရမည်။ ထို class တွင် လိုအပ်သည့် bit ရှိ/မရှိ
ဆုံးဖြတ်နိုင်ရမည်။ ဖြေရှင်းချက် သုံးမျိုး — `chmod` (bit)၊ `chown` (owner) နှင့် `sudo` (တစ်ကြိမ်
အခွင့် ငှားခြင်း) — ကို မှန်ကန်စွာ ရွေးနိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း — permission ပြဿနာ ဖန်တီး၍ စစ်သည်။

   ```bash
   whoami                  # What user am I?
   ls -la train.sh
   ./train.sh              # bash: ./train.sh: Permission denied
   chmod +x train.sh
   ./train.sh              # now it runs

   ls -la /data/checkpoints
   touch /data/checkpoints/x.pt   # Permission denied (root owns the directory)
   sudo chown -R "$(whoami)":"$(whoami)" /data/checkpoints
   ```

2. `ls -la` ၏ ကော်လံ ၃ ခုကို ဖတ်သည် — mode၊ owner၊ group။
3. `whoami` ၏ ရလဒ်နှင့် owner ကို နှိုင်းယှဉ်သည်။ ကိုက်ညီပါက user class၊ မကိုက်ညီပါက group class၊
   group လည်း မပါပါက other class ကို စစ်သည်။
4. ထို class ၏ ၃ လုံးတွင် လိုအပ်သည့် လုံး (`r`၊ `w`၊ `x`) ရှိ/မရှိ ကြည့်သည်။
5. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_2` (`diagnose_permission_denied`) သည် သတ်မှတ်ထားသည့်
   `ls -la` စာသား အပေါ်တွင် အခြေအနေ ၇ ခုကို စစ်၍ denied အခြေအနေ ၃ ခုနှင့် fix ၃ ခုကို ထုတ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `./train.sh` သည် `chmod +x` မလုပ်မီ denied၊ ပြီးနောက် run ရမည်။
- `lab.py` ၏ denied အရေအတွက်သည် ၃ ဖြစ်ရမည် — `./train.sh (execute)`၊ `./setup_gpu.sh (execute)`၊
  `/data/checkpoints (write)`။
- fix စာရင်းတွင် `chmod +x train.sh`၊ `sudo chmod +x setup_gpu.sh` နှင့်
  `sudo chown -R ubuntu:ubuntu /data/checkpoints` ပါရမည်။
- directory ထဲ **ဝင်ခြင်း** (`enter`) သည် other class ၏ `x` bit ဖြင့် ခွင့်ပြုခံရမည် — write နှင့်
  မတူသည်ကို မှတ်ရမည်။
- `[OK] exercise_2 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 3 — Disk report

**လိုအပ်ချက်** — `df -h` နှင့် `du -sh` ၏ စာသား output ကို parse လုပ်၍ စုစုပေါင်း capacity၊
သုံးပြီး ပမာဏ၊ ကျန်နေသည့် ပမာဏ၊ ၈၅% ကျော်နေသည့် mount နှင့် အကြီးဆုံး directory များကို
ဖော်ပြနိုင်ရမည်။ `tmpfs` ကဲ့သို့ အမှတ်တကယ် drive မဟုတ်သည့် entry များကို ခွဲထုတ်နိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း —

   ```bash
   df -h                       # Disk usage for all mounted drives
   df -h /home                 # Disk usage for /home specifically
   du -sh *                    # Size of each item in current directory
   du -sh ~/.cache             # pip and huggingface models land here
   du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20
   ```

2. `df -h` ၏ ကော်လံများ — `Filesystem`၊ `Size`၊ `Used`၊ `Avail`၊ `Use%`၊ `Mounted on`။ `Use%` ကို
   ဖတ်၍ ၈၅% ကျော်သည့် mount ကို မှတ်သည်။
3. `du -sh` ၏ လိုင်းတိုင်းသည် `size<TAB>path` ပုံစံ ဖြစ်သည်။ `sort -hr` ဖြင့် ကြီးစဉ် စီသည်။
4. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_3` (`disk_report`) သည် သတ်မှတ်ထားသည့် `df -h` နှင့်
   `du -sh` စာသားကို parse လုပ်၍ ဇယား၊ စုစုပေါင်း နှင့် သတိပေးချက်ကို ထုတ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- `df -h` မှ entry ၃ ခု ဖတ်ရမည်၊ ထိုအနက် `tmpfs` ကို ချန်လှပ်ပါက အမှတ်တကယ် file system ၂ ခု ကျန်ရမည်။
- စုစုပေါင်း capacity သည် `/dev/root` ၏ `98G` နှင့် `/dev/nvme0n1p2` ၏ `1.8T` ပေါင်းလဒ် ဖြစ်ရမည်။
- ၈၅% ကျော်သည့် mount သည် `/data` (93%) တစ်ခုသာ ဖြစ်ရမည်။
- အကြီးဆုံး ၃ ခုသည် `12G /data/checkpoints`၊ `2.4G /data/tokenized`၊ `1.1G /home/ubuntu/.cache` ဖြစ်ရမည်။
- `[OK] exercise_3 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 4 — apt install plan

**လိုအပ်ချက်** — GPU box အသစ် တစ်ခုအတွက် command အစဉ်ကို တည်ဆောက်ရမည်။ ပထမ အဆင့်သည်
`sudo apt update` ဖြစ်ရမည်။ install အဆင့်တွင် source lesson ၏ package ၈ ခု ပါရမည်။ အဆင့်တိုင်းတွင်
sudo လို/မလို နှင့် ရည်ရွယ်ချက် ပါရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း —

   ```bash
   whoami                      # What user am I?
   sudo apt update             # Refresh the package list (always do this first)
   sudo apt install -y \
       build-essential \
       git \
       curl \
       wget \
       tmux \
       htop \
       unzip \
       python3-venv
   apt list --installed        # What's installed?
   nvidia-smi                  # GPU processes and memory usage
   sudo apt clean              # Clear apt cache
   ```

2. package တိုင်း၏ ရည်ရွယ်ချက်ကို မှတ်သည် — `build-essential` သည် C compiler နှင့် `make`
   (Python package အများအပြား compile လုပ်ရန် လိုသည်)၊ `tmux` သည် session ကို ရှင်သန်စေသည်၊
   `python3-venv` သည် virtual environment ဖန်တီးနိုင်စေသည်။
3. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_4` (`apt_install_plan`) သည် အဆင့် ၆ ခု ပါသော အစီအစဉ်ကို
   တည်ဆောက်၍ အစဉ်၊ `-y`၊ sudo အရေအတွက် နှင့် package စာရင်း ပြည့်စုံမှုကို စစ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- အစီအစဉ်၏ ဒုတိယ အဆင့်သည် `sudo apt update` ဖြစ်ရမည် (ပထမ အဆင့်သည် `whoami`)။
- install အဆင့်တွင် package ၈ ခုလုံး ပါရမည်၊ `-y` တစ်ကြိမ် ပါရမည်။
- sudo လိုသည့် အဆင့် ၃ ခု ရှိရမည် — `apt update`၊ `apt install`၊ `apt clean`။
- `apt list --installed` ဖြင့် စစ်ပြီးနောက် ပျောက်နေသည့် package မရှိရမည်။
- `[OK] exercise_4 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 5 — macOS vs Linux

**လိုအပ်ချက်** — macOS မှ Linux သို့ ကူးသည့်အခါ ကွာခြားချက် ၈ ခုကို ဇယားအဖြစ် စီနိုင်ရမည်။
တစ်ခုစီအတွက် ကျရှုံးမှု အဖြစ်များသည့် နေရာ (trap) ကို ဖော်ပြနိုင်ရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း — macOS တွင် ရေးထားသည့် command ကို Linux ပေါ်တွင် စမ်းသည်။

   ```bash
   brew install htop            # command not found -> sudo apt install htop
   open file.txt                # command not found -> xdg-open, or cat / less
   sed -i '' 's/a/b/' config.yaml   # GNU sed takes the empty string as a file name
   sed -i 's/a/b/' config.yaml      # the Linux form
   echo $SHELL                  # most servers use bash, not zsh
   ls Model.py model.py         # on Linux these are two different files
   file script.sh               # "with CRLF line terminators" -> dos2unix script.sh
   ```

2. ကွာခြားချက် တိုင်းအတွက် တစ်လိုင်း trap ကို ရေးသည် — ဥပမာ rc ဖိုင်၊ binary လမ်းကြောင်း၊
   case sensitivity၊ line endings။
3. Python လမ်းကောင်း — `lab.py` ၏ `exercise_5` (`macos_vs_linux`) သည် ကွာခြားချက် ၈ ခု ပါသော
   ဇယားကို ဆွဲ၍ trap စာရင်းကို အက္ခရာ အစဉ်အတိုင်း စီပြီး remote box တွင် အဖြစ်များသည့် နေရာ ၄ ခုကို
   ဖော်ပြသည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- ဇယားတွင် လိုင်း ၈ ခု ရှိရမည်၊ လိုင်းတိုင်းတွင် ကော်လံ ၃ ခု (`macOS`၊ `Linux`၊ trap) ရှိရမည်။
- `sed -i` လိုင်းသည် macOS တွင် `-i ''` ဖြင့် စရမည်၊ Linux တွင် မပါရ။
- `~/.zshrc` နှင့် `~/.bashrc` သည် လိုင်းတစ်ခုတွင် တွဲရှိရမည်။
- case-sensitive လိုင်း ပါရမည်။
- `[OK] exercise_5 — ...` လိုင်း ထွက်ရမည်။

---

## Exercise 6 — Linux operations report

**လိုအပ်ချက်** — exercise ၁–၅ ၏ ရလဒ်ကို အစီရင်ခံစာ တစ်ခုအဖြစ် စုစည်းရမည်။ အစီရင်ခံစာတွင်
permission အခြေအနေ၊ disk အခြေအနေ၊ package အစီအစဉ် နှင့် porting အရေအတွက် ပါရမည်။

**အဆင့်များ**

1. Shell လမ်းကြောင်း — report အတွက် အချက်အလက် စုသည်။

   ```bash
   whoami
   ls -la
   df -h
   du -sh ~/.cache
   apt list --installed | wc -l
   ```

2. exercise တိုင်း၏ ရလဒ်ကို တစ်နေရာတွင် ပေါင်းသည် — mode ၆ ခု၊ denied ၃ ခု၊ fix ၃ ခု၊
   file system ၃ ခု၊ ၈၅% ကျော် mount ၁ ခု၊ package ၈ ခု၊ ကွာခြားချက် ၈ ခု။
3. Python လမ်းကြောင်း — `lab.py` ၏ `exercise_6` (`linux_ops_report`) သည် report ကို print ၍
   ကိန်းဂဏန်း တိုင်း တူညီ/မတူညီ ကို `assert` ဖြင့် စစ်သည်။

**အောင်မြင်မှု စစ်ဆေးခြင်း**

- အစီရင်ခံစာရှိ octal mode စာရင်းသည် exercise 1 ၏ ရလဒ်နှင့် တူရမည် (`train.sh=644`၊ `deploy.sh=755`၊
  `config.yaml=644`၊ `private.key=600`၊ `dataset/=755`၊ `checkpoints/=700` ဖြစ်သည်။
- denied အရေအတွက်သည် exercise 2 ၏ ရလဒ် (၃) နှင့် တူရမည်။
- အကြီးဆုံး directory သည် `/data/checkpoints` ဖြစ်ရမည်။
- ပထမ အဆင့်သည် `whoami` ဖြစ်ရမည်။
- နောက်ဆုံးတွင် `[PASS] All 6/6 exercises passed successfully.` လိုင်း ထွက်ရမည်။
