#!/usr/bin/env python3
"""ဤ course ၏ lab အားလုံးကို တစ်ကြိမ်တည်း run စစ်သည့် runner။

အသုံးပြုနည်း —
    python3 run_all_labs.py                 # module အားလုံး
    python3 run_all_labs.py --module 03     # module တစ်ခုသာ
    python3 run_all_labs.py --verbose       # lab တိုင်း၏ stdout ကို အပြည့် ပြ

Lab တိုင်းသည် offline နှင့် deterministic ဖြစ်သဖြင့် network၊ Docker၊ GPU မလိုပါ။
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent
MODULES = REPO / "modules"


def discover(only: str | None):
    found = []
    for lab in sorted(MODULES.glob("*/lab.py")):
        name = lab.parent.name
        if only and not name.startswith(only):
            continue
        found.append((name, lab))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description="Run every module lab in this course.")
    ap.add_argument("--module", default=None, help="run one module only, e.g. 03 or 03_gpu_setup_and_cloud")
    ap.add_argument("--verbose", action="store_true", help="print each lab's full output")
    args = ap.parse_args()

    labs = discover(args.module)
    if not labs:
        print("No lab.py found. Expected modules/<NN_folder>/lab.py")
        return 1

    print("=" * 78)
    print("AI Development Environment — module labs")
    print("=" * 78)
    print(f"{'Module':38} {'Exercises':>9} {'Status':>8} {'Time':>8}")
    print("-" * 78)

    failures, total_ex, started = 0, 0, time.perf_counter()
    for name, path in labs:
        t0 = time.perf_counter()
        proc = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, cwd=REPO)
        dt = time.perf_counter() - t0
        out = (proc.stdout or "") + (proc.stderr or "")
        exercises = out.count("[OK] exercise_")
        status = "PASS" if proc.returncode == 0 else "FAIL"
        if proc.returncode != 0:
            failures += 1
        total_ex += exercises
        print(f"{name:38} {exercises:>9} {status:>8} {dt:>7.2f}s")
        if args.verbose or proc.returncode != 0:
            print("-" * 78)
            print(out.rstrip())
            print("-" * 78)

    elapsed = time.perf_counter() - started
    print("=" * 78)
    print(f"TOTAL: {len(labs)} modules, {total_ex} exercises executed in {elapsed:.2f}s")
    print("[SUCCESS] All lab checks passed." if not failures else f"[FAILURE] {failures} module(s) failed.")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
