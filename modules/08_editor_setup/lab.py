#!/usr/bin/env python3
"""Module 08 — Editor Setup ၏ offline lab (Python standard library သာ)။

Lab သည် network မလိုပါ၊ `code` CLI ကို မ ခေါ်ပါ၊ third-party package မ သုံးပါ။
`settings.json` ကို temporary directory တွင် ကိုယ်တိုင် ရေး၍ parse လုပ်သည်။
`code --list-extensions` ၏ output ကို စာသား စာရင်း အဖြစ် တုပသည်။ ရလဒ်သည်
deterministic ဖြစ်သည်။

run နည်း:
    python3 modules/08_editor_setup/lab.py
"""

from __future__ import annotations

import json
import os
import tempfile

# ---------------------------------------------------------------------------
# Source lesson (phases/00-setup-and-tooling/08-editor-setup) မှ တိုက်ရိုက် ယူသည့်
# extension ID စာရင်း အစဉ်အတိုင်း။ ID တိုင်းသည် `code --install-extension` နှင့်
# ကိုက်ညီသည်။ ID တစ်ခုမျှ ကိုယ်တိုင် ဖန်တီး ထည့်သွင်းခြင်း မ ပြုရ။
# ---------------------------------------------------------------------------
REQUIRED_EXTENSIONS = [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "eamodio.gitlens",
    "ms-vscode-remote.remote-ssh",
    "ms-python.debugpy",
    "ms-python.black-formatter",
    "charliermarsh.ruff",
]

EXTENSION_PURPOSE = {
    "ms-python.python": "language support, virtual env detection, run/debug",
    "ms-python.vscode-pylance": "type checking, autocomplete, import resolution",
    "ms-toolsai.jupyter": "notebook ကို editor အတွင်း run၊ variable explorer",
    "eamodio.gitlens": "inline git blame၊ မည်သူ ပြောင်းသည် ကို ကြည့်ခြင်း",
    "ms-vscode-remote.remote-ssh": "remote GPU box ကို local ကဲ့သို့ ဖွင့်ခြင်း",
    "ms-python.debugpy": "Python step-through debugging",
    "ms-python.black-formatter": "Auto-format on save",
    "charliermarsh.ruff": "အမြန် linting",
}

# ---------------------------------------------------------------------------
# ဤ module သင်ပေးသည့် `settings.json` (source အတိုင်း)။
# ---------------------------------------------------------------------------
SETTINGS_DOC = {
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": True,
    "editor.rulers": [88, 120],
    "notebook.output.scrolling": True,
    "files.autoSave": "afterDelay",
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.scrollback": 10000,
}

# `parse_settings` က မဖြစ်မနေ စစ်သည့် key နှင့် မျှော်မှန်းတန်ဖိုး။
REQUIRED_SETTING_KEYS = {
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": True,
    "editor.rulers": [88, 120],
    "notebook.output.scrolling": True,
    "files.autoSave": "afterDelay",
}

# တုပသည့် `code --list-extensions` output။
# `ms-python.debugpy` ကို တမင် ချန်ထားသည် (ချို့နေသည့် extension ကို ပြရန်)။
SIMULATED_INSTALLED = [
    "charliermarsh.ruff",
    "eamodio.gitlens",
    "ms-python.black-formatter",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-toolsai.jupyter",
    "ms-toolsai.jupyter-keymap",
    "ms-vscode-remote.remote-ssh",
]

# format-on-save မူဝါဒ (language အလိုက်)။
FORMAT_POLICY = {
    "python": {
        "enabled": True,
        "formatter": "ms-python.black-formatter",
        "reason": "source: Black သည် format-on-save ကို ကိုင်တွယ်သည်; style တူညီသည်",
    },
    "jsonc": {
        "enabled": False,
        "formatter": None,
        "reason": "VS Code settings ဖိုင်တွင် comment ပါသည်; ကိုယ်တိုင် ချိန်ညှိသင့်သည်",
    },
    "markdown": {
        "enabled": False,
        "formatter": None,
        "reason": "စာသား ဖိုင်ကို ကိုယ်တိုင် စီစဉ်သည်; မလိုအပ်သည့် reflow ကို ရှောင်ခြင်း",
    },
    "dockerfile": {
        "enabled": False,
        "formatter": None,
        "reason": "layer စီစဉ်မှုကို လူက ဆုံးဖြတ်သည်; ဖော်မတ် ပြောင်းလျှင် layer ပြောင်းနိုင်သည်",
    },
}

# Remote SSH host entry တည်ဆောက်ရန် spec (source ၏ `~/.ssh/config` နမူနာအတိုင်း)။
SSH_HOST_SPEC = {
    "alias": "gpu-box",
    "hostname": "203.0.113.50",
    "user": "ubuntu",
    "identity_file": "~/.ssh/id_ed25519",
    "forward_agent": "yes",
}

# Editor alternatives ကို လိုအပ်ချက် အလိုက် ဆန်းစစ်ရန် အလေးချိန်။
EDITOR_REQUIREMENTS = {
    "remote_ssh_editing": 3,
    "vscode_settings_compat": 2,
    "jupyter_support": 2,
    "free_no_subscription": 2,
    "builtin_ai_completion": 1,
}

EDITOR_FEATURES = {
    "VS Code": {
        "remote_ssh_editing": True,
        "vscode_settings_compat": True,
        "jupyter_support": True,
        "free_no_subscription": True,
        "builtin_ai_completion": False,
        "note": "source ၏ အကြံပြု editor; extension နှင့် settings format ရင်းမြစ်",
    },
    "Cursor": {
        "remote_ssh_editing": True,
        "vscode_settings_compat": True,
        "jupyter_support": True,
        "free_no_subscription": False,
        "builtin_ai_completion": True,
        "note": "VS Code fork; extension နှင့် settings format တူညီသည်",
    },
    "Windsurf": {
        "remote_ssh_editing": True,
        "vscode_settings_compat": True,
        "jupyter_support": True,
        "free_no_subscription": False,
        "builtin_ai_completion": True,
        "note": "AI-first VS Code fork; extension, settings, Remote SSH တူညီသည်",
    },
    "Neovim": {
        "remote_ssh_editing": True,
        "vscode_settings_compat": False,
        "jupyter_support": True,
        "free_no_subscription": True,
        "builtin_ai_completion": False,
        "note": "pyright/pylsp + nvim-lspconfig + molten-nvim ကို ကိုယ်တိုင် ချိတ်ရသည်",
    },
}

OK = "[OK]"

# exercise_6 သည် exercise_1–5 ကို တိတ်ဆိတ်စွာ ပြန်လည် အသုံးပြုသည်။
_QUIET = False


def _p(*args) -> None:
    """`_QUIET` ဖြစ်နေလျှင် ရိုက်မထုတ်ပါ။"""
    if not _QUIET:
        print(*args)


def _line(char: str = "-", width: int = 68) -> str:
    return char * width


def _write_settings_file(directory: str, doc: dict) -> str:
    """`settings.json` ကို temporary directory အတွင်း ရေး၍ path ကို ပြန်ပေးသည်။"""
    path = os.path.join(directory, "settings.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(doc, handle, indent=4, ensure_ascii=False)
        handle.write("\n")
    return path


# ---------------------------------------------------------------------------
# Exercise 1 — parse_settings
# ---------------------------------------------------------------------------
def exercise_1(workdir: str) -> dict:
    """`settings.json` ကို ဖတ်၍ မဖြစ်မနေ key များ ပြည့်စုံ/မပြည့်စုံ ကို စစ်သည်။"""
    path = _write_settings_file(workdir, SETTINGS_DOC)
    with open(path, "r", encoding="utf-8") as handle:
        loaded = json.load(handle)

    _p("Exercise 1 — settings.json key စစ်ဆေးခြင်း")
    _p(f"  ဖိုင်: <tempdir>/{os.path.basename(path)}")
    _p(f"  key စုစုပေါင်း: {len(loaded)}")

    missing = []
    mismatched = []
    for key, expected in sorted(REQUIRED_SETTING_KEYS.items()):
        if key not in loaded:
            missing.append(key)
            _p(f"  [MISSING] {key}")
        elif loaded[key] != expected:
            mismatched.append(key)
            _p(f"  [MISMATCH] {key}: {loaded[key]!r} != {expected!r}")
        else:
            _p(f"  [OK] {key} = {json.dumps(expected, ensure_ascii=False)}")

    assert not missing, f"key ချို့နေသည်: {missing}"
    assert not mismatched, f"တန်ဖိုး မတူသည်: {mismatched}"
    assert loaded["editor.rulers"] == [88, 120]

    _p("  -> မဖြစ်မနေ key ၅ ခု အားလုံး မှန်ကန်သည်")
    _p(f"{OK} exercise_1 — settings.json key ၅ ခုကို စစ်ဆေးပြီးပါပြီ")
    return {"path": path, "total_keys": len(loaded), "missing": missing}


# ---------------------------------------------------------------------------
# Exercise 2 — extension_diff
# ---------------------------------------------------------------------------
def exercise_2() -> dict:
    """လိုအပ်သော extension နှင့် `code --list-extensions` output ကို နှိုင်းယှဉ်သည်။"""
    installed = sorted(SIMULATED_INSTALLED)
    required = sorted(REQUIRED_EXTENSIONS)

    _p("Exercise 2 — extension တိုက်ဆိုင်စစ်ခြင်း")
    _p(f"  installed (တုပထားသည်): {len(installed)} ခု")
    for ext in installed:
        mark = "required" if ext in required else "extra"
        _p(f"    {ext} [{mark}]")

    missing = [ext for ext in required if ext not in installed]
    extra = [ext for ext in installed if ext not in required]

    _p(f"  ချို့နေသည့် extension: {missing if missing else 'မရှိ'}")
    _p(f"  ပိုနေသည့် extension: {extra if extra else 'မရှိ'}")
    for ext in missing:
        _p(f"    install ရန်: code --install-extension {ext}")

    assert "ms-python.debugpy" in missing, "debugpy ချို့နေသည်ဟု မျှော်မှန်းသည်"
    assert set(required) - set(missing) <= set(installed)
    assert len(required) == 8

    _p(f"  -> လိုအပ် ၈ ခုအနက် {len(required) - len(missing)} ခု တပ်ဆင်ပြီးဖြစ်သည်")
    _p(f"{OK} exercise_2 — extension စာရင်း ၈ ခုကို နှိုင်းယှဉ်ပြီးပါပြီ")
    return {"missing": missing, "extra": extra, "installed_count": len(installed)}


# ---------------------------------------------------------------------------
# Exercise 3 — ssh_config_entry
# ---------------------------------------------------------------------------
def exercise_3() -> dict:
    """Remote SSH အတွက် `~/.ssh/config` host entry ကို spec မှ တည်ဆောက်သည်။"""
    spec = SSH_HOST_SPEC
    lines = [
        f"Host {spec['alias']}",
        f"    HostName {spec['hostname']}",
        f"    User {spec['user']}",
        f"    IdentityFile {spec['identity_file']}",
        f"    ForwardAgent {spec['forward_agent']}",
    ]
    block = "\n".join(lines) + "\n"

    _p("Exercise 3 — Remote SSH host entry တည်ဆောက်ခြင်း")
    _p("  ~/.ssh/config ထဲ ထည့်ရမည့် အပိုင်း:")
    for line in lines:
        _p(f"    {line}")

    required_tokens = ["Host gpu-box", "HostName 203.0.113.50", "User ubuntu",
                       "IdentityFile ~/.ssh/id_ed25519", "ForwardAgent yes"]
    for token in required_tokens:
        assert token in block, f"host entry တွင် မပါသည်: {token}"
    assert block.count("\n") == 5
    assert block.splitlines()[0] == "Host gpu-box"

    _p(f"  -> alias '{spec['alias']}' ဖြင့် 'Remote-SSH: Connect to Host' မှ ချိတ်နိုင်သည်")
    _p(f"{OK} exercise_3 — SSH host entry လိုင်း ၅ လိုင်း တည်ဆောက်ပြီးပါပြီ")
    return {"alias": spec["alias"], "block": block, "lines": len(lines)}


# ---------------------------------------------------------------------------
# Exercise 4 — format_on_save_policy
# ---------------------------------------------------------------------------
def exercise_4(languages=None) -> dict:
    """language အလိုက် format-on-save မူဝါဒကို ဆုံးဖြတ်သည်။"""
    if languages is None:
        languages = ["python", "jsonc", "markdown", "dockerfile", "unknown_lang"]

    _p("Exercise 4 — format-on-save မူဝါဒ")
    decisions = {}
    for lang in languages:
        policy = FORMAT_POLICY.get(lang)
        if policy is None:
            decisions[lang] = {
                "enabled": False,
                "formatter": None,
                "reason": "formatter မ သတ်မှတ်ရသေးပါ; 'version အလိုက် ပြန်စစ်ရန် လိုသည်'",
            }
        else:
            decisions[lang] = dict(policy)
        entry = decisions[lang]
        state = "ON" if entry["enabled"] else "OFF"
        formatter = entry["formatter"] if entry["formatter"] else "-"
        _p(f"  {lang:<13} format-on-save={state:<3} formatter={formatter}")
        _p(f"                 {entry['reason']}")

    assert decisions["python"]["enabled"] is True
    assert decisions["python"]["formatter"] == "ms-python.black-formatter"
    assert decisions["jsonc"]["enabled"] is False
    assert decisions["unknown_lang"]["enabled"] is False

    enabled = sorted(lang for lang, entry in decisions.items() if entry["enabled"])
    _p(f"  -> format-on-save ဖွင့်မည့် language: {enabled}")
    _p(f"{OK} exercise_4 — format-on-save မူဝါဒ {len(languages)} မျိုးအတွက် ဆုံးဖြတ်ပြီးပါပြီ")
    return {"decisions": decisions, "enabled": enabled}


# ---------------------------------------------------------------------------
# Exercise 5 — editor_choice_matrix
# ---------------------------------------------------------------------------
def exercise_5() -> dict:
    """VS Code / Cursor / Windsurf / Neovim ကို လိုအပ်ချက် အလိုက် အဆင့်သတ်သည်။"""
    _p("Exercise 5 — editor ရွေးချယ်မှု ဇယား")
    _p("  လိုအပ်ချက် အလေးချိန်:")
    for name, weight in sorted(EDITOR_REQUIREMENTS.items()):
        _p(f"    {name:<26} {weight}")

    scores = {}
    for editor, features in EDITOR_FEATURES.items():
        total = 0
        for requirement, weight in EDITOR_REQUIREMENTS.items():
            if features.get(requirement) is True:
                total += weight
        scores[editor] = total

    max_score = sum(EDITOR_REQUIREMENTS.values())
    _p(f"  အမှတ် အမြင့်ဆုံး ဖြစ်နိုင်သည်: {max_score}")
    ranking = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    for rank, (editor, score) in enumerate(ranking, start=1):
        _p(f"    {rank}. {editor:<9} {score}/{max_score}  — {EDITOR_FEATURES[editor]['note']}")

    winner, winner_score = ranking[0]
    met = [req for req in sorted(EDITOR_REQUIREMENTS)
           if EDITOR_FEATURES[winner].get(req) is True]
    _p(f"  -> ဤ လိုအပ်ချက် အစုအတွက် အသင့်တော်ဆုံး: {winner} ({winner_score}/{max_score})")
    _p(f"     ဖြည့်ဆည်းသည်: {met}")

    assert winner == "VS Code", f"မျှော်မှန်းသည့် ရလဒ် မတူသည်: {winner}"
    assert scores["Cursor"] == scores["Windsurf"]
    assert scores["Neovim"] < scores["VS Code"]

    _p(f"{OK} exercise_5 — editor ၄ ခုကို လိုအပ်ချက် ၅ မျိုးနှင့် အဆင့်သတ်ပြီးပါပြီ")
    return {"scores": scores, "ranking": ranking, "winner": winner}


# ---------------------------------------------------------------------------
# Exercise 6 — editor_report
# ---------------------------------------------------------------------------
def exercise_6(workdir: str) -> dict:
    """စစ်ဆေးချက် အားလုံးကို စုစည်း၍ setup အစီရင်ခံစာ ထုတ်သည်။"""
    global _QUIET

    _p("Exercise 6 — editor setup အစီရင်ခံစာ")
    _p("  (exercise_1–5 ကို တိတ်ဆိတ်စွာ ပြန်လည် ခေါ်သည်)")

    _QUIET = True
    try:
        settings_result = exercise_1(workdir)
        extension_result = exercise_2()
        ssh_result = exercise_3()
        policy_result = exercise_4()
        choice_result = exercise_5()
    finally:
        _QUIET = False

    checks = [
        ("settings.json", len(settings_result["missing"]) == 0,
         f"key {settings_result['total_keys']} ခု ဖတ်နိုင်သည်"),
        ("extensions", len(extension_result["missing"]) == 1,
         f"ချို့နေသည် {extension_result['missing']}"),
        ("remote-ssh entry", "Host gpu-box" in ssh_result["block"],
         f"alias {ssh_result['alias']} လိုင်း {ssh_result['lines']} လိုင်း"),
        ("format-on-save", policy_result["enabled"] == ["python"],
         f"ဖွင့်မည့် language {policy_result['enabled']}"),
        ("editor choice", choice_result["winner"] == "VS Code",
         f"အကြံပြု {choice_result['winner']}"),
    ]

    _p("  အခြေအနေ စုစည်းချက်:")
    passed = 0
    for name, ok, detail in checks:
        state = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        _p(f"    [{state}] {name:<18} {detail}")

    total = len(checks)
    ready = passed == total
    exit_code = 0 if ready else 1
    _p(f"  -> {passed}/{total} စစ်ဆေးချက် အောင်မြင်သည်; setup အခြေအနေ: "
       f"{'READY' if ready else 'INCOMPLETE'}")
    _p("  -> လုပ်ရန် ကျန်သည်: code --install-extension ms-python.debugpy")

    assert ready, f"စစ်ဆေးချက် {total} ခုအနက် {passed} ခုသာ အောင်မြင်သည်"
    assert exit_code == 0

    _p(f"{OK} exercise_6 — setup အစီရင်ခံစာ ({passed}/{total}) ထုတ်ပြီးပါပြီ")
    return {"checks": checks, "passed": passed, "total": total, "exit_code": exit_code}


def main() -> int:
    print(_line("="))
    print("Module 08 — Editor Setup · offline lab")
    print(_line("="))

    try:
        with tempfile.TemporaryDirectory(prefix="editor_setup_lab_") as workdir:
            exercise_1(workdir)
            print(_line())
            exercise_2()
            print(_line())
            exercise_3()
            print(_line())
            exercise_4()
            print(_line())
            exercise_5()
            print(_line())
            exercise_6(workdir)
    except AssertionError as error:  # pragma: no cover - ကျရှုံးသည့် အခြေအနေ
        print(f"[FAIL] {error}")
        return 1

    print(_line("="))
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
