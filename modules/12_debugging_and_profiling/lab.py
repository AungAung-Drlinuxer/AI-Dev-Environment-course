#!/usr/bin/env python3
"""Module 12 — Debugging & Profiling: offline lab.

ဤ lab သည် AI code ၏ တိတ်ဆိတ်စွာ ကျရှုံးသည့် bug များကို ဖမ်းသည့် နည်းလမ်း ခြောက်ခုကို
torch မလိုဘဲ Python standard library သာ ဖြင့် သရုပ်ပြသည်။ Nested list ကို tensor
အဖြစ် ကိုယ်စားပြုပြီး shape၊ dtype နှင့် NaN ကို ကြည့်ရှုခြင်း၊ သုညဖြင့် စားခြင်းမှ
ဖြစ်သော NaN ကို တကယ် ဖန်တီး၍ ဖမ်းခြင်း၊ matmul shape ကို မြှောက်မီ စစ်ခြင်း၊
cProfile-style stats ဇယားမှ နှေးဆုံး function ကို ရှာခြင်း၊ tracemalloc-style snapshot
မှ အများဆုံး allocate လုပ်သည့် နေရာကို ရှာခြင်း နှင့် loss curve မှ overfit ဖြစ်/မဖြစ်
ဆုံးဖြတ်ခြင်း တို့ ပါဝင်သည်။

Library သည် standard library သာ ဖြစ်သည်။ Network၊ Docker၊ GPU၊ torch မလိုပါ။
ရလဒ်သည် deterministic ဖြစ်သည် — wall-clock time ကို ပုံနှိပ်မထုတ်ပါ။
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Nested list ကို tensor အဖြစ် ကိုယ်စားပြုသည့် အခြေခံ function များ
# ---------------------------------------------------------------------------


def tensor_shape(data) -> tuple:
    """Nested list ၏ shape ကို tuple အဖြစ် ပြန်သည် — e.g. [[1,2],[3,4]] -> (2, 2)။"""
    shape = []
    node = data
    while isinstance(node, (list, tuple)):
        shape.append(len(node))
        node = node[0] if node else None
    return tuple(shape)


def flatten(data) -> list:
    """Nested list ကို တစ်လိုင်း (flat) list အဖြစ် ပြန်သည်။"""
    out = []
    if isinstance(data, (list, tuple)):
        for item in data:
            out.extend(flatten(item))
    else:
        out.append(data)
    return out


def infer_dtype(values: list) -> str:
    """Element များမှ dtype ကို ခန့်မှန်းသည် — bool / float32 / int64။"""
    has_bool = any(isinstance(v, bool) for v in values)
    has_float = any(isinstance(v, float) for v in values)
    has_int = any(isinstance(v, int) and not isinstance(v, bool) for v in values)
    if has_bool and not (has_float or has_int):
        return "bool"
    if has_float:
        return "float32"
    if has_int:
        return "int64"
    return "unknown"


def count_nan(values: list) -> int:
    """NaN element အရေအတွက်ကို ရေတွက်သည်။"""
    return sum(1 for v in values if isinstance(v, float) and math.isnan(v))


def count_inf(values: list) -> int:
    """Inf element အရေအတွက်ကို ရေတွက်သည်။"""
    return sum(1 for v in values if isinstance(v, float) and math.isinf(v))


def make_batch(rows: int = 3, cols: int = 4) -> list:
    """Deterministic float batch တစ်ခု တည်ဆောက်သည် (random မသုံးပါ)။"""
    return [
        [round(((i * 7 + j * 13) % 17) / 4.0 - 2.0, 4) for j in range(cols)]
        for i in range(rows)
    ]


# ---------------------------------------------------------------------------
# Exercise 1 — debug_print
# ---------------------------------------------------------------------------
def debug_print(name: str, data, device: str = "cpu") -> dict:
    """Tensor အလားတူ nested list တစ်ခု၏ shape၊ dtype၊ min/max/mean နှင့် NaN ကို ပြသည်။

    Source ၏ `debug_print(name, tensor)` ပုံစံအတိုင်း ဖြစ်သည် — min/max/mean တို့ကို
    NaN/Inf မဟုတ်သည့် တန်ဖိုးများအပေါ်တွင်သာ တွက်သဖြင့် ဖတ်ရန် လွယ်သည်။
    NaN ရှိ/မရှိ ကို `has_nan` တွင် သီးခြား ပြသည်။
    """
    values = flatten(data)
    nan_count = count_nan(values)
    inf_count = count_inf(values)
    finite = [
        v
        for v in values
        if not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))
    ]
    lo = min(finite) if finite else float("nan")
    hi = max(finite) if finite else float("nan")
    mean = (sum(finite) / len(finite)) if finite else float("nan")

    info = {
        "name": name,
        "shape": tensor_shape(data),
        "dtype": infer_dtype(values),
        "device": device,
        "min": lo,
        "max": hi,
        "mean": mean,
        "has_nan": nan_count > 0,
        "nan_count": nan_count,
        "inf_count": inf_count,
        "count": len(values),
    }
    print(
        f"  {name}: shape={info['shape']}, dtype={info['dtype']}, device={info['device']}, "
        f"min={lo:.4f}, max={hi:.4f}, mean={mean:.4f}, has_nan={info['has_nan']}"
    )
    return info


def exercise_1() -> dict:
    print("Exercise 1 — debug_print (nested list မှ shape၊ dtype၊ NaN ကို ကြည့်ရှုခြင်း)")
    batch = make_batch(3, 4)
    clean = debug_print("input batch", batch)
    print(f"  element count : {clean['count']}")

    injected = [row[:] for row in batch]
    injected[1][2] = float("nan")
    with_nan = debug_print("injected NaN", injected)

    assert clean["shape"] == (3, 4), "shape သည် (3, 4) ဖြစ်ရမည်"
    assert clean["dtype"] == "float32", "dtype သည် float32 ဖြစ်ရမည်"
    assert clean["has_nan"] is False, "original batch တွင် NaN မရှိရ"
    assert with_nan["has_nan"] is True, "NaN ထည့်ပြီးနောက် has_nan သည် True ဖြစ်ရမည်"
    assert with_nan["nan_count"] == 1, "NaN တစ်ခုသာ ရှိရမည်"
    assert clean["min"] == -2.0 and clean["max"] == 2.0, "min/max တန်ဖိုး မှားနေသည်"

    print("[OK] exercise_1 — debug_print ဖြင့် shape၊ dtype၊ NaN ကို စစ်ဆေးပြီးပါသည်")
    return {"clean": clean, "with_nan": with_nan}


# ---------------------------------------------------------------------------
# Exercise 2 — nan_detector
# ---------------------------------------------------------------------------
def forward_pass(inputs: list, divisor: float) -> list:
    """Element တိုင်းကို divisor ဖြင့် စားသည့် forward pass (nested list အဆင့်)။"""
    return [value / divisor for value in inputs]


def nan_detector(values: list, step: int) -> dict:
    """NaN နှင့် Inf ရှိသည့် index များကို ရှာသည် — source ၏ `detect_nan` ပုံစံ။"""
    nan_indices = [
        i for i, v in enumerate(values) if isinstance(v, float) and math.isnan(v)
    ]
    inf_indices = [
        i for i, v in enumerate(values) if isinstance(v, float) and math.isinf(v)
    ]
    return {
        "step": step,
        "has_nan": bool(nan_indices),
        "nan_indices": nan_indices,
        "inf_indices": inf_indices,
        "count": len(values),
    }


def exercise_2() -> dict:
    print("Exercise 2 — nan_detector (သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို ဖမ်းခြင်း)")

    raised = None
    try:
        1.0 / 0.0
    except ZeroDivisionError as exc:
        raised = type(exc).__name__
        print(f"  1.0 / 0.0 -> {raised}: {exc}")

    # IEEE 754 — divisor သည် non-finite ဖြစ်သောအခါ စားခြင်းသည် exception မမြှင့်ဘဲ NaN ကို ပြန်သည်။
    divisor = float("inf")
    inputs = [1.0, 2.0, float("inf"), -4.0]
    outputs = forward_pass(inputs, divisor)
    print(f"  forward pass   : inputs={inputs}, divisor={divisor}")
    print(f"  outputs        : {outputs}")

    report = nan_detector(outputs, step=500)
    print(
        f"  step {report['step']}      : has_nan={report['has_nan']}, "
        f"nan_indices={report['nan_indices']}, inf_indices={report['inf_indices']}"
    )

    assert raised == "ZeroDivisionError", "1.0/0.0 သည် ZeroDivisionError ဖြစ်ရမည်"
    assert report["has_nan"] is True, "NaN ကို ဖမ်းနိုင်ရမည်"
    assert report["nan_indices"] == [2], "NaN သည် index 2 တွင် ရှိရမည်"
    assert math.isnan(outputs[2]), "outputs[2] သည် NaN ဖြစ်ရမည်"
    assert outputs[0] == 0.0, "finite / inf = 0.0 ဖြစ်သည်"

    print("[OK] exercise_2 — စားခြင်းမှ ဖြစ်သော NaN ကို ဖန်တီး၍ ဖမ်းပြီးပါသည်")
    return {"report": report, "outputs": outputs}


# ---------------------------------------------------------------------------
# Exercise 3 — check_shapes
# ---------------------------------------------------------------------------
def check_shapes(a_shape: tuple, b_shape: tuple) -> dict:
    """matmul မလုပ်မီ shape နှစ်ခု တိုက်ဆိုင်/မတိုက်ဆိုင် စစ်သည်။

    Matmul အတွက် လိုအပ်ချက်သည် `a[1] == b[0]` ဖြစ်သည်။ Output shape သည်
    `(a[0], b[1])` ဖြစ်သည်။ မတိုက်ဆိုင်ပါက ရှင်းလင်းသည့် အကြောင်းပြချက်ကို ပြန်သည်။
    """
    if len(a_shape) != 2 or len(b_shape) != 2:
        return {
            "ok": False,
            "reason": "matmul အတွက် 2D shape နှစ်ခု လိုအပ်သည်",
            "out_shape": None,
        }
    if a_shape[1] != b_shape[0]:
        return {
            "ok": False,
            "reason": f"inner dimension မတိုက်ဆိုင်: a[1]={a_shape[1]} != b[0]={b_shape[0]}",
            "out_shape": None,
        }
    return {
        "ok": True,
        "reason": "shapes တိုက်ဆိုင်သည်",
        "out_shape": (a_shape[0], b_shape[1]),
    }


def matmul(a: list, b: list) -> list:
    """Shape စစ်ပြီးသော nested list နှစ်ခုကို မြှောက်သည်။"""
    n = len(a)
    k = len(b)
    m = len(b[0])
    out = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for p in range(k):
            av = a[i][p]
            for j in range(m):
                out[i][j] += av * b[p][j]
    return out


def exercise_3() -> dict:
    print("Exercise 3 — check_shapes (matmul shape မတိုက်ဆိုင်ခြင်းကို ကြိုတင် ဖမ်းခြင်း)")

    cases = [((4, 784), (784, 256)), ((4, 784), (256, 10)), ((4,), (4, 4))]
    results = []
    for a_shape, b_shape in cases:
        result = check_shapes(a_shape, b_shape)
        results.append((a_shape, b_shape, result))
        status = "OK" if result["ok"] else "REJECT"
        print(f"  {a_shape} @ {b_shape} -> {status}: {result['reason']}")
        if result["ok"]:
            print(f"    expected output shape: {result['out_shape']}")

    a = [[1.0, 2.0], [3.0, 4.0]]
    b = [[5.0, 6.0], [7.0, 8.0]]
    guard = check_shapes(tensor_shape(a), tensor_shape(b))
    print(f"  guard  {tensor_shape(a)} @ {tensor_shape(b)} -> ok={guard['ok']}")
    assert guard["ok"] is True, "စစ်မှန်သည့် shape သည် အတည်ပြု ခံရမည်"
    product = matmul(a, b)
    print(f"  matmul {tensor_shape(a)} @ {tensor_shape(b)} = {product}")

    assert results[0][2]["ok"] is True, "first case သည် တိုက်ဆိုင်ရမည်"
    assert results[0][2]["out_shape"] == (4, 256), "output shape မှားနေသည်"
    assert results[1][2]["ok"] is False, "inner dimension mismatch ကို ဖမ်းရမည်"
    assert results[2][2]["ok"] is False, "1D shape ကို ငြင်းရမည်"
    assert product == [[19.0, 22.0], [43.0, 50.0]], "matmul ရလဒ် မှားနေသည်"

    print("[OK] exercise_3 — matmul shape များကို မြှောက်မီ စစ်ဆေးပြီးပါသည်")
    return {"results": results, "product": product}


# ---------------------------------------------------------------------------
# Exercise 4 — profile_hotspot
# ---------------------------------------------------------------------------
# ဖမ်းယူထားသည့် cProfile-style stats ဇယား နမူနာ —
# (function name with file:lineno, ncalls, tottime, cumtime)
# ဤတန်ဖိုးများသည် `python -m cProfile -s cumtime train.py` ၏ output ကို
# ကိုယ်စားပြုသည့် **နမူနာ fixture** ဖြစ်သည်။ စစ်မှန်သည့် တန်ဖိုးကို မိမိ run မှ ရယူရမည်။
PROFILE_STATS = [
    ("debug_tools.py:120(train_step)", 10000, 0.4210, 12.5000),
    ("~/site-packages/torch/nn/modules/module.py:1501(_call_impl)", 10000, 0.5120, 11.9000),
    ("debug_tools.py:88(load_batch)", 10000, 6.2100, 6.2400),
    ("~/site-packages/torch/nn/functional.py:2202(linear)", 10000, 0.8800, 1.1200),
    ("~/site-packages/torch/autograd/__init__.py:200(backward)", 10000, 0.0400, 0.9100),
    ("debug_tools.py:145(accuracy)", 10000, 0.2500, 0.2600),
    ("<built-in method builtins.sum>", 10000, 0.1900, 0.1900),
]

_CUMTIME = 3
_TOTTIME = 2
_NCALLS = 1


def is_own_code(name: str) -> bool:
    """Function သည် ဤ project ၏ code ဖြစ်/မဖြစ် ဆုံးဖြတ်သည် — library frame များကို ဖယ်သည်။"""
    excluded = ("~/site-packages", "site-packages", "<built-in", "<method")
    return not name.startswith(excluded)


def rank_functions(stats: list, key: str = "cumtime", limit: int | None = None) -> list:
    """cProfile-style ဇယားကို သတ်မှတ်သည့် column အလိုက် စီသည် (များမှ နည်းသို့)။"""
    column = {"ncalls": _NCALLS, "tottime": _TOTTIME, "cumtime": _CUMTIME}[key]
    ranked = sorted(stats, key=lambda row: row[column], reverse=True)
    return ranked[:limit] if limit is not None else ranked


def hottest_own_code(stats: list, key: str = "tottime") -> tuple:
    """Project ၏ code ထဲမှ သတ်မှတ်သည့် column အလိုက် အများဆုံး function ကို ရှာသည်။"""
    column = {"tottime": _TOTTIME, "cumtime": _CUMTIME}[key]
    own = [row for row in stats if is_own_code(row[0])]
    return max(own, key=lambda row: row[column])


def exercise_4() -> dict:
    print("Exercise 4 — profile_hotspot (cProfile-style stats မှ နှေးဆုံး function ကို ရှာခြင်း)")

    print("  top 5 by cumtime:")
    for name, ncalls, tottime, cumtime in rank_functions(PROFILE_STATS, "cumtime", 5):
        print(f"    {name}  ncalls={ncalls}  tottime={tottime:.4f}  cumtime={cumtime:.4f}")

    hotspot = hottest_own_code(PROFILE_STATS, "tottime")
    print(f"  own-code hotspot : {hotspot[0]}")
    print(f"    ncalls={hotspot[_NCALLS]}  tottime={hotspot[_TOTTIME]:.4f}  cumtime={hotspot[_CUMTIME]:.4f}")

    slowest_overall = rank_functions(PROFILE_STATS, "cumtime", 1)[0]
    total_cumtime = rank_functions(PROFILE_STATS, "cumtime", 1)[0][_CUMTIME]
    share = hotspot[_TOTTIME] / total_cumtime * 100.0
    print(f"  slowest overall  : {slowest_overall[0]}  cumtime={slowest_overall[_CUMTIME]:.4f}")
    print(f"  hotspot share    : {share:.1f}% of the slowest overall cumtime")

    assert rank_functions(PROFILE_STATS, "cumtime", 1)[0][0].endswith("(train_step)"), "cumtime အများဆုံးသည် train_step ဖြစ်ရမည်"
    assert hotspot[0].endswith("(load_batch)"), "own-code tottime အများဆုံးသည် load_batch ဖြစ်ရမည်"
    assert is_own_code(hotspot[0]) is True, "hotspot သည် project code ဖြစ်ရမည်"
    assert is_own_code("~/site-packages/torch/nn/modules/module.py:1501(_call_impl)") is False, "library frame ကို ဖယ်ရမည်"
    assert share > 40.0, "data loading သည် အချိန် ကြီးမားစွာ စားရမည်"

    print("[OK] exercise_4 — cProfile-style ဇယားမှ hotspot ကို ခွဲထုတ်ပြီးပါသည်")
    return {"hotspot": hotspot, "slowest_overall": slowest_overall, "share": share}


# ---------------------------------------------------------------------------
# Exercise 5 — memory_hotspot
# ---------------------------------------------------------------------------
# ဖမ်းယူထားသည့် tracemalloc-style snapshot နမူနာ — (location, size_bytes, count)
# ဤတန်ဖိုးများသည် `tracemalloc.take_snapshot().statistics("lineno")` ၏ output ကို
# ကိုယ်စားပြုသည့် **နမူနာ fixture** ဖြစ်သည်။
MEMORY_SNAPSHOT = [
    ("data_loader.py:120", 51200000, 20),
    ("data_loader.py:64", 12800000, 40),
    ("train.py:210", 4096000, 1),
    ("debug_tools.py:300", 1048576, 8),
    ("train.py:44", 262144, 32),
]


def format_size(nbytes: int) -> str:
    """Byte ကို လူဖတ်နိုင်သည့် MiB/KiB/B အဖြစ် ပြောင်းသည်။"""
    if nbytes >= 1024 ** 2:
        return f"{nbytes / (1024 ** 2):.1f} MiB"
    if nbytes >= 1024:
        return f"{nbytes / 1024:.1f} KiB"
    return f"{nbytes} B"


def memory_report(snapshot: list, limit: int = 3) -> list:
    """Snapshot ကို size အလိုက် စီ၍ tracemalloc-style လိုင်းများ ပြန်သည်။"""
    ranked = sorted(snapshot, key=lambda row: row[1], reverse=True)
    lines = []
    for location, size, count in ranked[:limit]:
        average = size // count if count else 0
        lines.append(
            f"  {location}: size={format_size(size)}, count={count}, "
            f"average={format_size(average)}"
        )
    return lines


def top_allocation(snapshot: list) -> tuple:
    """အများဆုံး allocate လုပ်သည့် နေရာကို ပြန်သည်။"""
    return max(snapshot, key=lambda row: row[1])


def exercise_5() -> dict:
    print("Exercise 5 — memory_hotspot (tracemalloc-style snapshot မှ အများဆုံး နေရာကို ရှာခြင်း)")

    for line in memory_report(MEMORY_SNAPSHOT, 3):
        print(line)

    location, size, count = top_allocation(MEMORY_SNAPSHOT)
    print(f"  top allocation   : {location} -> {format_size(size)} in {count} allocations")

    total = sum(row[1] for row in MEMORY_SNAPSHOT)
    print(f"  snapshot total   : {format_size(total)} over {len(MEMORY_SNAPSHOT)} sites")

    assert location == "data_loader.py:120", "အများဆုံး နေရာသည် data_loader.py:120 ဖြစ်ရမည်"
    assert size == 51200000, "အများဆုံး size မှားနေသည်"
    assert format_size(size) == "48.8 MiB", "format_size ရလဒ် မှားနေသည်"
    assert format_size(262144) == "256.0 KiB", "KiB format မှားနေသည်"
    assert len(memory_report(MEMORY_SNAPSHOT, 10)) == len(MEMORY_SNAPSHOT), "limit အားလုံးကို ပြရမည်"

    print("[OK] exercise_5 — tracemalloc-style snapshot မှ hotspot ကို ရှာပြီးပါသည်")
    return {"location": location, "size": size, "count": count, "total": total}


# ---------------------------------------------------------------------------
# Exercise 6 — training_health_report
# ---------------------------------------------------------------------------
# ဖမ်းယူထားသည့် loss curve ဇယား နမူနာများ — epoch၊ train loss နှင့် validation loss။
OVERFIT_HISTORY = [
    {"epoch": 1, "train_loss": 2.3026, "val_loss": 2.2900},
    {"epoch": 2, "train_loss": 1.8200, "val_loss": 1.7800},
    {"epoch": 3, "train_loss": 1.3100, "val_loss": 1.4200},
    {"epoch": 4, "train_loss": 1.0200, "val_loss": 1.5100},
    {"epoch": 5, "train_loss": 0.8100, "val_loss": 1.6400},
    {"epoch": 6, "train_loss": 0.6200, "val_loss": 1.7900},
    {"epoch": 7, "train_loss": 0.5100, "val_loss": 1.9200},
    {"epoch": 8, "train_loss": 0.4300, "val_loss": 2.1100},
]

HEALTHY_HISTORY = [
    {"epoch": 1, "train_loss": 2.3026, "val_loss": 2.3100},
    {"epoch": 2, "train_loss": 1.9100, "val_loss": 1.9500},
    {"epoch": 3, "train_loss": 1.4200, "val_loss": 1.4900},
    {"epoch": 4, "train_loss": 1.0100, "val_loss": 1.1200},
    {"epoch": 5, "train_loss": 0.7800, "val_loss": 0.8900},
]

UNSTABLE_HISTORY = [
    {"epoch": 1, "train_loss": 2.3026, "val_loss": 2.3100},
    {"epoch": 2, "train_loss": 1.6100, "val_loss": 1.7000},
    {"epoch": 3, "train_loss": float("nan"), "val_loss": float("nan")},
    {"epoch": 4, "train_loss": float("nan"), "val_loss": float("nan")},
]


def _is_nan(value) -> bool:
    return isinstance(value, float) and math.isnan(value)


def training_health_report(history: list) -> dict:
    """Loss curve မှ overfit / healthy / diverging / unstable ကို ဆုံးဖြတ်သည်။

    ဆုံးဖြတ်ချက် အစဉ် —
    ၁။ Loss တစ်ခုခုတွင် NaN ရှိပါက "numerical-instability" ဖြစ်သည်။
    ၂။ Train loss ကျနေစဉ် val loss သည် အကောင်းဆုံး တန်ဖိုးမှ တက်လာပါက "overfitting" ဖြစ်သည်။
    ၃။ နှစ်ခုလုံး တက်ပါက "diverging" ဖြစ်သည်။
    ၄။ နှစ်ခုလုံး ကျပါက "healthy-learning" ဖြစ်သည်။
    ၅။ ကျန် အခြေအနေများအတွက် "monitor" ဖြစ်သည်။
    """
    epochs = [row["epoch"] for row in history]
    train = [row["train_loss"] for row in history]
    val = [row["val_loss"] for row in history]

    unstable = any(_is_nan(v) for v in train + val)
    train_first, train_last = train[0], train[-1]
    val_first, val_last = val[0], val[-1]

    if unstable:
        bad_epochs = sorted({row["epoch"] for row in history if _is_nan(row["train_loss"]) or _is_nan(row["val_loss"])})
        return {
            "verdict": "numerical-instability",
            "reason": f"NaN loss ကို epoch {bad_epochs} တွင် တွေ့သည် — learning rate၊ log(0) သို့မဟုတ် သုညဖြင့် စားခြင်းကို စစ်ရမည်",
            "best_val_epoch": None,
            "best_val_loss": None,
            "epochs": epochs,
        }

    best_val_loss = min(val)
    best_val_epoch = epochs[val.index(best_val_loss)]

    if train_last < train_first and val_last > best_val_loss + 1e-12:
        verdict = "overfitting"
        reason = (
            f"train loss ကျနေစဉ် val loss သည် epoch {best_val_epoch} ၏ "
            f"{best_val_loss:.4f} မှ {val_last:.4f} သို့ တက်လာသည်"
        )
    elif train_last > train_first and val_last > val_first:
        verdict = "diverging"
        reason = f"train loss နှင့် val loss နှစ်ခုလုံး တက်နေသည် ({train_first:.4f} -> {train_last:.4f}) — learning rate မြင့်နိုင်သည်"
    elif train_last < train_first and val_last <= val_first:
        verdict = "healthy-learning"
        reason = f"train loss နှင့် val loss နှစ်ခုလုံး ကျနေသည် (val {val_first:.4f} -> {val_last:.4f})"
    else:
        verdict = "monitor"
        reason = f"လမ်းကြောင်း မရှင်းလင်း (train {train_first:.4f} -> {train_last:.4f}, val {val_first:.4f} -> {val_last:.4f})"

    return {
        "verdict": verdict,
        "reason": reason,
        "best_val_epoch": best_val_epoch,
        "best_val_loss": best_val_loss,
        "epochs": epochs,
    }


def exercise_6() -> dict:
    print("Exercise 6 — training_health_report (loss curve မှ overfit ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း)")

    reports = {}
    for label, history in (
        ("overfit run", OVERFIT_HISTORY),
        ("healthy run", HEALTHY_HISTORY),
        ("unstable run", UNSTABLE_HISTORY),
    ):
        report = training_health_report(history)
        reports[label] = report
        print(f"  {label}:")
        for row in history:
            train_text = "nan" if _is_nan(row["train_loss"]) else f"{row['train_loss']:.4f}"
            val_text = "nan" if _is_nan(row["val_loss"]) else f"{row['val_loss']:.4f}"
            print(f"    epoch {row['epoch']}: train_loss={train_text}, val_loss={val_text}")
        if report["best_val_epoch"] is not None:
            print(f"    best val loss: {report['best_val_loss']:.4f} at epoch {report['best_val_epoch']}")
        print(f"    verdict: {report['verdict']}")
        print(f"    reason : {report['reason']}")

    assert reports["overfit run"]["verdict"] == "overfitting", "overfit table ကို ဖမ်းရမည်"
    assert reports["overfit run"]["best_val_epoch"] == 3, "best val epoch မှားနေသည်"
    assert reports["healthy run"]["verdict"] == "healthy-learning", "healthy table ကို မှန်ကန်စွာ ဆုံးဖြတ်ရမည်"
    assert reports["unstable run"]["verdict"] == "numerical-instability", "NaN တွင် instability ဟု ဆုံးဖြတ်ရမည်"

    print("[OK] exercise_6 — loss curve မှ overfit ကို ဆုံးဖြတ်ပြီးပါသည်")
    return reports


# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 70)
    print("Module 12 — Debugging & Profiling — offline lab")
    print("=" * 70)
    exercise_1()
    print()
    exercise_2()
    print()
    exercise_3()
    print()
    exercise_4()
    print()
    exercise_5()
    print()
    exercise_6()
    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
