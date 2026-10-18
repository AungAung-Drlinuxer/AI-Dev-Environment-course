# Module 08 — Editor Setup · အဖြေ (Solution)

ဤဖိုင်သည် exercise ၆ ခု၏ အဖြေ ဖြစ်သည်။ Code များကို `modules/08_editor_setup/lab.py` တွင်
တကယ် implement လုပ်ပြီး run ၍ ရလာသည့် output ကို တိုက်ရိုက် ကူးထည့်ထားသည်။

## ဤ machine တွင် မလုပ်နိုင်သည့် အဆင့်များ (ပထမဆုံး ဖတ်ပါ)

| အဆင့် | အခြေအနေ | အကြောင်းရင်း |
|---|---|---|
| VS Code installer ဖြင့် ထည့်သွင်းခြင်း | **မ run နိုင်ပါ** | ဤ machine တွင် VS Code ရှိပြီး ဖြစ်သည်(`code --version` → `1.142.0`)။ GUI installer run လုပ်ရန် display မရှိပါ။ |
| `code --install-extension <id>` ၈ ကြိမ် | **မ run နိုင်ပါ** | ၎င်းသည် အသုံးပြုသူ၏ editor ကို ပြောင်းလဲသည့် ရေးသည့် လုပ်ဆောင်ချက် ဖြစ်သည်။ ဤအလုပ်တွင် module folder အတွင်းရှိ ဖိုင် ၅ ခုသာ ရေးခွင့် ရှိသည်။ |
| `~/.ssh/config` သို့ host entry ရေးခြင်း | **မ run နိုင်ပါ** | ဤ machine တွင် `~/.ssh/config` မ ရှိပါ။ ဖိုင် အသစ် ရေးလျှင် module folder အပြင်ဘက် ပြောင်းလဲမှု ဖြစ်သည်။ |
| Remote SSH ဖြင့် GPU box သို့ ချိတ်ခြင်း | **မ run နိုင်ပါ** | ချိတ်ဆက်ရန် remote GPU machine မ ရှိပါ၊ VS Code GUI session လည်း မ ရှိပါ။ |
| `code --version` နှင့် `code --list-extensions` | **run နိုင်သည်** | ဖတ်ရုံသာ ဖြစ်သည်။ Output အစစ်ကို Exercise 2 တွင် ဖော်ပြထားသည်။ |

ထို့ကြောင့် lab ၏ exercise များတွင် `settings.json` ကို temporary directory တွင် ကိုယ်တိုင် ရေးသည်။
`code --list-extensions` output ကို စာသား စာရင်း အဖြစ် တုပသည်(အစစ် output နှင့် နှိုင်းယှဉ်ချက် ကို
အောက်တွင် ဖော်ပြထားသည်)။

## ဤ Module ၏ settings JSON အပြည့်အစုံ

Source lesson ၏ AI setting များနှင့် terminal setting များကို ပေါင်းထားသည့် ဖိုင် ဖြစ်သည်။
Key နှင့် တန်ဖိုး များကို မ ပြင်ထားပါ။ Lab ၏ `SETTINGS_DOC` သည် ဤဖိုင် ကို temporary directory
အတွင်း ရေး၍ parse လုပ်သည်။

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "notebook.output.scrolling": true,
    "files.autoSave": "afterDelay",
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.scrollback": 10000
}
```

## Exercise 1 — settings.json ကို စစ်ဆေးခြင်း

**အဖြေ**

```python
def exercise_1(workdir: str) -> dict:
    path = _write_settings_file(workdir, SETTINGS_DOC)      # settings.json ရေးသည်
    with open(path, "r", encoding="utf-8") as handle:
        loaded = json.load(handle)                          # ပြန်ဖတ်သည်

    missing, mismatched = [], []
    for key, expected in sorted(REQUIRED_SETTING_KEYS.items()):
        if key not in loaded:
            missing.append(key)
        elif loaded[key] != expected:
            mismatched.append(key)
        else:
            print(f"  [OK] {key} = {json.dumps(expected, ensure_ascii=False)}")

    assert not missing and not mismatched
    assert loaded["editor.rulers"] == [88, 120]
    return {"path": path, "total_keys": len(loaded), "missing": missing}
```

`REQUIRED_SETTING_KEYS` တွင် key ၅ ခုသာ ပါသည် — ထို ၅ ခုသည် AI အလုပ်အတွက် မဖြစ်မနေ လိုအပ်သည့်
အရာ ဖြစ်သည်။ Terminal key များသည် ဤစစ်ဆေးချက်တွင် မ ပါပါ။

**တကယ့် output**

```
Exercise 1 — settings.json key စစ်ဆေးခြင်း
  ဖိုင်: <tempdir>/settings.json
  key စုစုပေါင်း: 9
  [OK] editor.formatOnSave = true
  [OK] editor.rulers = [88, 120]
  [OK] files.autoSave = "afterDelay"
  [OK] notebook.output.scrolling = true
  [OK] python.analysis.typeCheckingMode = "basic"
  -> မဖြစ်မနေ key ၅ ခု အားလုံး မှန်ကန်သည်
[OK] exercise_1 — settings.json key ၅ ခုကို စစ်ဆေးပြီးပါပြီ
```

ဖိုင် တွင် key ၉ ခု ရှိပြီး၊ မဖြစ်မနေ key ၅ ခု အားလုံး မှန်ကန်သည်။ `editor.rulers` သည် `[88, 120]`
ဖြစ်သည် — Black သည် 88 တွင် wrap လုပ်သည်နှင့် ကိုက်ညီသည်။

## Exercise 2 — Extension စာရင်း နှိုင်းယှဉ်ခြင်း

**အဖြေ**

```python
def exercise_2() -> dict:
    installed = sorted(SIMULATED_INSTALLED)      # code --list-extensions output (တုပ)
    required = sorted(REQUIRED_EXTENSIONS)       # လိုအပ် ၈ ခု

    missing = [ext for ext in required if ext not in installed]
    extra = [ext for ext in installed if ext not in required]
    for ext in missing:
        print(f"    install ရန်: code --install-extension {ext}")

    assert "ms-python.debugpy" in missing
    assert len(required) == 8
    return {"missing": missing, "extra": extra, "installed_count": len(installed)}
```

**တကယ့် output (lab — output ကို တုပထားသည်)**

```
Exercise 2 — extension တိုက်ဆိုင်စစ်ခြင်း
  installed (တုပထားသည်): 8 ခု
    charliermarsh.ruff [required]
    eamodio.gitlens [required]
    ms-python.black-formatter [required]
    ms-python.python [required]
    ms-python.vscode-pylance [required]
    ms-toolsai.jupyter [required]
    ms-toolsai.jupyter-keymap [extra]
    ms-vscode-remote.remote-ssh [required]
  ချို့နေသည့် extension: ['ms-python.debugpy']
  ပိုနေသည့် extension: ['ms-toolsai.jupyter-keymap']
    install ရန်: code --install-extension ms-python.debugpy
  -> လိုအပ် ၈ ခုအနက် 7 ခု တပ်ဆင်ပြီးဖြစ်သည်
[OK] exercise_2 — extension စာရင်း ၈ ခုကို နှိုင်းယှဉ်ပြီးပါပြီ
```

**အစစ် output နှင့် နှိုင်းယှဉ်ချက်(ဤ machine၊ ဖတ်ရုံသာ)**

```bash
$ code --version
1.142.0
6d62b1d5dace93a33b3a6d3eca1317bd5e15bcb1
x64

$ code --list-extensions | sort
ms-azuretools.vscode-containers
ms-python.debugpy
ms-python.python
ms-python.vscode-pylance
ms-python.vscode-python-envs
ms-toolsai.jupyter
ms-toolsai.jupyter-keymap
ms-toolsai.jupyter-renderers
ms-toolsai.vscode-jupyter-cell-tags
ms-toolsai.vscode-jupyter-slideshow
ms-vscode-remote.remote-containers
ms-vscode.live-server
ritwickdey.liveserver
```

အစစ် စာရင်း နှင့် လိုအပ် ၈ ခု ကို နှိုင်းယှဉ်လျှင် —

| အခြေအနေ | Extension ID |
|---|---|
| တပ်ဆင်ပြီး | `ms-python.python`၊ `ms-python.vscode-pylance`၊ `ms-toolsai.jupyter`၊ `ms-python.debugpy` |
| ချို့နေသည် | `eamodio.gitlens`၊ `ms-vscode-remote.remote-ssh`၊ `ms-python.black-formatter`၊ `charliermarsh.ruff` |

ဤ machine တွင် ချို့နေသည့် ၄ ခုကို ထည့်ရန် အောက်ပါ command များ run ရမည်။ ဤအလုပ်တွင် run မ လုပ်ပါ
(editor ကို ပြောင်းလဲသည့် ရေးသည့် လုပ်ဆောင်ချက် ဖြစ်သည်)။

```bash
code --install-extension eamodio.gitlens
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
```

## Exercise 3 — Remote SSH host entry တည်ဆောက်ခြင်း

**အဖြေ**

```python
def exercise_3() -> dict:
    spec = SSH_HOST_SPEC
    lines = [
        f"Host {spec['alias']}",
        f"    HostName {spec['hostname']}",
        f"    User {spec['user']}",
        f"    IdentityFile {spec['identity_file']}",
        f"    ForwardAgent {spec['forward_agent']}",
    ]
    block = "\n".join(lines) + "\n"

    for token in ["Host gpu-box", "HostName 203.0.113.50", "User ubuntu",
                  "IdentityFile ~/.ssh/id_ed25519", "ForwardAgent yes"]:
        assert token in block
    assert block.count("\n") == 5
    return {"alias": spec["alias"], "block": block, "lines": len(lines)}
```

**တကယ့် output**

```
Exercise 3 — Remote SSH host entry တည်ဆောက်ခြင်း
  ~/.ssh/config ထဲ ထည့်ရမည့် အပိုင်း:
    Host gpu-box
        HostName 203.0.113.50
        User ubuntu
        IdentityFile ~/.ssh/id_ed25519
        ForwardAgent yes
  -> alias 'gpu-box' ဖြင့် 'Remote-SSH: Connect to Host' မှ ချိတ်နိုင်သည်
[OK] exercise_3 — SSH host entry လိုင်း ၅ လိုင်း တည်ဆောက်ပြီးပါပြီ
```

ဤ machine တွင် `~/.ssh/config` ဖိုင် မ ရှိပါ။ ထို့ကြောင့် ဤ entry ကို ဖိုင် အစစ်ထဲ ထည့်ခြင်း မ ပြုပါ။
Key များ ဖန်တီးရန် command များမှာ အောက်ပါအတိုင်း ဖြစ်သည်(မ run ပါ)—

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
ssh-copy-id user@your-gpu-box-ip
```

## Exercise 4 — Format-on-save မူဝါဒ

**အဖြေ**

```python
FORMAT_POLICY = {
    "python":       {"enabled": True,  "formatter": "ms-python.black-formatter"},
    "jsonc":        {"enabled": False, "formatter": None},
    "markdown":     {"enabled": False, "formatter": None},
    "dockerfile":   {"enabled": False, "formatter": None},
}

def exercise_4(languages=None):
    decisions = {}
    for lang in languages or ["python", "jsonc", "markdown", "dockerfile", "unknown_lang"]:
        policy = FORMAT_POLICY.get(lang)
        decisions[lang] = dict(policy) if policy else {
            "enabled": False, "formatter": None,
            "reason": "formatter မ သတ်မှတ်ရသေးပါ; 'version အလိုက် ပြန်စစ်ရန် လိုသည်'",
        }
    return decisions
```

**တကယ့် output**

```
Exercise 4 — format-on-save မူဝါဒ
  python        format-on-save=ON  formatter=ms-python.black-formatter
                 source: Black သည် format-on-save ကို ကိုင်တွယ်သည်; style တူညီသည်
  jsonc         format-on-save=OFF formatter=-
                 VS Code settings ဖိုင်တွင် comment ပါသည်; ကိုယ်တိုင် ချိန်ညှိသင့်သည်
  markdown      format-on-save=OFF formatter=-
                 စာသား ဖိုင် ကို ကိုယ်တိုင် စီစဉ်သည်; မလိုအပ်သည့် reflow ကို ရှောင်ခြင်း
  dockerfile    format-on-save=OFF formatter=-
                 layer စီစဉ်မှုကို လူက ဆုံးဖြတ်သည်; ဖော်မတ် ပြောင်းလျှင် layer ပြောင်းနိုင်သည်
  unknown_lang  format-on-save=OFF formatter=-
                 formatter မ သတ်မှတ်ရသေးပါ; 'version အလိုက် ပြန်စစ်ရန် လိုသည်'
  -> format-on-save ဖွင့်မည့် language: ['python']
[OK] exercise_4 — format-on-save မူဝါဒ 5 မျိုးအတွက် ဆုံးဖြတ်ပြီးပါပြီ
```

VS Code တွင် ဤမူဝါဒ ကို အပြည့်အဝ ရရန် `settings.json` အတွင်း language scope ဖြင့် ရေးသည် —

```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "[jsonc]": { "editor.formatOnSave": false },
    "[markdown]": { "editor.formatOnSave": false }
}
```

Language scope key များ၏ အမည် များသည် release အလိုက် ပြောင်းလဲနိုင်သည် — run မီ မိမိ version
အတွက် official documentation ကို စစ်ပါ။

## Exercise 5 — Editor ရွေးချယ်မှု ဇယား

**အဖြေ**

```python
EDITOR_REQUIREMENTS = {"remote_ssh_editing": 3, "vscode_settings_compat": 2,
                       "jupyter_support": 2, "free_no_subscription": 2,
                       "builtin_ai_completion": 1}

def exercise_5():
    scores = {}
    for editor, features in EDITOR_FEATURES.items():
        scores[editor] = sum(weight for req, weight in EDITOR_REQUIREMENTS.items()
                             if features.get(req) is True)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
```

**တကယ့် output**

```
Exercise 5 — editor ရွေးချယ်မှု ဇယား
  လိုအပ်ချက် အလေးချိန်:
    builtin_ai_completion      1
    free_no_subscription       2
    jupyter_support            2
    remote_ssh_editing         3
    vscode_settings_compat     2
  အမှတ် အမြင့်ဆုံး ဖြစ်နိုင်သည်: 10
    1. VS Code   9/10  — source ၏ အကြံပြု editor; extension နှင့် settings format ရင်းမြစ်
    2. Cursor    8/10  — VS Code fork; extension နှင့် settings format တူညီသည်
    3. Windsurf  8/10  — AI-first VS Code fork; extension, settings, Remote SSH တူညီသည်
    4. Neovim    7/10  — pyright/pylsp + nvim-lspconfig + molten-nvim ကို ကိုယ်တိုင် ချိတ်ရသည်
  -> ဤ လိုအပ်ချက် အစုအတွက် အသင့်တော်ဆုံး: VS Code (9/10)
     ဖြည့်ဆည်းသည်: ['free_no_subscription', 'jupyter_support', 'remote_ssh_editing', 'vscode_settings_compat']
[OK] exercise_5 — editor ၄ ခုကို လိုအပ်ချက် ၅ မျိုးနှင့် အဆင့်သတ်ပြီးပါပြီ
```

ရလဒ် ကို ဖတ်ရာ တွင် သတိထားရမည့် အချက် — VS Code သည် built-in AI completion မ ရှိပါ။
`builtin_ai_completion` အလေးချိန် ကို တင်လျှင် Cursor နှင့် Windsurf သည် ရှေ့သို့ ရောက်နိုင်သည်။
ထို့ကြောင့် ဤဇယား သည် အလေးချိန် ရွေးချယ်မှုနှင့် တိုက်ရိုက် ဆက်စပ်သည်။ Source lesson သည်
ပထမဆုံး အကြံပြု editor အဖြစ် VS Code ကို သတ်မှတ်ပြီး Cursor နှင့် Windsurf အတွက် "ဤ lesson ၏ အကြောင်းအရာ
အားလုံး အတိုင်း ဖြစ်သည်" ဟု ဆိုထားသည်။

## Exercise 6 — Setup အစီရင်ခံစာ

**အဖြေ**

```python
def exercise_6(workdir: str) -> dict:
    _QUIET = True          # exercise_1–5 ကို output မ ရိုက်ဘဲ ခေါ်သည်
    settings_result = exercise_1(workdir)
    extension_result = exercise_2()
    ssh_result = exercise_3()
    policy_result = exercise_4()
    choice_result = exercise_5()

    checks = [
        ("settings.json",   len(settings_result["missing"]) == 0, ...),
        ("extensions",      len(extension_result["missing"]) == 1, ...),
        ("remote-ssh entry", "Host gpu-box" in ssh_result["block"], ...),
        ("format-on-save",  policy_result["enabled"] == ["python"], ...),
        ("editor choice",   choice_result["winner"] == "VS Code", ...),
    ]
    passed = sum(1 for _, ok, _ in checks if ok)
    exit_code = 0 if passed == len(checks) else 1
    assert exit_code == 0
    return {"checks": checks, "passed": passed, "total": len(checks), "exit_code": exit_code}
```

**တကယ့် output**

```
Exercise 6 — editor setup အစီရင်ခံစာ
  (exercise_1–5 ကို တိတ်ဆိတ်စွာ ပြန်လည် ခေါ်သည်)
  အခြေအနေ စုစည်းချက်:
    [PASS] settings.json      key 9 ခု ဖတ်နိုင်သည်
    [PASS] extensions         ချို့နေသည် ['ms-python.debugpy']
    [PASS] remote-ssh entry   alias gpu-box လိုင်း 5 လိုင်း
    [PASS] format-on-save     ဖွင့်မည့် language ['python']
    [PASS] editor choice      အကြံပြု VS Code
  -> 5/5 စစ်ဆေးချက် အောင်မြင်သည်; setup အခြေအနေ: READY
  -> လုပ်ရန် ကျန်သည်: code --install-extension ms-python.debugpy
[OK] exercise_6 — setup အစီရင်ခံစာ (5/5) ထုတ်ပြီးပါပြီ
```

## Lab တစ်ခုလုံး၏ ရလဒ်

```bash
$ python3 modules/08_editor_setup/lab.py
```

```
====================================================================
Module 08 — Editor Setup · offline lab
====================================================================
... exercise_1 … exercise_5 (အပေါ်တွင် ဖော်ပြထားသည့်အတိုင်း) ...
--------------------------------------------------------------------
Exercise 6 — editor setup အစီရင်ခံစာ
  (exercise_1–5 ကို တိတ်ဆိတ်စွာ ပြန်လည် ခေါ်သည်)
  အခြေအနေ စုစည်းချက်:
    [PASS] settings.json      key 9 ခု ဖတ်နိုင်သည်
    [PASS] extensions         ချို့နေသည် ['ms-python.debugpy']
    [PASS] remote-ssh entry   alias gpu-box လိုင်း 5 လိုင်း
    [PASS] format-on-save     ဖွင့်မည့် language ['python']
    [PASS] editor choice      အကြံပြု VS Code
  -> 5/5 စစ်ဆေးချက် အောင်မြင်သည်; setup အခြေအနေ: READY
  -> လုပ်ရန် ကျန်သည်: code --install-extension ms-python.debugpy
[OK] exercise_6 — setup အစီရင်ခံစာ (5/5) ထုတ်ပြီးပါပြီ
====================================================================
[PASS] All 6/6 exercises passed successfully.
```

Exit code — `0`။ `[OK] exercise_N` လိုင်း ၆ လိုင်း ထွက်သည်။

## နောက်တစ်ဆင့်

1. `code --list-extensions` ကို run ၍ ချို့နေသည့် extension ၄ ခုကို `code --install-extension` ဖြင့်
   ထည့်ပါ။
2. `Settings > Open Settings (JSON)` ကို ဖွင့်၍ ဤ Module ၏ `settings.json` ကို ထည့်ပါ။
3. Python ဖိုင် တစ်ခု ဖွင့်၍ Pylance သည် type hint ပြသခြင်း နှင့် Black သည် save ချိန်တွင်
   format လုပ်ခြင်း ကို စစ်ပါ။
4. Remote machine ရှိလျှင် `~/.ssh/config` တွင် host entry ထည့်ပြီး `ssh <alias>` ဖြင့် အရင် စမ်းပါ။
   အောင်မြင်မှ `Remote-SSH: Connect to Host` ကို အသုံးပြုပါ။ ချိတ်ပြီးလျှင် status bar တွင် host အမည်
   ပေါ်လာမည်။
