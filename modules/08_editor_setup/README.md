# Module 08 — Editor Setup

## ရည်ရွယ်ချက် (Goal)

AI engineering လုပ်ငန်းစဉ် တစ်ခုလုံးအတွက် editor ကို **တစ်ကြိမ်တည်း မှန်ကန်စွာ ချိန်ညှိခြင်း** ကို
သင်ပေးသည်။ ဤ Module ပြီးစီးလျှင် —

- VS Code ကို ထည့်သွင်းခြင်း၊ version ကို terminal မှ စစ်ခြင်းကို လုပ်နိုင်သည်။
- Python၊ Jupyter၊ linting နှင့် Remote SSH အတွက် essential extension ၈ ခုကို `code --install-extension`
  ဖြင့် ထည့်နိုင်ပြီး `code --list-extensions` ဖြင့် ပြန်စစ်နိုင်သည်။
- Format-on-save၊ type checking နှင့် notebook output scrolling ကို `settings.json` တွင်
  ချိန်ညှိနိုင်သည်။
- Remote SSH ဖြင့် remote GPU machine ပေါ်တွင် local ကဲ့သို့ ဖိုင် ပြင်ခြင်း၊ terminal run ခြင်း၊
  debug လုပ်ခြင်း ကို တည်ဆောက်နိုင်သည်။
- VS Code၊ Cursor၊ Windsurf နှင့် Neovim ကို လိုအပ်ချက် အလိုက် နှိုင်းယှဉ်၍ ရွေးချယ်နိုင်သည်။

အခန်း အရှည် ~၂၀ မိနစ်၊ အမျိုးအစား **Build** ဖြစ်သည်။

## လိုအပ်ချက် (Prerequisites)

- Phase 0၊ Module 01 (Dev Environment) ပြီးစီးထားခြင်း — terminal အခြေခံ အသုံးပြုနိုင်ခြင်း လိုသည်။
- Linux၊ macOS သို့မဟုတ် Windows + WSL2 တစ်ခုခု ရှိခြင်း။
- Remote SSH အဆင့်အတွက် remote machine(cloud VM သို့မဟုတ် lab server)တစ်ခု ရှိလျှင် ပိုကောင်းသည်။
  **မရှိလျှင် လည်း ဖြစ်သည်** — `~/.ssh/config` entry တည်ဆောက်ခြင်းကို ကိုယ်တိုင် run နိုင်သည်။
- GPU မလိုအပ်ပါ။ Internet မလိုအပ်ပါ (lab သည် offline ဖြစ်သည်)။

> command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. **Step 1: Install VS Code** — installer ရယူခြင်း၊ `code --version` ဖြင့် စစ်ခြင်း၊ macOS တွင် `code`
   command ကို PATH ထဲ ထည့်ခြင်း။
2. **Step 2: Install Essential Extensions** — `code --install-extension` ဖြင့် extension ၈ ခု ထည့်ခြင်း၊
   `code/vscode/extensions.json` ကို `.vscode/extensions.json` အဖြစ် အသုံးပြုခြင်း။
3. **Step 3: Configure Settings** — `python.analysis.typeCheckingMode`၊ `editor.formatOnSave`၊
   `editor.rulers`၊ `notebook.output.scrolling`၊ `files.autoSave`။
4. **Step 4: Terminal Integration** — integrated terminal profile၊ font size၊ scrollback နှင့်
   shortcut များ။
5. **Step 5: Remote Development (SSH into GPU Boxes)** — `ssh-keygen`၊ `ssh-copy-id`၊ `~/.ssh/config`
   host entry နှင့် `Remote-SSH: Connect to Host`။
6. **Alternatives** — Cursor၊ Windsurf နှင့် Vim/Neovim ၏ tradeoff များ။

## Exercise တစ်လိုင်းချင်း

| # | Exercise | တစ်လိုင်း အနှစ်ချုပ် | Lab function |
|---|---|---|---|
| 1 | settings.json ကို စစ်ဆေးခြင်း | VS Code `settings.json` ကို parse လုပ်ပြီး မဖြစ်မနေ key ၅ ခု၏ တန်ဖိုး မှန်/မမှန် ဆုံးဖြတ်ခြင်း | `exercise_1` (`parse_settings`) |
| 2 | Extension စာရင်း နှိုင်းယှဉ်ခြင်း | လိုအပ်သည့် extension ၈ ခုကို `code --list-extensions` output နှင့် နှိုင်းယှဉ်၍ ချို့နေသည့် အရာ ရှာခြင်း | `exercise_2` (`extension_diff`) |
| 3 | Remote SSH host entry တည်ဆောက်ခြင်း | `~/.ssh/config` အတွက် host entry ကို spec မှ တည်ဆောက်၍ လိုင်းတိုင်း စစ်ခြင်း | `exercise_3` (`ssh_config_entry`) |
| 4 | Format-on-save မူဝါဒ | language အလိုက် format-on-save ဖွင့်/ပိတ် နှင့် formatter ကို ဆုံးဖြတ်ခြင်း | `exercise_4` (`format_on_save_policy`) |
| 5 | Editor ရွေးချယ်မှု ဇယား | VS Code / Cursor / Windsurf / Neovim ကို လိုအပ်ချက် ၅ မျိုးဖြင့် အမှတ်ပေး၍ အဆင့်သတ်ခြင်း | `exercise_5` (`editor_choice_matrix`) |
| 6 | Setup အစီရင်ခံစာ | စစ်ဆေးချက် ၅ ခုကို စုစည်း၍ READY / INCOMPLETE နှင့် exit code ကို ဆုံးဖြတ်ခြင်း | `exercise_6` (`editor_report`) |

Exercise အပြည့်အစုံ နှင့် အောင်မြင်မှု စစ်နည်းကို `exercise.md` တွင် ဖတ်ပါ။ အဖြေနှင့် တကယ့်
run ရလဒ်ကို `solution.md` တွင် ဖတ်ပါ။

## Lab ကို run ခြင်း

```bash
python3 modules/08_editor_setup/lab.py
```

Lab သည် Python standard library သာ အသုံးပြုသည်။ Network၊ VS Code၊ GPU မလိုအပ်ပါ။ `settings.json`
ကို temporary directory တွင် ကိုယ်တိုင် ရေး၍ parse လုပ်သည်။ `code --list-extensions` ၏ output ကို
စာသား စာရင်း အဖြစ် တုပသည်။ ရလဒ်သည် deterministic ဖြစ်သည်။ Exit code 0 နှင့် အောက်ပါ လိုင်း
ထွက်ရမည်။

```
[PASS] All 6/6 exercises passed successfully.
```

## ဖိုင်စာရင်း

| ဖိုင် | အကြောင်းအရာ |
|---|---|
| `README.md` | ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic စာရင်း၊ exercise စာရင်း၊ ဖိုင်စာရင်း (ဤဖိုင်) |
| `explanation.md` | အဓိက သင်ခန်းစာ — ပြဿနာ၊ အလွှာ ၅ လွှာ၊ LSP၊ editor နှိုင်းယှဉ်ချက်၊ လက်တွေ့ ချိန်ညှိမှု၊ သတိထားရမည့် အချက်၊ self-check |
| `exercise.md` | exercise ၆ ခု — လိုအပ်ချက်၊ အဆင့်၊ အောင်မြင်မှု စစ်နည်း |
| `solution.md` | exercise ၆ ခု၏ အဖြေ၊ `settings.json` အပြည့်အစုံ နှင့် တကယ့် run ရလဒ် |
| `lab.py` | exercise ၆ ခုကို `def exercise_1()` … `def exercise_6()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## ဆက်စပ် Module များ

- **Module 05 (Jupyter Notebooks)** — notebook ကို VS Code အတွင်း run ခြင်းနှင့် ဆက်စပ်သည်။
- **Module 10 (Terminal & Shell)** — integrated terminal နှင့် SSH ကို နက်ရှိုင်းစွာ ဆက်လက် ရှင်းပြသည်။
- **Module 12 (Debugging & Profiling)** — `ms-python.debugpy` ဖြင့် VS Code debugger ကို အသုံးပြုသည်။
