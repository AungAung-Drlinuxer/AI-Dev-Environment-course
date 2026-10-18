#!/usr/bin/env python3
"""Module 11 - Linux for AI: offline lab (standard library only).

The six exercises of this module model the Linux command-line work of the
lesson.  Python cannot call `chmod`, `chown`, `sudo`, `apt`, `df` or `du`
here (no shelling out, no network, no sudo), so every command is *simulated*
on the fixed text that this file carries.

Run from the repository root:

    python3 modules/11_linux_for_ai/lab.py

Every exercise prints a readable result and then one line

    [OK] exercise_N — <short description>

The script ends with `[PASS] All 6/6 exercises passed successfully.` and
exits 0.  Every input is a literal, so the output is identical on each run.
"""

from __future__ import annotations

import re

# ==========================================================================
# Exercise 1 - permission modes
# ==========================================================================

BIT_VALUE = {"r": 4, "w": 2, "x": 1, "-": 0}
VALUE_BIT = {4: "r", 2: "w", 1: "x", 0: "-"}
CLASS_START = {"user": 0, "group": 3, "other": 6}

# (path, ls -l mode string, what the mode means)
FILE_MODES = (
    ("train.sh", "-rw-r--r--", "script that is not executable yet"),
    ("deploy.sh", "-rwxr-xr-x", "script that is executable"),
    ("config.yaml", "-rw-r--r--", "config readable by everyone"),
    ("private.key", "-rw-------", "secret readable by the owner only"),
    ("dataset/", "drwxr-xr-x", "shared directory"),
    ("checkpoints/", "drwx------", "directory readable by the owner only"),
)

# (starting mode, symbolic change, what the change does)
SYMBOLIC_CHANGES = (
    ("-rw-r--r--", "a+x", "chmod +x train.sh  -> execute for all classes"),
    ("-rwxrwxrwx", "o-w", "chmod o-w shared.sh  -> drop other's write bit"),
    ("-rw-rw-rw-", "go-w", "chmod go-w team.txt  -> owner writes only"),
    ("-rwxr-xr-x", "u+w", "chmod u+w deploy.sh  -> owner gets write back"),
)


def split_mode(mode):
    """Split an `ls -l` mode string into (file type character, 9 characters)."""
    mode = mode.strip()
    if len(mode) == 9:
        return "-", mode
    if len(mode) == 10:
        return mode[0], mode[1:]
    raise ValueError("bad mode string: {!r}".format(mode))


def body_to_octal(body):
    """Turn `rwxr-xr--` into `754` (one octal digit per permission class)."""
    digits = []
    for start in (0, 3, 6):
        value = 0
        for char in body[start:start + 3]:
            if char not in BIT_VALUE:
                raise ValueError("bad permission character: {!r}".format(char))
            value |= BIT_VALUE[char]
        digits.append(str(value))
    return "".join(digits)


def mode_to_octal(mode):
    """Turn a full `ls -l` mode into `chmod` octal notation."""
    _, body = split_mode(mode)
    return body_to_octal(body)


def octal_to_mode(octal, filetype="-"):
    """Turn `chmod` octal notation back into an `ls -l` mode string."""
    digits = octal.strip()
    if len(digits) == 4 and digits[0] == "0":
        digits = digits[1:]
    if len(digits) != 3 or any(char not in "01234567" for char in digits):
        raise ValueError("bad octal mode: {!r}".format(octal))
    letters = []
    for digit in digits:
        value = int(digit)
        for bit in (4, 2, 1):
            letters.append(VALUE_BIT[bit] if value & bit else "-")
    return filetype + "".join(letters)


def apply_symbolic_change(body, change):
    """Apply a symbolic change such as `u+x`, `go-w` or `a+x` to 9 characters."""
    match = re.fullmatch(r"(?P<who>[ugoa]+)(?P<op>[+\-=])(?P<perms>[rwx]*)", change)
    if not match:
        raise ValueError("bad symbolic change: {!r}".format(change))
    who = match.group("who")
    op = match.group("op")
    perms = match.group("perms")
    targets = [index for letter, index in (("u", 0), ("g", 3), ("o", 6))
               if letter in who or "a" in who]
    characters = list(body)
    for index in targets:
        for offset, letter in enumerate("rwx"):
            if op == "+":
                if letter in perms:
                    characters[index + offset] = letter
            elif op == "-":
                if letter in perms:
                    characters[index + offset] = "-"
            else:
                characters[index + offset] = letter if letter in perms else "-"
    return "".join(characters)


def exercise_1():
    """Convert between symbolic permission modes and octal modes."""
    print("exercise_1 — permission_bits")
    print("  {:<14} {:<12} {:<7} {}".format("path", "mode", "octal", "meaning"))
    rows = []
    for path, mode, meaning in FILE_MODES:
        octal = mode_to_octal(mode)
        rows.append((path, mode, octal))
        print("  {:<14} {:<12} {:<7} {}".format(path, mode, octal, meaning))

    print("  round trip (octal -> symbolic) and the chmod command:")
    for path, mode, octal in rows:
        filetype, _ = split_mode(mode)
        back = octal_to_mode(octal, filetype)
        print("    chmod {0} {1:<14} -> {2}  (round trip: {3})".format(
            octal, path, back, "same" if back == mode else "DIFFERENT"))

    print("  symbolic changes applied by hand:")
    for mode, change, note in SYMBOLIC_CHANGES:
        _, body = split_mode(mode)
        changed = apply_symbolic_change(body, change)
        print("    {0:<12} {1:<6} -> -{2}  0{3}   {4}".format(
            mode, change, changed, body_to_octal(changed), note))

    assert [octal for _, _, octal in rows] == ["644", "755", "644", "600", "755", "700"]
    for path, mode, octal in rows:
        filetype, _ = split_mode(mode)
        assert octal_to_mode(octal, filetype) == mode, "round trip must be exact"
    assert apply_symbolic_change("rw-r--r--", "a+x") == "rwxr-xr-x"
    assert mode_to_octal("-rwxr-xr-x") == "755"
    assert body_to_octal(apply_symbolic_change("rw-rw-rw-", "go-w")) == "644"
    print("[OK] exercise_1 — converted {} modes between symbolic and octal".format(
        len(rows)))
    return rows


# ==========================================================================
# Exercise 2 - diagnose_permission_denied
# ==========================================================================

# Simulation of `ls -la` on a fresh GPU box (`/data` is owned by root).
LISTING = (
    "-rw-r--r-- 1 ubuntu ubuntu   512 Mar 19 10:00 train.sh",
    "-rw-r--r-- 1 root   root     640 Mar 19 10:00 setup_gpu.sh",
    "-rw-r--r-- 1 ubuntu ubuntu  1280 Mar 19 10:00 config.yaml",
    "-rw------- 1 ubuntu ubuntu  1679 Mar 19 10:00 id_rsa",
    "-rw-r----- 1 ubuntu lab      2048 Mar 19 10:00 shared_report.csv",
    "drwxr-xr-x 2 root   root    4096 Mar 19 10:00 checkpoints",
)

# (path, mode, owner, group, action, user, groups, expected verdict, fix)
PERMISSION_CASES = (
    ("./train.sh", "-rw-r--r--", "ubuntu", "ubuntu", "execute",
     "ubuntu", ("ubuntu",), False, "chmod +x train.sh"),
    ("./setup_gpu.sh", "-rw-r--r--", "root", "root", "execute",
     "ubuntu", ("ubuntu",), False, "sudo chmod +x setup_gpu.sh"),
    ("/data/checkpoints", "drwxr-xr-x", "root", "root", "write",
     "ubuntu", ("ubuntu",), False, "sudo chown -R ubuntu:ubuntu /data/checkpoints"),
    ("/data/checkpoints", "drwxr-xr-x", "root", "root", "enter",
     "ubuntu", ("ubuntu",), True, "none needed — the other class has x"),
    ("./id_rsa", "-rw-------", "ubuntu", "ubuntu", "read",
     "ubuntu", ("ubuntu",), True, "none needed — the owner has r"),
    ("./config.yaml", "-rw-r--r--", "ubuntu", "ubuntu", "read",
     "ubuntu", ("ubuntu",), True, "none needed — the owner has r"),
    ("./shared_report.csv", "-rw-r-----", "ubuntu", "lab", "read",
     "guest", ("lab",), True, "none needed — the group class has r"),
)


def permission_class(owner, group, user, groups):
    """Decide which permission class applies: owner, group or other."""
    if user == owner:
        return "user"
    if group in groups:
        return "group"
    return "other"


def class_bits(body, cls):
    """Return the three permission characters of one class."""
    start = CLASS_START[cls]
    return body[start:start + 3]


def action_bit(action):
    """Map an action onto the permission bit it needs."""
    return {"read": "r", "write": "w", "execute": "x", "enter": "x"}[action]


def access_allowed(mode, owner, group, user, groups, action):
    """Return (allowed, permission class, permission characters)."""
    _, body = split_mode(mode)
    cls = permission_class(owner, group, user, groups)
    bits = class_bits(body, cls)
    return action_bit(action) in bits, cls, bits


def exercise_2():
    """Diagnose a "Permission denied" case from simulated `ls -la` output."""
    print("exercise_2 — diagnose_permission_denied")
    print("  ls -la on the box:")
    for line in LISTING:
        print("    {}".format(line))

    denials, fixes = [], []
    print("  checks (user ubuntu, group ubuntu, unless noted):")
    for case in PERMISSION_CASES:
        path, mode, owner, group, action, user, groups, expected, fix = case
        allowed, cls, bits = access_allowed(mode, owner, group, user, groups, action)
        verdict = "allowed" if allowed else "Permission denied"
        print("    {0:<20} {1:<12} {2:<8} as {3:<7} class {4:<6} bits {5}  -> {6}".format(
            path, mode, action, user, cls, bits, verdict))
        if not allowed:
            print("      fix: {}".format(fix))
            denials.append(path + " (" + action + ")")
            if fix not in fixes:
                fixes.append(fix)
        assert allowed == expected, "wrong verdict for {}".format(path)

    print("  denied cases   : {}".format(len(denials)))
    print("  distinct fixes : {}".format(len(fixes)))
    for fix in fixes:
        print("    $ {}".format(fix))
    print("  rule: 'Permission denied' means the class that applies to you has no "
          "r/w/x bit for the action - chmod fixes bits, chown fixes the owner, "
          "sudo only borrows root for one command.")

    assert len(denials) == 3
    assert "chmod +x train.sh" in fixes
    assert any(fix.startswith("sudo chown") for fix in fixes)
    assert len(fixes) == 3
    print("[OK] exercise_2 — diagnosed {} denials and listed {} fixes".format(
        len(denials), len(fixes)))
    return denials, fixes


# ==========================================================================
# Exercise 3 - disk_report
# ==========================================================================

DF_TEXT = """Filesystem      Size  Used Avail Use% Mounted on
/dev/root        98G   64G   33G  65% /
tmpfs           7.8G     0  7.8G   0% /dev/shm
/dev/nvme0n1p2  1.8T  1.7T  132G  93% /data
"""

DU_TEXT = """12G\t/data/checkpoints
1.1G\t/home/ubuntu/.cache
340M\t/home/ubuntu/.cache/pip
156M\t/home/ubuntu/miniconda3
2.4G\t/data/tokenized
0\t/data/empty
"""

SIZE_UNITS = (("T", 2 ** 40), ("G", 2 ** 30), ("M", 2 ** 20), ("K", 2 ** 10))
CROWDED_PERCENT = 85


def parse_size(text):
    """Turn `64G` or `1.7T` or `0` into a number of bytes (1024-based)."""
    text = text.strip()
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([KMGTP]?)", text)
    if not match:
        raise ValueError("bad size: {!r}".format(text))
    number = float(match.group(1))
    unit = match.group(2)
    if unit:
        factor = dict(SIZE_UNITS)[unit]
    else:
        factor = 1
    return int(round(number * factor))


def human_size(num_bytes):
    """Turn a number of bytes into a short `df -h` / `du -sh` style string."""
    for unit, factor in SIZE_UNITS:
        if num_bytes >= factor:
            value = num_bytes / factor
            if value >= 10:
                return "{:.0f}{}".format(value, unit)
            return "{:.1f}{}".format(value, unit)
    return "{}B".format(num_bytes)


def parse_df(text):
    """Parse `df -h` output into a list of file system records."""
    records = []
    lines = text.strip().splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 6:
            continue
        filesystem, size, used, avail, percent, mount = parts[:6]
        records.append({
            "filesystem": filesystem,
            "size": size,
            "used": used,
            "avail": avail,
            "percent": int(percent.rstrip("%")),
            "mount": mount,
            "size_bytes": parse_size(size),
            "used_bytes": parse_size(used),
            "avail_bytes": parse_size(avail),
        })
    return records


def parse_du(text):
    """Parse `du -sh` output into a list of (bytes, path) records."""
    records = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        size, path = line.split(None, 1)
        records.append({"path": path.strip(), "size": size,
                        "bytes": parse_size(size)})
    return records


def exercise_3():
    """Parse `df -h` and `du -sh` text into a disk report."""
    records = parse_df(DF_TEXT)
    usage = parse_du(DU_TEXT)

    print("exercise_3 — disk_report")
    print("  df -h (as printed by the box):")
    print("    {:<16} {:>6} {:>6} {:>6} {:>5} {}".format(
        "Filesystem", "Size", "Used", "Avail", "Use%", "Mounted on"))
    for record in records:
        print("    {filesystem:<16} {size:>6} {used:>6} {avail:>6} {percent:>4}% {mount}".format(
            **record))

    real = [record for record in records if record["filesystem"].startswith("/dev/")]
    capacity = sum(record["size_bytes"] for record in real)
    used = sum(record["used_bytes"] for record in real)
    avail = sum(record["avail_bytes"] for record in real)
    print("  real file systems (tmpfs excluded): {}".format(len(real)))
    print("    capacity {}  used {}  available {}".format(
        human_size(capacity), human_size(used), human_size(avail)))

    crowded = [record for record in real if record["percent"] >= CROWDED_PERCENT]
    for record in crowded:
        print("  crowded: {} at {}% - free space in {} before the next download".format(
            record["mount"], record["percent"], record["mount"]))
    if not crowded:
        print("  crowded: none above {}%".format(CROWDED_PERCENT))

    usage.sort(key=lambda record: (-record["bytes"], record["path"]))
    print("  du -sh output, largest first:")
    for record in usage:
        print("    {:<8} {}".format(record["size"], record["path"]))
    top = usage[:3]
    print("  top 3 space hogs: {}".format(", ".join(
        "{0} {1}".format(record["size"], record["path"]) for record in top)))
    print("  tip from the lesson: du -h --max-depth=1 / 2>/dev/null | sort -hr | head -20")

    assert len(records) == 3 and len(real) == 2
    assert capacity == parse_size("98G") + parse_size("1.8T")
    assert used > avail
    assert [record["mount"] for record in crowded] == ["/data"]
    assert [record["path"] for record in top] == [
        "/data/checkpoints", "/data/tokenized", "/home/ubuntu/.cache"]
    assert human_size(12 * 2 ** 30) == "12G"
    assert human_size(340 * 2 ** 20) == "340M"
    print("[OK] exercise_3 — reported {} file systems and {} du entries".format(
        len(records), len(usage)))
    return {"capacity": capacity, "used": used, "avail": avail,
            "crowded": [record["mount"] for record in crowded]}


# ==========================================================================
# Exercise 4 - apt_install_plan
# ==========================================================================

# The packages the lesson installs on a fresh GPU box, in the lesson's order.
BASE_PACKAGES = (
    ("build-essential", "C compiler, make and friends — many Python packages need it"),
    ("git", "clone repositories"),
    ("curl", "HTTP downloads and API calls"),
    ("wget", "file downloads"),
    ("tmux", "terminal multiplexer — keeps training alive after a disconnect"),
    ("htop", "interactive process viewer"),
    ("unzip", "expand zip archives such as datasets"),
    ("python3-venv", "built-in virtual environments"),
)

APT_PLAN = (
    ("whoami", False, False, "check which user you are before anything else"),
    ("sudo apt update", True, False, "refresh the package list - always first"),
    ("sudo apt install -y build-essential git curl wget tmux htop unzip python3-venv",
     True, True, "install the whole fresh-box set in one shot"),
    ("apt list --installed", False, False, "confirm the packages are present"),
    ("nvidia-smi", False, False, "confirm driver and GPU are visible"),
    ("sudo apt clean", True, False, "clear the apt cache when disk runs low"),
)


def build_apt_plan():
    """Return the ordered install plan as a list of dicts."""
    plan = []
    for index, (command, needs_sudo, needs_update_first, purpose) in enumerate(
            APT_PLAN, start=1):
        plan.append({
            "step": index,
            "command": command,
            "sudo": needs_sudo,
            "after_update": needs_update_first,
            "purpose": purpose,
        })
    return plan


def missing_packages(installed, wanted):
    """Return the wanted packages that are not installed (sorted, stable)."""
    return sorted(name for name, _ in wanted if name not in installed)


def exercise_4():
    """Build an ordered apt install plan for a fresh GPU box."""
    plan = build_apt_plan()

    print("exercise_4 — apt_install_plan")
    print("  fresh GPU box, in this order:")
    for step in plan:
        marker = "sudo" if step["sudo"] else "user"
        print("    {}. [{}] {}".format(step["step"], marker, step["command"]))
        print("       {}".format(step["purpose"]))

    install = [step for step in plan if step["command"].startswith("apt install")
               or "apt install" in step["command"]][0]
    print("  packages in the install step ({}):".format(len(BASE_PACKAGES)))
    for name, purpose in BASE_PACKAGES:
        print("    {:<16} {}".format(name, purpose))

    installed_after = [name for name, _ in BASE_PACKAGES]
    print("  verification: apt list --installed | grep -c for the set")
    print("    missing after install: {}".format(
        missing_packages(installed_after, BASE_PACKAGES) or "none"))
    print("    still missing on a box with only git: {}".format(
        missing_packages(["git", "curl"], BASE_PACKAGES)))

    assert plan[1]["command"] == "sudo apt update", "update must come first"
    assert install["step"] == 3
    assert install["sudo"] and install["after_update"]
    for name, _ in BASE_PACKAGES:
        assert name in install["command"], "{} must be in the install command".format(name)
    assert install["command"].count("-y") == 1
    assert sum(1 for step in plan if step["sudo"]) == 3
    assert missing_packages(installed_after, BASE_PACKAGES) == []
    assert len(missing_packages(["git", "curl"], BASE_PACKAGES)) == 6
    print("[OK] exercise_4 — built a {}-step apt plan for {} packages".format(
        len(plan), len(BASE_PACKAGES)))
    return plan


# ==========================================================================
# Exercise 5 - macos_vs_linux
# ==========================================================================

# (macOS habit, Linux equivalent, the trap it causes)
PORTING_ROWS = (
    ("brew install htop", "sudo apt install htop", "package names differ"),
    ("open file.txt", "xdg-open file.txt", "no GUI on a remote box - use cat or less"),
    ("pbcopy, pbpaste", "not available", "no clipboard over SSH"),
    ("~/.zshrc", "~/.bashrc", "aliases written in the wrong rc file never load"),
    ("/opt/homebrew/", "/usr/bin/, /usr/local/bin/",
     "binaries live in different directories"),
    ("sed -i '' 's/a/b/' file", "sed -i 's/a/b/' file",
     "macOS sed needs an empty string after -i, Linux does not"),
    ("case-insensitive file system", "case-sensitive file system",
     "Model.py and model.py are two different files on Linux"),
    ("line endings \\n", "line endings \\n",
     "Windows \\r\\n breaks bash scripts - run dos2unix"),
)


def tabulate(rows, headers, widths):
    """Render a simple left-aligned text table."""
    lines = ["  " + " ".join(header.ljust(width)
                             for header, width in zip(headers, widths)).rstrip()]
    lines.append("  " + " ".join("-" * width for width in widths))
    for row in rows:
        lines.append("  " + " ".join(cell.ljust(width)
                                     for cell, width in zip(row, widths)).rstrip())
    return lines


def exercise_5():
    """Tabulate the macOS-versus-Linux differences and traps."""
    print("exercise_5 — macos_vs_linux")
    for line in tabulate(PORTING_ROWS, ("macOS", "Linux", "trap"), (30, 30, 46)):
        print(line)

    traps = sorted(row[2] for row in PORTING_ROWS)
    print("  traps worth memorising ({}):".format(len(traps)))
    for index, trap in enumerate(traps, start=1):
        print("    {:>2}. {}".format(index, trap))

    print("  most common tripping points on a remote box:")
    print("    1. a script that runs on macOS but is not executable on Linux")
    print("       -> chmod +x script.sh")
    print("    2. an alias that does nothing -> it is in ~/.zshrc, not ~/.bashrc")
    print("    3. a sed one-liner that fails -> remove the empty string after -i")
    print("    4. a missing import of a file that only differs in letter case")

    assert len(PORTING_ROWS) == 8
    assert len(traps) == len(PORTING_ROWS)
    assert PORTING_ROWS[5][0].startswith("sed -i ''")
    assert PORTING_ROWS[6][1] == "case-sensitive file system"
    assert "~/.bashrc" in [row[1] for row in PORTING_ROWS]
    assert "no clipboard over SSH" in traps
    print("[OK] exercise_5 — tabulated {} macOS-to-Linux differences".format(
        len(PORTING_ROWS)))
    return PORTING_ROWS


# ==========================================================================
# Exercise 6 - linux_ops_report
# ==========================================================================


def exercise_6():
    """Print one operations report over everything the lab produced."""
    mode_rows = [(path, mode_to_octal(mode)) for path, mode, _ in FILE_MODES]
    denials, fixes = [], []
    for path, mode, owner, group, action, user, groups, expected, fix in PERMISSION_CASES:
        allowed, _, _ = access_allowed(mode, owner, group, user, groups, action)
        if not allowed:
            denials.append("{} ({})".format(path, action))
            if fix not in fixes:
                fixes.append(fix)

    records = parse_df(DF_TEXT)
    usage = parse_du(DU_TEXT)
    real = [record for record in records if record["filesystem"].startswith("/dev/")]
    crowded = [record for record in real if record["percent"] >= CROWDED_PERCENT]
    capacity = sum(record["size_bytes"] for record in real)
    used = sum(record["used_bytes"] for record in real)
    available = sum(record["avail_bytes"] for record in real)
    biggest = max(usage, key=lambda record: record["bytes"])
    plan = build_apt_plan()

    print("exercise_6 — linux_ops_report")
    print("  ================ Linux operations report ================")
    print("  permissions : {} modes converted, {} denied, {} fixes".format(
        len(mode_rows), len(denials), len(fixes)))
    print("    octal modes: {}".format(", ".join(
        "{}={}".format(path, octal) for path, octal in mode_rows)))
    print("    denials    : {}".format("; ".join(denials)))
    print("    fixes      : {}".format("; ".join(fixes)))
    print("  disk        : {} file systems, capacity {}, used {}, available {}".format(
        len(records), human_size(capacity), human_size(used),
        human_size(available)))
    print("    crowded    : {} ({}%)".format(
        ", ".join(record["mount"] for record in crowded) or "none",
        crowded[0]["percent"] if crowded else 0))
    print("    biggest dir: {} {}".format(biggest["size"], biggest["path"]))
    print("  packages    : {} steps, {} packages in the install step".format(
        len(plan), len(BASE_PACKAGES)))
    print("    first step : {}".format(plan[0]["command"]))
    print("    install    : {}".format(plan[2]["command"]))
    print("  porting     : {} macOS-to-Linux differences tracked".format(
        len(PORTING_ROWS)))
    print("  verdict     : {} mode(s) to fix with chmod, {} path(s) to reclaim on {}, "
          "{} package(s) to install".format(
              len(fixes), len(crowded), crowded[0]["mount"] if crowded else "-",
              len(BASE_PACKAGES)))
    print("  =========================================================")

    assert len(mode_rows) == len(FILE_MODES)
    assert len(denials) == 3
    assert len(fixes) == 3
    assert len(records) == 3 and len(crowded) == 1
    assert used < capacity
    assert biggest["path"] == "/data/checkpoints"
    assert plan[0]["command"] == "whoami"
    assert len(plan) == len(APT_PLAN)
    print("[OK] exercise_6 — operations report over {} denials and {} file systems".format(
        len(denials), len(records)))
    return {"denials": len(denials), "fixes": len(fixes),
            "file_systems": len(records), "crowded": len(crowded),
            "plan_steps": len(plan)}


# ==========================================================================
# Runner
# ==========================================================================

EXERCISES = (
    ("exercise_1", exercise_1),
    ("exercise_2", exercise_2),
    ("exercise_3", exercise_3),
    ("exercise_4", exercise_4),
    ("exercise_5", exercise_5),
    ("exercise_6", exercise_6),
)


def main() -> int:
    print("=" * 74)
    print("Module 11 - Linux for AI : offline lab")
    print("=" * 74)
    passed = 0
    for name, function in EXERCISES:
        function()
        print()
        passed += 1
    print("[PASS] All {}/{} exercises passed successfully.".format(passed, len(EXERCISES)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
