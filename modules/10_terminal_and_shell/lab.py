#!/usr/bin/env python3
"""Module 10 - Terminal & Shell: offline lab (standard library only).

The six exercises of this module are shell workflows.  Python cannot call
`grep`, `sort`, `tail`, `awk` or `tmux` here (no shelling out, no network),
so every stage is *modelled* in pure Python and run on a fake training log
that this file writes once into a temporary directory.

Run from the repository root:

    python3 modules/10_terminal_and_shell/lab.py

Every exercise prints a readable result and then one line

    [OK] exercise_N - <short description>

The script ends with `[PASS] All 6/6 exercises passed successfully.` and
exits 0.  Output is deterministic: the log is generated from a formula, so
it is identical on every run.
"""

from __future__ import annotations

import datetime as _dt
import math
import os
import re
import tempfile

# --------------------------------------------------------------------------
# The fake training log
# --------------------------------------------------------------------------

EPOCHS = 100
LOG_NAME = "train.log"
BEST_NAME = "losses_sorted.txt"
TAIL_NAME = "losses_tail5.txt"
SESSION = "training"

BASE_TIME = _dt.datetime(2026, 1, 1, 0, 0, 0)

# The log is written in the format the lesson's Exercise 3 produces:
#   epoch <n> loss: <value>
# with a timestamp and a learning rate in front, so that
# `awk '{print $NF}'` really does print the loss value.
EPOCH_LINE_RE = re.compile(
    r"^\[(?P<ts>[^\]]+)\]\s+epoch\s+(?P<epoch>\d+)/(?P<total>\d+)\s+"
    r"lr:\s+(?P<lr>[0-9.eE+-]+)\s+loss:\s+(?P<loss>[0-9.]+)\s*$"
)
LEVEL_LINE_RE = re.compile(
    r"^\[(?P<ts>[^\]]+)\]\s+(?P<level>ERROR|WARNING)\s+-\s+(?P<message>.+)$"
)

WARNING_EPOCHS = (18, 55, 88)
ERROR_EPOCHS = (37, 74)


def _timestamp(offset_seconds: int) -> str:
    """Format BASE_TIME + offset as `YYYY-mm-dd HH:MM:SS`."""
    moment = BASE_TIME + _dt.timedelta(seconds=offset_seconds)
    return moment.strftime("%Y-%m-%d %H:%M:%S")


def _loss_for(epoch: int) -> float:
    """Deterministic loss: exponential decay plus a small saw-tooth ripple."""
    decay = 2.5 * math.exp(-epoch / 25.0)
    ripple = 0.02 * ((epoch * 7) % 5)
    return round(decay + ripple, 4)


def build_log_text() -> str:
    """Build the whole fake training log as one string."""
    lines = []
    clock = 0
    for epoch in range(1, EPOCHS + 1):
        clock += 1
        lines.append(
            "[{ts}] epoch {e}/{total} lr: 1.00e-04 loss: {loss:.4f}".format(
                ts=_timestamp(clock), e=epoch, total=EPOCHS, loss=_loss_for(epoch)
            )
        )
        if epoch in WARNING_EPOCHS:
            clock += 1
            lines.append(
                "[{ts}] WARNING - gradient norm {gn:.2f} clipped".format(
                    ts=_timestamp(clock), gn=1.0 + (epoch % 7) * 0.3
                )
            )
        if epoch in ERROR_EPOCHS:
            clock += 1
            lines.append(
                "[{ts}] ERROR - CUDA out of memory at step {step}".format(
                    ts=_timestamp(clock), step=epoch * 16
                )
            )
    clock += 1
    lines.append("[{ts}] final_accuracy=0.8731".format(ts=_timestamp(clock)))
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# A tiny shared workspace (created once, on demand)
# --------------------------------------------------------------------------

_WORKSPACE = None


def workspace() -> str:
    """Create the temporary directory and write `train.log` into it, once."""
    global _WORKSPACE
    if _WORKSPACE is None:
        _WORKSPACE = tempfile.mkdtemp(prefix="mod10_terminal_lab_")
        with open(log_path(), "w", encoding="utf-8") as handle:
            handle.write(build_log_text())
    return _WORKSPACE


def log_path() -> str:
    """Absolute path of the fake training log."""
    return os.path.join(workspace(), LOG_NAME)


def read_lines(path: str):
    """`cat`: read a file into a list of lines without the newline."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().splitlines()


def write_lines(path: str, lines, append: bool = False) -> None:
    """`>` (overwrite) or `>>` (append) for a list of lines."""
    mode = "a" if append else "w"
    with open(path, mode, encoding="utf-8") as handle:
        for line in lines:
            handle.write(line + "\n")


# --------------------------------------------------------------------------
# grep / awk / sort / tail semantics
# --------------------------------------------------------------------------


def grep(pattern: str, lines, invert: bool = False, ignore_case: bool = False):
    """`grep <pattern>`: keep the lines in which the pattern is found."""
    flags = re.IGNORECASE if ignore_case else 0
    compiled = re.compile(pattern, flags)
    kept = []
    for line in lines:
        matched = compiled.search(line) is not None
        if matched != invert:
            kept.append(line)
    return kept


def awk_last_field(lines):
    """`awk '{print $NF}'`: the last whitespace-separated field of each line."""
    return [line.split()[-1] for line in lines if line.split()]


def sort_numeric(values, reverse: bool = False):
    """`sort -n` (numeric) and, with reverse=True, `sort -n -r`."""
    return sorted(values, key=float, reverse=reverse)


def tail(items, count: int):
    """`tail -n <count>` on a list of items."""
    if count >= len(items):
        return list(items)
    return list(items[-count:])


def head(items, count: int):
    """`head -n <count>` on a list of items."""
    return list(items[:count])


def parse_records(lines):
    """Split the log into epoch records, level records and everything else."""
    epochs, levels, others = [], [], []
    for line in lines:
        hit = EPOCH_LINE_RE.match(line)
        if hit:
            epochs.append(
                {
                    "timestamp": hit.group("ts"),
                    "epoch": int(hit.group("epoch")),
                    "total": int(hit.group("total")),
                    "lr": hit.group("lr"),
                    "loss": float(hit.group("loss")),
                }
            )
            continue
        hit = LEVEL_LINE_RE.match(line)
        if hit:
            levels.append(
                {
                    "timestamp": hit.group("ts"),
                    "level": hit.group("level"),
                    "message": hit.group("message"),
                }
            )
            continue
        others.append(line)
    return epochs, levels, others


# ==========================================================================
# Exercise 1 - parse_training_log
# ==========================================================================


def exercise_1():
    """Parse epoch/loss lines out of the fake training log."""
    path = log_path()
    lines = read_lines(path)
    epochs, levels, others = parse_records(lines)

    print("exercise_1 - parse_training_log")
    print("  file      : {}".format(LOG_NAME))
    print("  path      : <tmp>/{}".format(LOG_NAME))
    print("  total lines: {}".format(len(lines)))
    print("  epoch records : {}".format(len(epochs)))
    print("  level records : {} (ERROR {}, WARNING {})".format(
        len(levels),
        len([r for r in levels if r["level"] == "ERROR"]),
        len([r for r in levels if r["level"] == "WARNING"]),
    ))
    print("  other records : {}".format(len(others)))
    print("  first 3 epochs:")
    for record in head(epochs, 3):
        print("    epoch {epoch:>3}/{total} lr {lr} loss {loss:.4f}".format(**record))
    print("  last 3 epochs:")
    for record in tail(epochs, 3):
        print("    epoch {epoch:>3}/{total} lr {lr} loss {loss:.4f}".format(**record))
    print("  unparsed line: {!r}".format(others[0] if others else ""))

    assert len(epochs) == EPOCHS
    assert len(levels) == len(WARNING_EPOCHS) + len(ERROR_EPOCHS)
    assert len(others) == 1, "only the final_accuracy line stays unparsed"
    assert epochs[0]["epoch"] == 1 and epochs[-1]["epoch"] == EPOCHS
    assert all(r["loss"] > 0 for r in epochs)
    print("[OK] exercise_1 - parsed {} epoch records and {} level records".format(
        len(epochs), len(levels)))
    return epochs, levels


# ==========================================================================
# Exercise 2 - filter_lines
# ==========================================================================


def exercise_2():
    """Filter the log with grep semantics."""
    lines = read_lines(log_path())
    epochs, levels, _ = parse_records(lines)

    loss_lines = grep("loss:", lines)
    error_lines = grep("ERROR", lines)
    warn_lines = grep("WARNING", lines)
    quiet_lines = grep("ERROR|WARNING", lines, invert=True)
    early_lines = grep(r"epoch (1|2|3)/", lines)

    print("exercise_2 - filter_lines (grep semantics)")
    print("  grep 'loss:'            -> {} lines".format(len(loss_lines)))
    print("    first : {}".format(loss_lines[0]))
    print("    last  : {}".format(loss_lines[-1]))
    print("  grep 'ERROR'            -> {} lines".format(len(error_lines)))
    for line in error_lines:
        print("    {}".format(line))
    print("  grep 'WARNING'          -> {} lines".format(len(warn_lines)))
    print("  grep -v 'ERROR|WARNING' -> {} lines".format(len(quiet_lines)))
    print("  grep -E 'epoch (1|2|3)/' -> {} lines".format(len(early_lines)))
    for line in early_lines:
        print("    {}".format(line))
    print("  grep -i 'cuda'          -> {} lines".format(
        len(grep("cuda", lines, ignore_case=True))))

    assert len(loss_lines) == len(epochs) == EPOCHS
    assert len(error_lines) == len(ERROR_EPOCHS)
    assert len(warn_lines) == len(WARNING_EPOCHS)
    assert len(quiet_lines) == len(lines) - len(error_lines) - len(warn_lines)
    assert len(early_lines) == 3
    assert len(grep("cuda", lines, ignore_case=True)) == len(ERROR_EPOCHS)
    print("[OK] exercise_2 - grep filtered {} lines down to {} loss lines".format(
        len(lines), len(loss_lines)))
    return loss_lines


# ==========================================================================
# Exercise 3 - run_pipeline
# ==========================================================================


def exercise_3():
    """Model `cat | grep | awk | sort | head > file` stage by stage."""
    stages = []
    lines = read_lines(log_path())
    stages.append(("cat {}".format(LOG_NAME), len(lines), None))

    matched = grep("loss:", lines)
    stages.append(("grep 'loss:'", len(matched), matched[0]))

    values = awk_last_field(matched)
    stages.append(("awk '{print $NF}'", len(values), values[0]))

    ascending = sort_numeric(values)
    stages.append(("sort -n", len(ascending), ascending[0]))

    smallest = head(ascending, 5)
    stages.append(("head -5", len(smallest), smallest[0]))

    best_out = os.path.join(workspace(), BEST_NAME)
    write_lines(best_out, smallest)
    stages.append(("> {}".format(BEST_NAME), len(smallest), smallest[0]))

    tail5 = tail(ascending, 5)
    tail_out = os.path.join(workspace(), TAIL_NAME)
    write_lines(tail_out, tail5)
    write_lines(tail_out, ["# appended by >> {}".format(TAIL_NAME)], append=True)
    stages.append(("tail -5 >> {}".format(TAIL_NAME), len(tail5) + 1, tail5[0]))

    print("exercise_3 - run_pipeline")
    print("  pipeline: cat {0} | grep 'loss:' | awk '{{print $NF}}' "
          "| sort -n | head -5 > {1}".format(LOG_NAME, BEST_NAME))
    for index, (stage, count, sample) in enumerate(stages, start=1):
        print("    stage {n}: {stage:<34} -> {count:>3} lines"
              .format(n=index, stage=stage, count=count))

    print("  file {0} after redirect (>):".format(BEST_NAME))
    for line in read_lines(best_out):
        print("    {}".format(line))
    print("  file {0} after append (>>):".format(TAIL_NAME))
    for line in read_lines(tail_out):
        print("    {}".format(line))

    assert values == [line.split()[-1] for line in matched]
    assert ascending == sorted(values, key=float)
    assert read_lines(best_out) == smallest
    appended = read_lines(tail_out)
    assert appended[-1] == "# appended by >> {}".format(TAIL_NAME)
    assert appended[:-1] == tail5
    print("[OK] exercise_3 - pipeline of {} stages wrote 2 files".format(len(stages)))
    return smallest, tail5


# ==========================================================================
# Exercise 4 - loss_statistics
# ==========================================================================


def exercise_4():
    """Summarise the loss values with tail statistics."""
    lines = read_lines(log_path())
    values = awk_last_field(grep("loss:", lines))
    numbers = [float(value) for value in values]
    epochs, _, _ = parse_records(lines)

    total = len(numbers)
    mean = sum(numbers) / total
    last_ten = tail(numbers, 10)
    first_ten = head(numbers, 10)
    mean_last_ten = sum(last_ten) / len(last_ten)
    mean_first_ten = sum(first_ten) / len(first_ten)
    lowest = min(numbers)
    highest = max(numbers)
    best_epoch = numbers.index(lowest) + 1

    print("exercise_4 - loss_statistics")
    print("  values        : {}".format(total))
    print("  min loss      : {:.4f} (epoch {})".format(lowest, best_epoch))
    print("  max loss      : {:.4f} (epoch {})".format(highest, numbers.index(highest) + 1))
    print("  mean loss     : {:.4f}".format(mean))
    print("  mean of head -10 : {:.4f}".format(mean_first_ten))
    print("  mean of tail -10 : {:.4f}".format(mean_last_ten))
    print("  tail -10 values :")
    for epoch, value in zip(range(total - 9, total + 1), last_ten):
        print("    epoch {e:>3} loss {v:.4f}".format(e=epoch, v=value))
    print("  improvement head->tail: {:.4f}".format(mean_first_ten - mean_last_ten))
    print("  final epoch loss from log: {:.4f}".format(epochs[-1]["loss"]))

    assert total == EPOCHS
    assert lowest <= mean <= highest
    assert mean_last_ten < mean_first_ten, "loss must go down over training"
    assert abs(epochs[-1]["loss"] - numbers[-1]) < 1e-9
    print("[OK] exercise_4 - loss dropped from {:.4f} to {:.4f} (mean tail -10)".format(
        mean_first_ten, mean_last_ten))
    return {
        "count": total,
        "min": lowest,
        "max": highest,
        "mean": mean,
        "mean_tail_10": mean_last_ten,
        "best_epoch": best_epoch,
    }


# ==========================================================================
# Exercise 5 - tmux_plan
# ==========================================================================


def exercise_5():
    """Build the tmux command sequence for a three-pane training session."""
    commands = [
        "tmux new-session -d -s {s} -n train".format(s=SESSION),
        "tmux split-window -h -t {s}".format(s=SESSION),
        "tmux split-window -v -t {s}".format(s=SESSION),
        "tmux send-keys -t {s}:0.0 'python train.py --epochs 100 --lr 1e-4' C-m".format(s=SESSION),
        "tmux send-keys -t {s}:0.1 'watch -n1 nvidia-smi' C-m".format(s=SESSION),
        "tmux send-keys -t {s}:0.2 'tail -f logs/experiment.log' C-m".format(s=SESSION),
        "tmux select-pane -t {s}:0.0".format(s=SESSION),
        "tmux attach -t {s}".format(s=SESSION),
    ]
    panes = [
        ("{s}:0.0".format(s=SESSION), "Training run", "python train.py --epochs 100 --lr 1e-4"),
        ("{s}:0.1".format(s=SESSION), "GPU monitor", "watch -n1 nvidia-smi"),
        ("{s}:0.2".format(s=SESSION), "Logs", "tail -f logs/experiment.log"),
    ]
    keys = [
        ("Ctrl+B then \"", "split the window horizontally"),
        ("Ctrl+B then %", "split the window vertically"),
        ("Ctrl+B then arrow key", "move between panes"),
        ("Ctrl+B then d", "detach; the session keeps running"),
    ]

    print("exercise_5 - tmux_plan")
    print("  session: {!r} with {} panes".format(SESSION, len(panes)))
    for target, title, program in panes:
        print("    pane {t:<10} {title:<14} runs: {program}".format(
            t=target, title=title, program=program))
    print("  command sequence:")
    for index, command in enumerate(commands, start=1):
        print("    {n}. {c}".format(n=index, c=command))
    print("  key bindings (prefix Ctrl+B):")
    for combo, purpose in keys:
        print("    {combo:<24} {purpose}".format(combo=combo, purpose=purpose))
    print("  reattach later with: tmux attach -t {s}".format(s=SESSION))
    print("  list sessions with : tmux ls")

    assert commands[0].startswith("tmux new-session -d -s {}".format(SESSION))
    assert sum(1 for c in commands if "split-window" in c) == 2
    assert sum(1 for c in commands if "send-keys" in c) == 3
    assert "watch -n1 nvidia-smi" in commands[4]
    assert commands[-1] == "tmux attach -t {}".format(SESSION)
    print("[OK] exercise_5 - built {}-command plan for {} panes".format(
        len(commands), len(panes)))
    return commands


# ==========================================================================
# Exercise 6 - log_ops_report
# ==========================================================================


def exercise_6():
    """Print one operations report over everything the lab produced."""
    path = log_path()
    lines = read_lines(path)
    epochs, levels, others = parse_records(lines)
    values = [float(v) for v in awk_last_field(grep("loss:", lines))]
    errors = [r for r in levels if r["level"] == "ERROR"]
    warnings = [r for r in levels if r["level"] == "WARNING"]

    # Exercise 4 prints a lot; recompute the few numbers the report needs.
    mean_loss = sum(values) / len(values)
    mean_tail_10 = sum(tail(values, 10)) / 10
    best_epoch = values.index(min(values)) + 1
    size_bytes = os.path.getsize(path)
    tail_file = os.path.join(workspace(), TAIL_NAME)

    print("exercise_6 - log_ops_report")
    print("  ==================== operations report ====================")
    print("  log file          : {} ({} bytes)".format(LOG_NAME, size_bytes))
    print("  workspace         : <tmp>")
    print("  total lines       : {}".format(len(lines)))
    print("  epoch lines       : {}".format(len(epochs)))
    print("  ERROR lines       : {} -> {}".format(
        len(errors), "; ".join(r["message"] for r in errors)))
    print("  WARNING lines     : {}".format(len(warnings)))
    print("  other lines       : {} -> {!r}".format(
        len(others), others[0] if others else ""))
    print("  loss min / mean / max : {:.4f} / {:.4f} / {:.4f}".format(
        min(values), mean_loss, max(values)))
    print("  mean of tail -10 loss : {:.4f}".format(mean_tail_10))
    print("  best epoch            : {}".format(best_epoch))
    print("  pipeline artifacts    : {}, {}".format(BEST_NAME, TAIL_NAME))
    print("  tail artifact exists  : {}".format(os.path.exists(tail_file)))
    print("  tmux session plan     : {} panes in '{}'".format(3, SESSION))
    print("  verdict               : log readable, loss decreasing, "
          "{} errors to review".format(len(errors)))
    print("  ==========================================================")

    assert len(lines) == len(epochs) + len(levels) + len(others)
    assert size_bytes > 0
    assert len(errors) == len(ERROR_EPOCHS)
    assert mean_tail_10 < mean_loss, "later epochs must be better than the average"
    assert os.path.exists(tail_file)
    print("[OK] exercise_6 - ops report over {} lines, {} errors, {} warning".format(
        len(lines), len(errors), len(warnings)))
    return {
        "lines": len(lines),
        "epochs": len(epochs),
        "errors": len(errors),
        "warnings": len(warnings),
        "mean_loss": mean_loss,
    }


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
    print("Module 10 - Terminal & Shell : offline lab")
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
