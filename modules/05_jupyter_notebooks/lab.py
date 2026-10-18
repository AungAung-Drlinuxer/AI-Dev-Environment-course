#!/usr/bin/env python3
"""Lab — Module 05: Jupyter Notebooks.

Standard library only. Offline. Deterministic (no `random`).
The lab writes a small `.ipynb` file into a temporary directory, then reads it
back as JSON — exactly the way a notebook is stored on disk — and reports on
cell types, execution order, hidden state, timing and notebook-versus-script
fit. Run with:

    python3 modules/05_jupyter_notebooks/lab.py
"""

import json
import keyword
import os
import re
import tempfile
import time

# ---------------------------------------------------------------------------
# Names that a cell may use without defining them first.
# ---------------------------------------------------------------------------

BUILTINS = {
    "print", "len", "range", "int", "float", "str", "list", "dict", "set",
    "tuple", "sum", "min", "max", "abs", "enumerate", "zip", "sorted", "open",
    "repr", "isinstance", "type", "round", "True", "False", "None", "self",
}

ASSIGN_RE = re.compile(r"^\s*([A-Za-z_]\w*)\s*(?::[^=\n]+)?=(?!=)")
IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z_]\w*)")
IDENT_RE = re.compile(r"(?<!\.)\b[A-Za-z_]\w*\b")


# ---------------------------------------------------------------------------
# A real notebook, written to a temporary directory by build_sample_notebook().
# Cell order below is the order in the file (top to bottom). The
# `execution_count` values are deliberately not monotonic, and the last code
# cell depends on names that no earlier cell defines.
# ---------------------------------------------------------------------------

def _code(source, execution_count, outputs=None):
    return {
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs if outputs is not None else [],
        "source": source,
    }


def _markdown(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source,
    }


def build_sample_notebook(path):
    """Write a small .ipynb to `path` and return the path."""
    notebook = {
        "cells": [
            _markdown(["# Training experiment\n", "Prototype of a learning-rate run.\n"]),
            _code(["import math\n"], 1),
            _code(["x = 10\n"], 3),
            _code(["y = x * 2\n"], 2),
            _code(["print(y + 1)\n"], 4, [{"output_type": "stream", "name": "stdout", "text": ["21\n"]}]),
            _markdown(["## Plot\n", "The cell below needs a figure library.\n"]),
            _code(["plt.plot(losses)\n"], 5),
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(notebook, handle, ensure_ascii=False, indent=1)
    return path


# ---------------------------------------------------------------------------
# Helpers shared by the exercises.
# ---------------------------------------------------------------------------

def load_notebook(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def cell_source(cell):
    """A cell's `source` is a list of lines in nbformat 4; join it back."""
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(source)
    return source


def code_cells(notebook):
    return [c for c in notebook["cells"] if c.get("cell_type") == "code"]


def defined_names(source):
    names = set()
    for line in source.splitlines():
        match = ASSIGN_RE.match(line)
        if match:
            names.add(match.group(1))
        match = IMPORT_RE.match(line)
        if match:
            names.add(match.group(1))
    return names


def used_names(source):
    names = set()
    for token in IDENT_RE.findall(source):
        if token in BUILTINS or keyword.iskeyword(token):
            continue
        names.add(token)
    return names


# ---------------------------------------------------------------------------
# Exercise 1 — read_notebook
# ---------------------------------------------------------------------------

def exercise_1(path):
    """Parse the .ipynb JSON and split cells by type."""
    notebook = load_notebook(path)
    cells = notebook["cells"]
    by_type = {}
    for cell in cells:
        by_type[cell["cell_type"]] = by_type.get(cell["cell_type"], 0) + 1

    print("=== Exercise 1 — read_notebook ===")
    print(f"File: <tmp>/{os.path.basename(path)}")
    print(f"nbformat: {notebook['nbformat']}.{notebook['nbformat_minor']}")
    print(f"Total cells: {len(cells)}")
    for cell_type in sorted(by_type):
        print(f"  {cell_type:<9}: {by_type[cell_type]}")
    print(f"Code cells: {len(code_cells(notebook))}")

    assert len(cells) == 7
    assert by_type == {"markdown": 2, "code": 5}
    print("[OK] exercise_1 — cell count and types")
    return notebook


# ---------------------------------------------------------------------------
# Exercise 2 — execution_order_check
# ---------------------------------------------------------------------------

def exercise_2(notebook):
    """Detect out-of-order execution_count sequences."""
    pairs = []
    for index, cell in enumerate(code_cells(notebook)):
        pairs.append((index, cell.get("execution_count")))

    counts = [count for _, count in pairs]
    print("=== Exercise 2 — execution_order_check ===")
    print(f"execution_count in file order: {counts}")

    inversions = []
    for position in range(1, len(counts)):
        previous = counts[position - 1]
        current = counts[position]
        if previous is not None and current is not None and current < previous:
            inversions.append((position, previous, current))

    for position, previous, current in inversions:
        print(f"  index {position}: execution_count {current} runs after {previous} (out of order)")
    print(f"Out-of-order transitions: {len(inversions)}")
    if inversions:
        print("Verdict: notebook was NOT run top to bottom. Use Kernel > Restart & Run All.")
    else:
        print("Verdict: execution order is linear.")

    assert counts == [1, 3, 2, 4, 5]
    assert len(inversions) == 1
    print("[OK] exercise_2 — out-of-order execution detected")
    return inversions


# ---------------------------------------------------------------------------
# Exercise 3 — hidden_state_scan
# ---------------------------------------------------------------------------

def exercise_3(notebook):
    """Estimate which cells would fail after a restart from variable deps."""
    available = set()
    risky = []
    print("=== Exercise 3 — hidden_state_scan ===")
    for index, cell in enumerate(code_cells(notebook)):
        source = cell_source(cell)
        uses = used_names(source)
        defines = defined_names(source)
        missing = sorted(name for name in uses if name not in available and name not in defines)
        if missing:
            risky.append((index, cell.get("execution_count"), missing))
            print(f"  code cell {index}: uses {missing} before any cell defines it")
        available |= defines

    print(f"Cells at risk after 'Restart & Run All': {len(risky)}")
    if risky:
        print("Verdict: hidden state. A deleted or reordered cell provided these names.")
    else:
        print("Verdict: every name is defined before use.")

    assert [(index, missing) for index, _, missing in risky] == [(4, ["losses", "plt"])]
    print("[OK] exercise_3 — hidden state estimated from dependencies")
    return risky


# ---------------------------------------------------------------------------
# Exercise 4 — timeit_compare
# ---------------------------------------------------------------------------

def exercise_4(size=100_000):
    """Time two implementations of the same work (squares of 0..size-1)."""
    start = time.perf_counter()
    comprehension = [n * n for n in range(size)]
    comprehension_time = time.perf_counter() - start

    start = time.perf_counter()
    manual = []
    for n in range(size):
        manual.append(n * n)
    manual_time = time.perf_counter() - start

    print("=== Exercise 4 — timeit_compare ===")
    print(f"Work: squares of 0..{size - 1}")
    print("  list comprehension : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဂဏန်းအဖြစ် မပြပါ")
    print("  append loop        : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဂဏန်းအဖြစ် မပြပါ")
    print("  တိုင်းတာနည်း        : JupyterLab တွင် `%timeit` ဖြင့် ကိုယ်တိုင် တိုင်းပါ")
    print(f"  identical results  : {comprehension == manual}")

    assert comprehension == manual
    assert len(comprehension) == size
    assert comprehension_time > 0.0 and manual_time > 0.0
    print("[OK] exercise_4 — two implementations timed")
    return comprehension


# ---------------------------------------------------------------------------
# Exercise 5 — notebook_or_script
# ---------------------------------------------------------------------------

NOTEBOOK_TASKS = {
    "explore a dataset": "notebook",
    "prototype a model": "notebook",
    "visualize results": "notebook",
    "explain your work": "notebook",
    "quick experiments": "notebook",
    "training pipeline": "script",
    "reusable utilities": "script",
    "code with a __main__ guard": "script",
    "code that runs on a schedule": "script",
    "production code": "script",
}


def exercise_5():
    """Decide notebook versus script for a list of task types."""
    print("=== Exercise 5 — notebook_or_script ===")
    decisions = []
    for task in sorted(NOTEBOOK_TASKS):
        choice = NOTEBOOK_TASKS[task]
        decisions.append((task, choice))
        print(f"  {task:<28} -> {choice}")

    notebook_count = sum(1 for _, choice in decisions if choice == "notebook")
    script_count = len(decisions) - notebook_count
    print(f"Notebook fit: {notebook_count}   Script fit: {script_count}")
    print("Rule: explore in notebooks, ship in scripts.")

    assert notebook_count == 5 and script_count == 5
    print("[OK] exercise_5 — notebook versus script decided per task")
    return decisions


# ---------------------------------------------------------------------------
# Exercise 6 — notebook_health_report
# ---------------------------------------------------------------------------

def exercise_6(path):
    """Aggregate the trap checks into a single health report."""
    notebook = load_notebook(path)
    cells = notebook["cells"]
    types = {}
    for cell in cells:
        types[cell["cell_type"]] = types.get(cell["cell_type"], 0) + 1

    counts = [c.get("execution_count") for c in code_cells(notebook)]
    inversions = sum(1 for i in range(1, len(counts)) if counts[i] < counts[i - 1])

    available = set()
    risky = 0
    for cell in code_cells(notebook):
        source = cell_source(cell)
        missing = [n for n in used_names(source)
                   if n not in available and n not in defined_names(source)]
        if missing:
            risky += 1
        available |= defined_names(source)

    print("=== Exercise 6 — notebook_health_report ===")
    print(f"cells          : {len(cells)} (code {types.get('code', 0)}, markdown {types.get('markdown', 0)})")
    print(f"execution order: {'linear' if inversions == 0 else str(inversions) + ' out-of-order transition(s)'}")
    print(f"hidden state   : {risky} cell(s) at risk after restart")
    healthy = inversions == 0 and risky == 0
    print(f"overall        : {'HEALTHY' if healthy else 'NEEDS FIX (Restart & Run All before sharing)'}")

    assert len(cells) == 7
    assert inversions == 1
    assert risky == 1
    assert healthy is False
    print("[OK] exercise_6 — notebook health report")
    return {"cells": len(cells), "inversions": inversions, "risky": risky, "healthy": healthy}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print("Notebook health lab (standard library only, offline)\n")
    with tempfile.TemporaryDirectory(prefix="nb_lab_") as tmp:
        path = os.path.join(tmp, "sample.ipynb")
        build_sample_notebook(path)
        print(f"Sample notebook written to a temporary directory: {os.path.basename(path)}\n")
        notebook = exercise_1(path)
        exercise_2(notebook)
        exercise_3(notebook)
        exercise_4()
        exercise_5()
        exercise_6(path)
    print("\n[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
