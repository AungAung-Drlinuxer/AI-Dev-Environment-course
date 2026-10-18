# Module 11 — Solution

ဤစာရှိ output အားလုံးသည် တကယ် run ရလဒ် ဖြစ်သည်။ Lab ကို ဤ command ဖြင့် run သည် —

```bash
python3 modules/11_linux_for_ai/lab.py
```

- exit code — `0`
- နောက်ဆုံးလိုင်း — `[PASS] All 6/6 exercises passed successfully.`
- run ၃ ကြိမ် နှိုင်းယှဉ်ပြီး output သည် byte အလိုက် တူညီသည်။

Lab သည် `chmod`၊ `chown`၊ `apt`၊ `df` နှင့် `du` ကို လုပ်ဆောင်ခြင်း မပြုပါ။ သတ်မှတ်ထားသည့်
စာသား အပေါ်တွင် ထို command များ၏ logic ကို တုပသည်။ ထို့ကြောင့် `sudo`၊ `apt` သို့မဟုတ် GPU
မရှိသည့် machine တွင်လည်း run နိုင်သည်။

---

## Exercise 1 — Permission bits

**အဖြေ** — permission bit သုံးစု၏ တန်ဖိုးကို ပေါင်းလိုက်သည့်အခါ octal digit ရသည်။ `r` = ၄၊
`w` = ၂၊ `x` = ၁ ဖြစ်သဖြင့် `rwx` = ၇၊ `rw-` = ၆၊ `r--` = ၄၊ `r-x` = ၅၊ `---` = ၀ ဖြစ်သည်။

```bash
ls -l train.py
# -rwxr-xr-- 1 user group 2048 Mar 19 10:00 train.py
chmod +x train.sh           # Make a script executable
chmod 755 deploy.sh         # Owner: full, others: read+execute
chmod 644 config.yaml       # Owner: read+write, others: read only
chown user:group file.txt   # Change who owns a file (needs sudo)
```

Python လမ်းကြောင်း (`exercise_1` — `permission_bits`) ရလဒ် —

```text
exercise_1 — permission_bits
  path           mode         octal   meaning
  train.sh       -rw-r--r--   644     script that is not executable yet
  deploy.sh      -rwxr-xr-x   755     script that is executable
  config.yaml    -rw-r--r--   644     config readable by everyone
  private.key    -rw-------   600     secret readable by the owner only
  dataset/       drwxr-xr-x   755     shared directory
  checkpoints/   drwx------   700     directory readable by the owner only
  round trip (octal -> symbolic) and the chmod command:
    chmod 644 train.sh       -> -rw-r--r--  (round trip: same)
    chmod 755 deploy.sh      -> -rwxr-xr-x  (round trip: same)
    chmod 644 config.yaml    -> -rw-r--r--  (round trip: same)
    chmod 600 private.key    -> -rw-------  (round trip: same)
    chmod 755 dataset/       -> drwxr-xr-x  (round trip: same)
    chmod 700 checkpoints/   -> drwx------  (round trip: same)
  symbolic changes applied by hand:
    -rw-r--r--   a+x    -> -rwxr-xr-x  0755   chmod +x train.sh  -> execute for all classes
    -rwxrwxrwx   o-w    -> -rwxrwxr-x  0775   chmod o-w shared.sh  -> drop other's write bit
    -rw-rw-rw-   go-w   -> -rw-r--r--  0644   chmod go-w team.txt  -> owner writes only
    -rwxr-xr-x   u+w    -> -rwxr-xr-x  0755   chmod u+w deploy.sh  -> owner gets write back
[OK] exercise_1 — converted 6 modes between symbolic and octal
```

ရှင်းလင်းချက် — `train.sh` သည် `644` (owner ဖတ်/ရေးသာ၊ run မရ) ဖြစ်သဖြင့် `./train.sh` သည်
"Permission denied" ပေးသည်။ `a+x` ကို ကျင့်သုံးလိုက်ပါက `755` ဖြစ်လာ၍ run နိုင်သည် —
ဤအချက်သည် source lesson ၏ `chmod +x train.sh` နှင့် တူညီသည် (source တွင် ဖော်ပြသည့်အတိုင်း
`chmod +x` သည် execute bit ကို ဖြည့်သည်)။ `go-w` သည် group နှင့် other ၏ write bit ကို ဖျောက်သဖြင့်
`rw-rw-rw-` သည် `rw-r--r--` (= `644`) ဖြစ်လာသည်။

---

## Exercise 2 — Diagnose "Permission denied"

**အဖြေ** — စစ်ဆေးသည့် အစဉ်သည် — `ls -la` ဖြင့် mode/owner/group ဖတ်၊ `whoami` နှင့် နှိုင်းယှဉ်၍
class (user/group/other) ဆုံးဖြတ်၊ ထို class တွင် လိုအပ်သည့် bit ရှိ/မရှိ စစ်။

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

Python လမ်းကြောင်း (`exercise_2` — `diagnose_permission_denied`) ရလဒ် —

```text
exercise_2 — diagnose_permission_denied
  ls -la on the box:
    -rw-r--r-- 1 ubuntu ubuntu   512 Mar 19 10:00 train.sh
    -rw-r--r-- 1 root   root     640 Mar 19 10:00 setup_gpu.sh
    -rw-r--r-- 1 ubuntu ubuntu  1280 Mar 19 10:00 config.yaml
    -rw------- 1 ubuntu ubuntu  1679 Mar 19 10:00 id_rsa
    -rw-r----- 1 ubuntu lab      2048 Mar 19 10:00 shared_report.csv
    drwxr-xr-x 2 root   root    4096 Mar 19 10:00 checkpoints
  checks (user ubuntu, group ubuntu, unless noted):
    ./train.sh           -rw-r--r--   execute  as ubuntu  class user   bits rw-  -> Permission denied
      fix: chmod +x train.sh
    ./setup_gpu.sh       -rw-r--r--   execute  as ubuntu  class other  bits r--  -> Permission denied
      fix: sudo chmod +x setup_gpu.sh
    /data/checkpoints    drwxr-xr-x   write    as ubuntu  class other  bits r-x  -> Permission denied
      fix: sudo chown -R ubuntu:ubuntu /data/checkpoints
    /data/checkpoints    drwxr-xr-x   enter    as ubuntu  class other  bits r-x  -> allowed
    ./id_rsa             -rw-------   read     as ubuntu  class user   bits rw-  -> allowed
    ./config.yaml        -rw-r--r--   read     as ubuntu  class user   bits rw-  -> allowed
    ./shared_report.csv  -rw-r-----   read     as guest   class group  bits r--  -> allowed
  denied cases   : 3
  distinct fixes : 3
    $ chmod +x train.sh
    $ sudo chmod +x setup_gpu.sh
    $ sudo chown -R ubuntu:ubuntu /data/checkpoints
  rule: 'Permission denied' means the class that applies to you has no r/w/x bit for the action - chmod fixes bits, chown fixes the owner, sudo only borrows root for one command.
[OK] exercise_2 — diagnosed 3 denials and listed 3 fixes
```

ရှင်းလင်းချက် — အခြေအနေ ၇ ခုအနက် ၃ ခု ကျရှုံးသည်။

- `./train.sh` — မိမိ (ubuntu) သည် owner ဖြစ်သော်လည်း `rw-` တွင် `x` မရှိပါ။ ဖြေရှင်းချက်သည်
  `chmod +x train.sh` ဖြစ်သည်။
- `./setup_gpu.sh` — owner သည် root ဖြစ်သဖြင့် မိမိသည် other class ဖြစ်သည်။ other တွင် `r--`
  သာ ရှိသည်။ fix နှစ်မျိုး ရှိသည် — `sudo chmod +x setup_gpu.sh` (bit ဖြည့်) သို့မဟုတ်
  `sudo chown ubuntu:ubuntu setup_gpu.sh` (owner ပြောင်း)။
- `/data/checkpoints` ထဲ **ဖိုင် ရေးခြင်း** — directory သည် root ပိုင်၊ mode `drwxr-xr-x` ဖြစ်သဖြင့်
  other တွင် `r-x` သာ ရှိသည်။ write အတွက် `w` လိုသဖြင့် denied ဖြစ်သည်။ fix သည်
  `sudo chown -R ubuntu:ubuntu /data/checkpoints` ဖြစ်သည်။
- ထို directory ထဲ **ဝင်ခြင်း** (`enter`) သည် other ၏ `x` bit ဖြင့် ခွင့်ပြုသည် — `cd` လုပ်နိုင်သည်။
  ထို့ကြောင့် list လုပ်ခြင်း နှင့် ဖိုင် ရေးခြင်း ကွာခြားချက်ကို ခွဲခြားရမည်။
- `./shared_report.csv` — မိမိ မဟုတ်သည့် အသုံးပြုသူ (guest) ဖြစ်သော်လည်း `lab` group တွင် ပါဝင်သဖြင့်
  group class `r--` ဖြင့် ဖတ်နိုင်သည်။

---

## Exercise 3 — Disk report

**အဖြေ** — `df -h` က capacity/used/avail/percent ကို တစ်လိုင်းစီ၊ `du -sh` က size/path ကို
တစ်လိုင်းစီ ပေးသည်။ `tmpfs` သည် အမှတ်တကယ် drive မဟုတ်သဖြင့် စုစုပေါင်း တွက်ရာတွင် ချန်လှပ်သည်။

```bash
df -h                       # Disk usage for all mounted drives
df -h /home                 # Disk usage for /home specifically
du -sh *                    # Size of each item in current directory
du -sh ~/.cache             # pip and huggingface models land here
du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20
pip cache purge             # Clear pip cache
sudo apt clean              # Clear apt cache
```

Python လမ်းကြောင်း (`exercise_3` — `disk_report`) ရလဒ် —

```text
exercise_3 — disk_report
  df -h (as printed by the box):
    Filesystem         Size   Used  Avail  Use% Mounted on
    /dev/root           98G    64G    33G   65% /
    tmpfs              7.8G      0   7.8G    0% /dev/shm
    /dev/nvme0n1p2     1.8T   1.7T   132G   93% /data
  real file systems (tmpfs excluded): 2
    capacity 1.9T  used 1.8T  available 165G
  crowded: /data at 93% - free space in /data before the next download
  du -sh output, largest first:
    12G      /data/checkpoints
    2.4G     /data/tokenized
    1.1G     /home/ubuntu/.cache
    340M     /home/ubuntu/.cache/pip
    156M     /home/ubuntu/miniconda3
    0        /data/empty
  top 3 space hogs: 12G /data/checkpoints, 2.4G /data/tokenized, 1.1G /home/ubuntu/.cache
  tip from the lesson: du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20
[OK] exercise_3 — reported 3 file systems and 6 du entries
```

ရှင်းလင်းချက် — `df -h` မှ entry ၃ ခု ရသည်။ `tmpfs` ကို ချန်လှပ်ပါက အမှတ်တကယ် file system
၂ ခု (root နှင့် `/data`) ကျန်သည်။ စုစုပေါင်း capacity သည် `98G` + `1.8T` = `1.9T` ဖြစ်သည်
(လူဖတ်နိုင်သည့် ပုံစံဖြင့် လုံးဝန်းသည်)။ `/data` သည် 93% ရှိသဖြင့် ၈၅% သတိပေးချက် လိုင်းကို
ဖြတ်သည် — checkpoint အဟောင်းများကို ရှာပြီး ရှင်းရမည်။ `du -sh` ၏ အကြီးဆုံး ၃ ခုသည်
checkpoint၊ tokenized dataset နှင့် pip cache ဖြစ်သည်။

---

## Exercise 4 — apt install plan

**အဖြေ** — GPU box အသစ် တစ်ခုအတွက် အစဉ်သည် — `whoami` → `sudo apt update` →
`sudo apt install -y <package ၈ ခု>` → `apt list --installed` → `nvidia-smi` → `sudo apt clean`။
`apt update` ကို မဖြစ်မနေ ပထမ လုပ်ရမည်။

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
sudo apt clean
```

Python လမ်းကြောင်း (`exercise_4` — `apt_install_plan`) ရလဒ် —

```text
exercise_4 — apt_install_plan
  fresh GPU box, in this order:
    1. [user] whoami
       check which user you are before anything else
    2. [sudo] sudo apt update
       refresh the package list - always first
    3. [sudo] sudo apt install -y build-essential git curl wget tmux htop unzip python3-venv
       install the whole fresh-box set in one shot
    4. [user] apt list --installed
       confirm the packages are present
    5. [user] nvidia-smi
       confirm driver and GPU are visible
    6. [sudo] sudo apt clean
       clear the apt cache when disk runs low
  packages in the install step (8):
    build-essential  C compiler, make and friends — many Python packages need it
    git              clone repositories
    curl             HTTP downloads and API calls
    wget             file downloads
    tmux             terminal multiplexer — keeps training alive after a disconnect
    htop             interactive process viewer
    unzip            expand zip archives such as datasets
    python3-venv     built-in virtual environments
  verification: apt list --installed | grep -c for the set
    missing after install: none
    still missing on a box with only git: ['build-essential', 'htop', 'python3-venv', 'tmux', 'unzip', 'wget']
[OK] exercise_4 — built a 6-step apt plan for 8 packages
```

ရှင်းလင်းချက် — `sudo` လိုသည့် အဆင့်သည် ၃ ခု ဖြစ်သည် (`apt update`၊ `apt install`၊
`apt clean`)။ `whoami`၊ `apt list --installed` နှင့် `nvidia-smi` သည် sudo မလိုပါ။
စစ်ဆေးသည့် လုပ်ငန်းစဉ်သည် `apt list --installed` output တွင် package စာရင်း အားလုံး
ပါ/မပါ ကို စစ်သည် — `git` နှင့် `curl` သာ ရှိသည့် box တွင် ၆ ခု ကျန်နေသည်။

---

## Exercise 5 — macOS vs Linux

**အဖြေ** — macOS မှ Linux သို့ ကူးသည့်အခါ ကွာခြားချက် ၈ ခု ရှိသည်။ trap တိုင်းသည်
remote GPU box ပေါ်တွင် အလုပ် ရပ်စေနိုင်သည်။

```bash
brew install htop            # command not found -> sudo apt install htop
open file.txt                # command not found -> xdg-open, or cat / less
sed -i '' 's/a/b/' config.yaml   # GNU sed takes the empty string as a file name
sed -i 's/a/b/' config.yaml      # the Linux form
echo $SHELL                  # most servers use bash, not zsh
ls Model.py model.py         # on Linux these are two different files
file script.sh               # "with CRLF line terminators" -> dos2unix script.sh
```

| macOS | Linux | သတိထားရမည့် အချက် |
|---|---|---|
| `brew install` | `sudo apt install` | package အမည် တစ်ခါတစ်ရံ မတူပါ |
| `open file.txt` | `xdg-open file.txt` | remote box တွင် GUI မရှိပါ — `cat` ကို သုံးရမည် |
| `pbcopy` / `pbpaste` | မရှိပါ | SSH အပေါ်တွင် clipboard မရပါ |
| `~/.zshrc` | `~/.bashrc` | rc ဖိုင် မှားလျှင် alias အလုပ်မလုပ်ပါ |
| `/opt/homebrew/` | `/usr/bin/`, `/usr/local/bin/` | binary လမ်းကြောင်း မတူပါ |
| `sed -i '' 's/a/b/' file` | `sed -i 's/a/b/' file` | macOS သည် အလွတ် string လိုသည် |
| case-insensitive | case-sensitive | `Model.py` နှင့် `model.py` သည် ဖိုင် နှစ်ခု ဖြစ်သည် |
| line endings `\n` | line endings `\n` | Windows ၏ `\r\n` သည် bash script ကို ပျက်စေသည် |

Python လမ်းကြောင်း (`exercise_5` — `macos_vs_linux`) ရလဒ် —

```text
exercise_5 — macos_vs_linux
  macOS                          Linux                          trap
  ------------------------------ ------------------------------ ----------------------------------------------
  brew install htop              sudo apt install htop          package names differ
  open file.txt                  xdg-open file.txt              no GUI on a remote box - use cat or less
  pbcopy, pbpaste                not available                  no clipboard over SSH
  ~/.zshrc                       ~/.bashrc                      aliases written in the wrong rc file never load
  /opt/homebrew/                 /usr/bin/, /usr/local/bin/     binaries live in different directories
  sed -i '' 's/a/b/' file        sed -i 's/a/b/' file           macOS sed needs an empty string after -i, Linux does not
  case-insensitive file system   case-sensitive file system     Model.py and model.py are two different files on Linux
  line endings \n                line endings \n                Windows \r\n breaks bash scripts - run dos2unix
  traps worth memorising (8):
     1. Model.py and model.py are two different files on Linux
     2. Windows \r\n breaks bash scripts - run dos2unix
     3. aliases written in the wrong rc file never load
     4. binaries live in different directories
     5. macOS sed needs an empty string after -i, Linux does not
     6. no GUI on a remote box - use cat or less
     7. no clipboard over SSH
     8. package names differ
  most common tripping points on a remote box:
    1. a script that runs on macOS but is not executable on Linux
       -> chmod +x script.sh
    2. an alias that does nothing -> it is in ~/.zshrc, not ~/.bashrc
    3. a sed one-liner that fails -> remove the empty string after -i
    4. a missing import of a file that only differs in letter case
[OK] exercise_5 — tabulated 8 macOS-to-Linux differences
```

ရှင်းလင်းချက် — ဇယား၏ လိုင်း ၈ ခုသည် source lesson ၏ ကွာခြားချက် ဇယားနှင့် တူညီသည်။
တတိယ ကော်လံသည် ထို ကွာခြားချက်မှ ဖြစ်ပေါ်သည့် အမှန်တကယ် ကျရှုံးမှုကို ဖော်ပြသည်။
လက်တွေ့တွင် အဖြစ်အများဆုံး ကျရှုံးမှု လေးခုကို သီးခြား ဖော်ပြထားသည် — executable bit၊
rc ဖိုင်၊ `sed -i` နှင့် case sensitivity။

---

## Exercise 6 — Linux operations report

**အဖြေ** — report သည် exercise ၁–၅ ၏ ရလဒ်ကို တစ်နေရာတည်းတွင် စုသည်။

```bash
whoami
ls -la
df -h
du -sh ~/.cache
apt list --installed | wc -l
```

Python လမ်းကြောင်း (`exercise_6` — `linux_ops_report`) ရလဒ် —

```text
exercise_6 — linux_ops_report
  ================ Linux operations report ================
  permissions : 6 modes converted, 3 denied, 3 fixes
    octal modes: train.sh=644, deploy.sh=755, config.yaml=644, private.key=600, dataset/=755, checkpoints/=700
    denials    : ./train.sh (execute); ./setup_gpu.sh (execute); /data/checkpoints (write)
    fixes      : chmod +x train.sh; sudo chmod +x setup_gpu.sh; sudo chown -R ubuntu:ubuntu /data/checkpoints
  disk        : 3 file systems, capacity 1.9T, used 1.8T, available 165G
    crowded    : /data (93%)
    biggest dir: 12G /data/checkpoints
  packages    : 6 steps, 8 packages in the install step
    first step : whoami
    install    : sudo apt install -y build-essential git curl wget tmux htop unzip python3-venv
  porting     : 8 macOS-to-Linux differences tracked
  verdict     : 3 mode(s) to fix with chmod, 1 path(s) to reclaim on /data, 8 package(s) to install
  =========================================================
[OK] exercise_6 — operations report over 3 denials and 3 file systems
```

ပြီးနောက် runner သည် ဤလိုင်းကို print ၍ exit 0 ဖြင့် ပြီးသည် —

```text
[PASS] All 6/6 exercises passed successfully.
```

ရှင်းလင်းချက် — report ရှိ ကိန်းဂဏန်း တိုင်းသည် exercise ၁–၅ ၏ ရလဒ်နှင့် ကိုက်ညီရမည်။
`assert` များသည် ထို ကိုက်ညီမှုကို စစ်သည် — mode ၆ ခု၊ denied ၃ ခု၊ fix ၃ ခု၊ file system
၃ ခု၊ ၈၅% ကျော် ၁ ခု၊ အကြီးဆုံး directory `/data/checkpoints`၊ အစီအစဉ် ၆ အဆင့်။
`available 165G` သည် `Avail` ကော်လံ နှစ်ခု၏ ပေါင်းလဒ် ဖြစ်သည် (`33G` + `132G`)။
`df -h` သည် အရွယ်အစား တစ်ခုစီကို သီးခြား လုံးဝန်းသဖြင့် `Use%` သည် ပြန်တွက်သည့်
တန်ဖိုးနှင့် အနည်းငယ် ကွာနိုင်သည် — report တွင် `df` ပြသည့် `Use%` ကို ယူထားသည်။
