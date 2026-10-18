#!/usr/bin/env python3
"""Module 02 — Git & Collaboration lab (offline, deterministic).

Git လုပ်ငန်းစဉ်များကို memory ထဲတွင် သရုပ်ဖော်သည်။ git binary ကို ခေါ်ခြင်း မရှိပါ;
network၊ GPU၊ third-party package မလိုပါ။ Python standard library သာ သုံးသည်။

Run:
    python3 modules/02_git_and_collaboration/lab.py
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from os.path import basename

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------


def _heading(number: int, name: str) -> None:
    print()
    print("=" * 70)
    print(f"Exercise {number} — {name}")
    print("=" * 70)


def _ok(number: int, description: str) -> None:
    print(f"[OK] exercise_{number} — {description}")


# ----------------------------------------------------------------------------
# Exercise 1 — parse_git_config
# ----------------------------------------------------------------------------

IDENTITY_KEYS = ("user.name", "user.email")

CONFIG_TEXT = """\
user.name=Ko Aung
user.email=aung@example.com
core.editor=vim
init.defaultBranch=main
pull.rebase=false
"""

INCOMPLETE_CONFIG_TEXT = """\
user.name=
core.editor=nano
init.defaultBranch=main
"""


def parse_git_config(text: str) -> dict[str, str]:
    """`git config --list` ၏ output ကို key → value dict အဖြစ် ပြောင်းသည်။

    မှတ်ချက် — `#` သို့မဟုတ် `;` ဖြင့် စသည့် လိုင်းနှင့် `=` မပါသည့် လိုင်းကို ချန်လှပ်သည်။
    """
    config: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        config[key.strip()] = value.strip()
    return config


def check_identity(config: dict[str, str]) -> dict[str, object]:
    """identity (user.name, user.email) ပြည့်စုံခြင်းကို စစ်သည်။"""
    name = config.get("user.name", "")
    email = config.get("user.email", "")
    problems: list[str] = []
    if not name:
        problems.append("user.name မရှိပါ")
    if not email:
        problems.append("user.email မရှိပါ")
    elif "@" not in email or "." not in email.split("@")[-1]:
        problems.append("user.email ပုံစံ မမှန်ပါ")
    return {
        "name": name,
        "email": email,
        "complete": not problems,
        "problems": problems,
    }


def exercise_1() -> None:
    _heading(1, "parse_git_config — git identity ကို ဖတ်ခြင်း")

    for label, text in (("ပြည့်စုံသည့် config", CONFIG_TEXT),
                        ("မပြည့်စုံသည့် config", INCOMPLETE_CONFIG_TEXT)):
        print(f"-- {label} --")
        config = parse_git_config(text)
        print(f"parse လုပ်ပြီး key အရေအတွက် : {len(config)}")
        for key in sorted(config):
            value = config[key] if config[key] else "(အလွတ်)"
            print(f"  {key:22} = {value}")
        identity = check_identity(config)
        for key in IDENTITY_KEYS:
            print(f"  စစ်ဆေးချက် {key:14} : {'ရှိသည်' if config.get(key) else 'မရှိပါ'}")
        print(f"  identity ပြည့်စုံမှု      : {identity['complete']}")
        if identity["problems"]:
            for problem in identity["problems"]:
                print(f"  ပြဿနာ — {problem}")
        print()

    complete = check_identity(parse_git_config(CONFIG_TEXT))
    assert complete["complete"] is True
    assert complete["name"] == "Ko Aung"
    assert complete["email"] == "aung@example.com"
    broken = check_identity(parse_git_config(INCOMPLETE_CONFIG_TEXT))
    assert broken["complete"] is False
    assert len(broken["problems"]) == 2
    assert parse_git_config(CONFIG_TEXT)["core.editor"] == "vim"

    _ok(1, "git config မှ identity ဖတ်ပြီး ပြည့်စုံမှု စစ်ခြင်း")


# ----------------------------------------------------------------------------
# Exercise 2 — build_gitignore
# ----------------------------------------------------------------------------

CHECKPOINT_PATTERNS = ("*.pt", "*.pth", "*.safetensors")
OTHER_PATTERNS = (".env", ".venv/", "__pycache__/", "data/", "wandb/")

GITIGNORE_TEXT = """\
# Model checkpoints — ဤဖိုင်များသည် ကြီးမားသည်၊ ပြန် generate လုပ်နိုင်သည်
*.pt
*.pth
*.safetensors

# Secrets နှင့် ပတ်ဝန်းကျင်
.env
.venv/

# Generated / cache
__pycache__/
data/
wandb/
"""

PROBE_PATHS = (
    "models/perceptron.pt",
    "checkpoints/llama-3-8b.safetensors",
    "models/old-weights.pth",
    "src/train.py",
    "README.md",
    "requirements.txt",
    ".env",
    ".venv/lib/python3.11/site-packages/torch/__init__.py",
    "__pycache__/train.cpython-311.pyc",
    "data/train.csv",
    "wandb/run-20260101/output.log",
)


def compile_ignore(patterns) -> list[tuple[str, bool]]:
    """`.gitignore` pattern စာရင်းကို (pattern, is_directory) rule အဖြစ် ပြောင်းသည်။"""
    rules: list[tuple[str, bool]] = []
    for raw in patterns:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        is_directory = line.endswith("/")
        rules.append((line.rstrip("/"), is_directory))
    return rules


def is_ignored(path: str, rules) -> str | None:
    """path ကို ignore လုပ်သည့် pattern ကို ပြန်သည်; မဟုတ်ပါက None ပြန်သည်။"""
    clean = path.strip("/")
    segments = clean.split("/")
    for pattern, is_directory in rules:
        if is_directory:
            if pattern in segments[:-1] or pattern in segments:
                return pattern + "/"
        else:
            if fnmatch.fnmatch(clean, pattern) or fnmatch.fnmatch(basename(clean), pattern):
                return pattern
    return None


def build_gitignore() -> str:
    """checkpoint နှင့် ဖိုင်ကြီးများကို ဖုံးလွှမ်းသည့် `.gitignore` စာသား ပြန်သည်။"""
    return GITIGNORE_TEXT


def exercise_2() -> None:
    _heading(2, "build_gitignore — checkpoint များကို ဖုံးလွှမ်းခြင်း")

    text = build_gitignore()
    print("-- .gitignore အကြောင်းအရာ --")
    for line in text.splitlines():
        print(f"  {line}")

    rules = compile_ignore(text.splitlines())
    print()
    print(f"pattern rule အရေအတွက် : {len(rules)}")
    print()
    print("-- စမ်းသပ်သည့် path များ --")
    ignored, tracked = [], []
    for path in PROBE_PATHS:
        hit = is_ignored(path, rules)
        if hit is None:
            tracked.append(path)
            print(f"  [track] {path}")
        else:
            ignored.append((path, hit))
            print(f"  [ignore:{hit} ] {path}")

    print()
    print(f"ignore ဖြစ်သည့် path : {len(ignored)}")
    print(f"track ဖြစ်သည့် path : {len(tracked)}")

    checkpoints = [p for p in CHECKPOINT_PATTERNS]
    print()
    print("-- checkpoint extension တိုင်း ဖုံးလွှမ်းမှု --")
    for pattern in checkpoints:
        probe = "models/example" + pattern[1:]
        hit = is_ignored(probe, rules)
        print(f"  {pattern:16} → {probe:28} : {'ignore' if hit else 'TRACK (မှားသည်)'}")
        assert hit is not None

    assert is_ignored("models/perceptron.pt", rules) == "*.pt"
    assert is_ignored("checkpoints/llama-3-8b.safetensors", rules) == "*.safetensors"
    assert is_ignored("__pycache__/train.cpython-311.pyc", rules) == "__pycache__/"
    assert is_ignored("data/train.csv", rules) == "data/"
    assert is_ignored("src/train.py", rules) is None
    assert is_ignored("README.md", rules) is None

    _ok(2, ".gitignore တည်ဆောက်ပြီး checkpoint ဖုံးလွှမ်းမှု စစ်ခြင်း")


# ----------------------------------------------------------------------------
# Exercise 3 — commit_workflow
# ----------------------------------------------------------------------------


@dataclass
class CommitState:
    """add → commit → push လုပ်ငန်းစဉ်၏ အခြေအနေ။"""

    branch: str = "main"
    untracked: list[str] = field(default_factory=list)
    staged: list[str] = field(default_factory=list)
    local: list[str] = field(default_factory=list)
    remote: list[str] = field(default_factory=list)

    @property
    def ahead(self) -> int:
        return len(self.local) - len(self.remote)

    def show(self, step: str) -> None:
        print(
            f"  [{step:22}] staged={self.staged} "
            f"local={len(self.local)} remote={len(self.remote)} ahead={self.ahead}"
        )

    def touch(self, *paths: str) -> None:
        self.untracked.extend(paths)
        self.show("touch")

    def add(self, *paths: str) -> None:
        for path in paths:
            if path in self.untracked:
                self.untracked.remove(path)
        self.staged.extend(paths)
        self.show("git add")

    def commit(self, message: str) -> str:
        if not self.staged:
            self.show("git commit (skip)")
            print("            → staged မရှိသဖြင့် commit မဖြစ်ပါ")
            return "nothing_to_commit"
        entry = f"{message} [{','.join(sorted(self.staged))}]"
        self.local.append(entry)
        self.staged = []
        self.show("git commit")
        return entry

    def push(self, remote: str = "origin") -> str:
        if self.ahead <= 0:
            self.show("git push (no-op)")
            print(f"            → push လုပ်ရန် commit မရှိပါ ({remote}/{self.branch} up to date)")
            return "up_to_date"
        sent = self.ahead
        self.remote = list(self.local)
        self.show("git push")
        print(f"            → commit {sent} ခု {remote}/{self.branch} သို့ ရောက်သည်")
        return "pushed"


def exercise_3() -> None:
    _heading(3, "commit_workflow — add → commit → push state machine")

    repo = CommitState()
    print(f"branch : {repo.branch}")
    print()

    repo.touch("src/perceptron.py")
    repo.add("src/perceptron.py")
    message = repo.commit("Add perceptron implementation")
    print(f"            → commit hash (ပုံစံစားသာ) : {'a3f9c21' + ' ' + message[:24]}")
    repo.push("origin")

    print()
    print("-- ဒုတိယ အလှည့် — commit နှစ်ခု တစ်ကြိမ်တည်း push --")
    repo.touch("notebooks/02_git.ipynb", "notes/git.md")
    repo.add("notebooks/02_git.ipynb", "notes/git.md")
    repo.commit("Add git lesson notes")
    repo.touch("src/trainer.py")
    repo.add("src/trainer.py")
    repo.commit("Add trainer skeleton")
    print(f"  push မလုပ်မီ ahead : {repo.ahead}")
    repo.push("origin")

    print()
    print("-- push မလိုသည့် အခြေအနေ --")
    repo.push()

    print()
    print("-- staged မရှိဘဲ commit လုပ်ရန် ကြိုးစားခြင်း --")
    repo.commit("Empty commit attempt")

    assert repo.remote == repo.local
    assert repo.ahead == 0
    assert len(repo.local) == 3
    assert repo.commit("x") == "nothing_to_commit"

    _ok(3, "add → commit → push လုပ်ငန်းစဉ် အခြေအနေ ပြခြင်း")


# ----------------------------------------------------------------------------
# Exercise 4 — branch_experiment
# ----------------------------------------------------------------------------


def merge_files(base: dict[str, str], ours: dict[str, str],
                theirs: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """base/ours/theirs သုံးမျိုးမှ merge လုပ်ပြီး (ရလဒ်, conflict key စာရင်း) ပြန်သည်။"""
    result: dict[str, str] = dict(base)
    conflicts: list[str] = []
    for key in sorted(set(base) | set(ours) | set(theirs)):
        b, o, t = base.get(key), ours.get(key), theirs.get(key)
        if o == t:
            if o is not None:
                result[key] = o
        elif o == b:
            if t is not None:
                result[key] = t
            else:
                result.pop(key, None)
        elif t == b:
            if o is not None:
                result[key] = o
            else:
                result.pop(key, None)
        else:
            conflicts.append(key)
    return result, conflicts


def branch_experiment(base: dict[str, str], branch_changes: dict[str, str],
                      main_changes: dict[str, str]) -> dict[str, object]:
    """branch တစ်ခု ဖန်တီး၊ commit နှစ်လိုင်း ပြီး merge ၏ အခြေအနေကို ဆုံးဖြတ်သည်။"""
    theirs = dict(base)
    theirs.update(branch_changes)
    ours = dict(base)
    ours.update(main_changes)
    result, conflicts = merge_files(base, ours, theirs)
    fast_forward = ours == base
    return {
        "base": base,
        "branch": theirs,
        "main": ours,
        "merged": result,
        "conflicts": conflicts,
        "fast_forward": fast_forward,
        "status": "conflict" if conflicts else "clean",
    }


def exercise_4() -> None:
    _heading(4, "branch_experiment — branch ဖန်တီး၊ merge နှင့် conflict")

    base = {"optimizer": "sgd", "lr": "0.01", "epochs": "3"}

    print("-- အခြေအနေ ၁ — မတူညီသည့် key ကို ပြင်ခြင်း (conflict မဖြစ်) --")
    case_a = branch_experiment(
        base,
        branch_changes={"optimizer": "adam"},
        main_changes={"lr": "0.001"},
    )
    for label in ("base", "branch", "main", "merged"):
        print(f"  {label:7} : {case_a[label]}")
    print(f"  status  : {case_a['status']}")
    print(f"  conflict: {case_a['conflicts']}")
    print()

    print("-- အခြေအနေ ၂ — key တူညီသည့် လိုင်းကို နှစ်ဖက် ပြင်ခြင်း (conflict) --")
    case_b = branch_experiment(
        base,
        branch_changes={"optimizer": "adam"},
        main_changes={"optimizer": "rmsprop"},
    )
    for label in ("base", "branch", "main", "merged"):
        print(f"  {label:7} : {case_b[label]}")
    print(f"  status  : {case_b['status']}")
    print(f"  conflict: {case_b['conflicts']}")
    print(f"  လုပ်ဆောင်ရန် : conflict ဖြစ်သည့် key ကို လူက ရွေး၍ {case_b['conflicts']} ကို ပြင်၊")
    print("               ပြီးနောက် `git add` + `git commit` ဖြင့် merge ကို အပြီးသတ်သည်")
    print()

    print("-- အခြေအနေ ၃ — main မပြောင်းလျှင် fast-forward --")
    case_c = branch_experiment(base, branch_changes={"optimizer": "adam"}, main_changes={})
    print(f"  branch commit ရှိသည် : {case_c['branch'] != base}")
    print(f"  fast-forward         : {case_c['fast_forward']}")
    print(f"  merged               : {case_c['merged']}")
    print(f"  status               : {case_c['status']}")

    assert case_a["status"] == "clean"
    assert case_a["merged"] == {"optimizer": "adam", "lr": "0.001", "epochs": "3"}
    assert case_b["status"] == "conflict"
    assert case_b["conflicts"] == ["optimizer"]
    assert case_c["fast_forward"] is True

    _ok(4, "branch ဖန်တီး၊ merge နှင့် conflict ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း")


# ----------------------------------------------------------------------------
# Exercise 5 — read_log
# ----------------------------------------------------------------------------

LOG_TEXT = """\
9f2c1ab Add lesson 13 python for AI engineering
4d8e730 Add lesson 12 debugging and profiling
b71a055 Add lesson 11 linux for AI
c30f914 Fix typo in lesson 06 lockfile section
7a62dec Add lesson 06 python environments
1f0b8c2 Initial commit
"""


def parse_log(text: str) -> list[dict[str, str]]:
    """`git log --oneline` စာသားကို [{'hash':…, 'subject':…}] အဖြစ် ပြောင်းသည်။"""
    entries: list[dict[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        commit_hash = parts[0]
        subject = parts[1] if len(parts) > 1 else ""
        entries.append({"hash": commit_hash, "subject": subject})
    return entries


def summarize_log(entries, keyword: str = "") -> dict[str, object]:
    """log entry စာရင်းကို အနှစ်ချုပ်သည်။ keyword ပါလျှင် ထို commit များကို စစ်ထုတ်သည်။"""
    matched = [e for e in entries if keyword.lower() in e["subject"].lower()]
    return {
        "total": len(entries),
        "matched": matched,
        "newest": entries[0] if entries else None,
        "oldest": entries[-1] if entries else None,
        "hashes": [e["hash"] for e in entries],
    }


def exercise_5() -> None:
    _heading(5, "read_log — git log --oneline ကို parse လုပ်ခြင်း")

    entries = parse_log(LOG_TEXT)
    print("-- git log --oneline --")
    for entry in entries:
        print(f"  {entry['hash']} {entry['subject']}")

    summary = summarize_log(entries)
    print()
    print(f"commit စုစုပေါင်း : {summary['total']}")
    print(f"အသစ်ဆုံး        : {summary['newest']['hash']} {summary['newest']['subject']}")
    print(f"အဟောင်းဆုံး     : {summary['oldest']['hash']} {summary['oldest']['subject']}")

    print()
    print("-- commit တစ်ခုကို ကြည့်ခြင်း (git show --stat) --")
    pick = entries[0]
    print(f"  ရွေးသည့် commit : {pick['hash']}")
    print(f"  `git show --stat {pick['hash']}` ၏ ရလဒ် (ပုံစံစားသာ) :")
    print(f"     {pick['hash']} {pick['subject']}")
    print("     1 file changed, 118 insertions(+), 0 deletions(-)")

    print()
    print("-- path အလိုက် စစ်ထုတ်ခြင်း (git log --oneline -- <path>) --")
    phase_entries = [e for e in entries if "lesson" in e["subject"].lower()]
    print(f"  စစ်ထုတ်ပြီး commit အရေအတွက် : {len(phase_entries)}")
    for entry in phase_entries:
        print(f"    {entry['hash']} {entry['subject']}")

    assert summary["total"] == 6
    assert summary["newest"]["hash"] == "9f2c1ab"
    assert summary["oldest"]["subject"] == "Initial commit"
    assert len(phase_entries) == 5
    assert summarize_log(entries, "typo")["matched"][0]["hash"] == "c30f914"

    _ok(5, "git log --oneline ကို parse ပြီး အနှစ်ချုပ် ထုတ်ခြင်း")


# ----------------------------------------------------------------------------
# Exercise 6 — status_report
# ----------------------------------------------------------------------------

STATUS_ENTRIES = (
    ("src/perceptron.py", "modified"),
    ("notebooks/02_git.ipynb", "staged"),
    ("notes/git.md", "staged"),
    ("models/scratch.pt", "untracked"),
    ("README.md", "modified"),
    ("src/trainer.py", "untracked"),
    ("config.yaml", "unmerged"),
)

STATUS_ORDER = ("staged", "modified", "untracked", "unmerged")


def status_report(entries) -> dict[str, object]:
    """working tree entry များကို အုပ်စုခွဲပြီး push ရန် အဆင်သင့် ဖြစ်/မဖြစ် ဆုံးဖြတ်သည်။"""
    groups: dict[str, list[str]] = {state: [] for state in STATUS_ORDER}
    for path, state in entries:
        groups.setdefault(state, []).append(path)
    for state in groups:
        groups[state] = sorted(groups[state])

    unmerged = groups.get("unmerged", [])
    staged = groups.get("staged", [])
    ready = bool(staged) and not unmerged

    if unmerged:
        next_step = "merge conflict ကို ရှေးဦး ဖြေရှင်းရန် လိုသည်"
    elif not staged:
        next_step = "git add <path> ဖြင့် ဖိုင်ကို stage လုပ်ရန် လိုသည်"
    else:
        next_step = 'git commit -m "<message>" ပြီးနောက် git push -u origin <branch>'

    return {
        "groups": groups,
        "counts": {state: len(paths) for state, paths in groups.items()},
        "total": len(entries),
        "ready": ready,
        "next_step": next_step,
    }


def exercise_6() -> None:
    _heading(6, "status_report — working tree အခြေအနေ အစီရင်ခံစာ")

    report = status_report(STATUS_ENTRIES)
    print("-- git status --short မှ entry များ --")
    marker = {"staged": "A/M", "modified": " M ", "untracked": "?? ", "unmerged": "UU "}
    for path, state in STATUS_ENTRIES:
        print(f"  {marker[state]} {path}")

    print()
    print("-- အုပ်စုအလိုက် --")
    for state in STATUS_ORDER:
        paths = report["groups"][state]
        print(f"  {state:10} ({len(paths)}) : {paths}")

    print()
    print(f"entry စုစုပေါင်း         : {report['total']}")
    print(f"push ရန် အဆင်သင့်       : {report['ready']}")
    print(f"လုပ်ဆောင်ရမည့် အဆင့်    : {report['next_step']}")

    print()
    print("-- conflict မရှိသည့် အခြေအနေ --")
    clean = status_report((("src/perceptron.py", "staged"), ("README.md", "modified")))
    print(f"  staged : {clean['groups']['staged']}")
    print(f"  ready  : {clean['ready']}")

    print()
    print("-- staged မရှိသည့် အခြေအနေ --")
    empty = status_report((("README.md", "modified"), ("notes/git.md", "untracked")))
    print(f"  staged : {empty['groups']['staged']}")
    print(f"  ready  : {empty['ready']}")

    assert report["ready"] is False
    assert report["counts"]["staged"] == 2
    assert report["counts"]["unmerged"] == 1
    assert clean["ready"] is True
    assert empty["ready"] is False
    assert empty["next_step"].startswith("git add")

    _ok(6, "untracked / modified / staged ခွဲထုတ်ပြီး push အဆင်သင့်မှု ဆုံးဖြတ်ခြင်း")


# ----------------------------------------------------------------------------
# runner
# ----------------------------------------------------------------------------

EXERCISES = (
    exercise_1,
    exercise_2,
    exercise_3,
    exercise_4,
    exercise_5,
    exercise_6,
)


def main() -> int:
    print("Module 02 — Git & Collaboration lab (offline, standard library သာ)")
    for exercise in EXERCISES:
        exercise()
    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
