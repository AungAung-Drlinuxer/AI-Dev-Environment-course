# Module 11 — Linux for AI

**Type:** Learn · **Time:** ~30 min · **Prerequisites:** Phase 0, Lesson 01

## ရည်ရွယ်ချက်

ဤ module သည် cloud GPU box တစ်ခုပေါ်တွင် AI အလုပ် လုပ်ရန် လိုအပ်သည့် Linux ကျွမ်းကျင်မှုကို သင်ပေးသည်။
ပြီးစီးပါက —

- Linux file system ၏ တည်ဆောက်ပုံ (`/`၊ `home/`၊ `tmp/`၊ `usr/`၊ `etc/`၊ `var/log/`၊ `mnt/`၊ `proc/`) ကို နားလည်မည်။
- `pwd`၊ `ls -la`၊ `cd`၊ `mkdir -p`၊ `cp -r`၊ `mv`၊ `rm`၊ `cat`၊ `head`၊ `tail -f`၊ `less`၊ `grep`၊ `find`
  ဖြင့် ဖိုင် လုပ်ဆောင်ချက်များကို command line မှ လုပ်နိုင်မည်။
- `ls -la` ၏ mode ကို ဖတ်၍ `chmod` (symbolic နှင့် octal) နှင့် `chown` ဖြင့် "Permission denied" ကို
  ဖြေရှင်းနိုင်မည်။
- `apt update` နှင့် `apt install -y` ဖြင့် GPU box အသစ် တစ်ခုကို package ၈ ခုဖြင့် အသင့် ဖြစ်စေနိုင်မည်။
- macOS မှ Linux သို့ ကူးသည့်အခါ ကျရှုံးမှု အဖြစ်များသည့် နေရာ ၈ ခုကို ကြိုတင် သိရှိမည်။

## လိုအပ်ချက် (Prerequisites)

- ကိုယ်ပိုင် machine (Linux၊ macOS သို့မဟုတ် WSL2) နှင့် terminal တစ်ခု။
- Phase 0 ၏ Lesson 01 (Dev Environment) ကို ပြီးစီးထားခြင်း — source lesson ၏ prerequisite အတိုင်း။
- Python အခြေခံ (function၊ list၊ string၊ f-string၊ `import`) — `lab.py` ကို ဖတ်ရန်။
- **sudo၊ `apt` နှင့် GPU သည် မလိုအပ်ပါ။** ဤ module ၏ lab သည် offline ဖြစ်သည်။

## Subtopic စာရင်း

1. File System Layout — root `/` အောက်ရှိ directory များ နှင့် AI အလုပ်နှင့် ဆက်စပ်မှု
2. Essential Commands — လမ်းကြောင်း ရွှေ့ခြင်း၊ ဖိုင် နှင့် directory၊ ဖိုင် ဖတ်ခြင်း၊ ရှာဖွေခြင်း
3. Permissions — owner၊ group၊ other၊ `r`/`w`/`x` bit၊ symbolic နှင့် octal mode၊ `chmod`၊ `chown`
4. Package Management (`apt`) — `apt update`၊ `apt install -y`၊ `apt list --installed`၊ `apt remove`၊ `sudo apt clean`
5. Users and sudo — `whoami`၊ `sudo`၊ `sudo su` နှင့် root အဖြစ် မလုပ်သင့်သည့် အကြောင်းရင်း
6. Processes and systemd — `htop`၊ `ps aux | grep python`၊ `kill`၊ `kill -9`၊ `nvidia-smi`၊ `systemctl start/stop/restart/status/enable`
7. Disk Space — `df -h`၊ `du -sh`၊ `du -h --max-depth=1 / | sort -hr | head -20`၊ `pip cache purge`
8. Networking — `wget`၊ `curl -O`၊ `curl -s | python3 -m json.tool`၊ `scp`၊ `rsync -avz --progress`
9. tmux: Keep Sessions Alive — `new -s`၊ detach (`Ctrl+B` ထို့နောက် `d`)၊ `ls`၊ `attach -t`၊ pane ခွဲခြင်း
10. WSL2 for Windows Users — `wsl --install -d Ubuntu-24.04`၊ `/mnt/c/Users/YourName/`၊ GPU passthrough
11. Gotchas: macOS to Linux — package manager၊ `open`၊ clipboard၊ rc ဖိုင်၊ binary လမ်းကြောင်း၊ `sed -i`၊
    case sensitivity၊ line endings
12. Quick Reference Card — source lesson ၏ အုပ်စုအလိုက် command စာရင်း

## Exercise တစ်လိုင်းချင်း

1. **Exercise 1 — Permission bits (`permission_bits`)** — symbolic mode (`-rwxr-xr--`) နှင့် octal mode
   (`754`) ကို အပြန်အလှန် ပြောင်းပြီး `chmod +x`၊ `chmod go-w` ကဲ့သို့ symbolic change များကို
   တွက်သည်။
2. **Exercise 2 — Diagnose "Permission denied" (`diagnose_permission_denied`)** — `ls -la` output မှ
   owner၊ group နှင့် bit ကို ဖတ်၍ မည်သည့် class က ဆုံးဖြတ်သည်၊ ခွင့်ပြု/မပြု၊ မည်သည့် fix
   (`chmod`၊ `chown`၊ `sudo`) လိုသည် ကို ဆုံးဖြတ်သည်။
3. **Exercise 3 — Disk report (`disk_report`)** — `df -h` နှင့် `du -sh` စာသားကို parse လုပ်၍
   capacity၊ သုံးပြီး ပမာဏ၊ ကျန်နေသည့် ပမာဏ၊ ၈၅% ကျော်သည့် mount နှင့် အကြီးဆုံး directory ၃ ခုကို ပြသည်။
4. **Exercise 4 — apt install plan (`apt_install_plan`)** — GPU box အသစ် တစ်ခုအတွက် command အစဉ် ၆ ခုနှင့်
   source lesson ၏ package ၈ ခုကို အကြောင်းပြချက်နှင့်တကွ တည်ဆောက်သည်။
5. **Exercise 5 — macOS vs Linux (`macos_vs_linux`)** — source lesson ၏ ကွာခြားချက် ၈ ခုကို ဇယားအဖြစ်
   စီ၍ remote box တွင် ကျရှုံးမှု အဖြစ်များသည့် နေရာများကို ဖော်ပြသည်။
6. **Exercise 6 — Linux operations report (`linux_ops_report`)** — အထက်ပါ အဆင့် အားလုံး၏ ရလဒ်ကို
   permission၊ disk၊ package နှင့် porting ဟူ၍ အစီရင်ခံစာ တစ်ခုအဖြစ် စုစည်းသည်။

## ဖိုင်စာရင်း

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic စာရင်း၊ exercise စာရင်း၊ ဖိုင်စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ (file system၊ permissions၊ apt၊ disk၊ networking၊ tmux၊ WSL2၊ gotchas၊ figure ၃ ခု၊ self-check ၅ ခု) |
| `exercise.md` | exercise ၆ ခု — လိုအပ်ချက်၊ အဆင့်များ၊ အောင်မြင်မှု စစ်ဆေးနည်း |
| `solution.md` | အဖြေ ၆ ခု — တကယ် run ရလဒ် နှင့်တကွ |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## Lab ကို run ခြင်း

```bash
# repository root မှ
python3 modules/11_linux_for_ai/lab.py
```

ဤ lab သည် **standard library သာ** သုံးသည်။ network၊ `sudo`၊ `apt`၊ Docker၊ GPU မလိုအပ်ပါ။
`chmod`၊ `chown`၊ `apt`၊ `df` နှင့် `du` ကို လုပ်ဆောင်ခြင်း မပြုဘဲ သတ်မှတ်ထားသည့် စာသား အပေါ်တွင်
တုပစစ်ဆေးသည်။ ရလဒ်သည် **deterministic** ဖြစ်သည် — run တိုင်း တူညီသည်။

**သတိ** — command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
