#!/usr/bin/env python3
"""Module 03 — GPU Setup & Cloud: offline lab.

ဤ lab သည် GPU မရှိသော machine တွင် run နိုင်ရန် ရေးထားသည့် **simulation** ဖြစ်သည်။
nvidia-smi output ကို ဖမ်းယူထားသည့် နမူနာ ဇယားမှ parse လုပ်ခြင်း၊ fp16 rule of thumb
ဖြင့် model အရွယ်အစား တွက်ခြင်း၊ pure Python matmul ကို အချိန်တိုင်းခြင်း၊ CPU/GPU
speedup လိုင်း ဖော်မတ်ချခြင်း နှင့် local/cloud route ဆုံးဖြတ်ခြင်း တို့ကို ပြသည်။

သုံးသည့် library သည် Python standard library သာ ဖြစ်သည်။ network၊ torch၊ GPU မလိုပါ။
ရလဒ်သည် deterministic ဖြစ်သည် (random မသုံးပါ)။
"""

from __future__ import annotations

import re
import time

# ---------------------------------------------------------------------------
# ဖမ်းယူထားသည့် nvidia-smi ဇယား နမူနာ (simulation fixture)
# ---------------------------------------------------------------------------
# ဤစာသားသည် **လက်တွေ့ machine တွင် run ရမည့် နေရာ** ကို ကိုယ်စားပြုသည့် နမူနာ ဖြစ်သည်။
# တန်ဖိုး အားလုံးသည် ဤ lab ၏ နမူနာ ဖြစ်သည် — မိမိ machine ၏ အမှန်တန်ဖိုးကို
# `nvidia-smi` ကို ကိုယ်တိုင် run ၍ ရယူရမည်။ Version များ အလိုက် ပြောင်းလဲနိုင်သည်။
SAMPLE_NVIDIA_SMI = """\
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.54.14              Driver Version: 550.54.14      CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4090        WDDM  |   00000000:01:00.0  On |                  Off |
| 30%   45C    P8             30W / 450W   |     1234MiB /  24564MiB |      5%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
"""

# source တွင် "keep a margin" ဟု ဆိုထားသည် (အရေအတွက် အတိအကျ မပေးပါ)။
# ဤ lab သည် ရှင်းလင်းစေရန် ၁၀ ရာခိုင်နှုန်းကို နမူနာ margin အဖြစ် သုံးသည်။
LAB_RESERVED_FRACTION = 0.10

MIB_IN_BYTES = 1024 * 1024


# ---------------------------------------------------------------------------
# Exercise 1 — parse_nvidia_smi
# ---------------------------------------------------------------------------
def parse_nvidia_smi(text: str) -> dict:
    """nvidia-smi ဇယား output မှ driver version၊ GPU အမည် နှင့် memory ကို ဖတ်သည်။"""
    driver = None
    match = re.search(r"Driver Version:\s*([0-9][0-9.]*)", text)
    if match:
        driver = match.group(1)

    name = None
    match = re.search(r"^\|\s+(\d+)\s+(.+?)\s{2,}\S", text, re.MULTILINE)
    if match:
        name = match.group(2).strip()

    used_mib = None
    total_mib = None
    match = re.search(r"(\d+)MiB\s*/\s*(\d+)MiB", text)
    if match:
        used_mib = int(match.group(1))
        total_mib = int(match.group(2))

    free_mib = None
    if used_mib is not None and total_mib is not None:
        free_mib = total_mib - used_mib

    return {
        "driver_version": driver,
        "gpu_name": name,
        "used_mib": used_mib,
        "total_mib": total_mib,
        "free_mib": free_mib,
        "total_bytes": (total_mib * MIB_IN_BYTES) if total_mib is not None else None,
        "free_bytes": (free_mib * MIB_IN_BYTES) if free_mib is not None else None,
    }


def exercise_1() -> dict:
    print("Exercise 1 — parse_nvidia_smi (nvidia-smi ဇယားမှ device အချက်အလက် ဖတ်ခြင်း)")
    device = parse_nvidia_smi(SAMPLE_NVIDIA_SMI)
    print(f"  driver version : {device['driver_version']}")
    print(f"  gpu name       : {device['gpu_name']}")
    print(f"  memory used    : {device['used_mib']} MiB / {device['total_mib']} MiB")
    print(f"  memory free    : {device['free_mib']} MiB")
    print(f"  total bytes    : {device['total_bytes']}")

    assert device["driver_version"] is not None, "driver version မဖတ်နိုင်ပါ"
    assert device["gpu_name"] is not None, "GPU အမည် မဖတ်နိုင်ပါ"
    assert device["gpu_name"].startswith("NVIDIA"), "GPU အမည် format မမှန်ပါ"
    assert device["total_mib"] == 24564, "total memory မှားနေသည်"
    assert device["free_mib"] == device["total_mib"] - device["used_mib"], "free memory တွက် မှားနေသည်"

    print("[OK] exercise_1 — nvidia-smi ဇယားမှ device အချက်အလက် ဖတ်ပြီးပါသည်")
    return device


# ---------------------------------------------------------------------------
# Exercise 2 — fp16_model_fit
# ---------------------------------------------------------------------------
def fp16_model_fit(free_bytes: int) -> dict:
    """parameter တစ်ခုလျှင် ၂ byte ဆိုသည့် rule of thumb ဖြင့် fit ကို တွက်သည်။"""
    params_at_2_bytes = free_bytes / 2
    lab_budget_bytes = int(free_bytes * (1.0 - LAB_RESERVED_FRACTION))
    params_with_margin = lab_budget_bytes / 2
    return {
        "free_bytes": free_bytes,
        "params_at_2_bytes": params_at_2_bytes,
        "params_billions": params_at_2_bytes / 1e9,
        "lab_budget_bytes": lab_budget_bytes,
        "params_with_margin_billions": params_with_margin / 1e9,
        "bytes_per_parameter": 2,
    }


def exercise_2() -> dict:
    print("Exercise 2 — fp16_model_fit (fp16 rule of thumb ဖြင့် model အရွယ်အစား တွက်ခြင်း)")
    device = parse_nvidia_smi(SAMPLE_NVIDIA_SMI)
    fit = fp16_model_fit(device["free_bytes"])
    print(f"  free VRAM            : {fit['free_bytes']} bytes")
    print(f"  bytes per parameter  : {fit['bytes_per_parameter']} (fp16)")
    print(f"  est. max params      : {fit['params_billions']:.2f}B parameters")
    print(f"  lab margin ({int(LAB_RESERVED_FRACTION * 100)}%)     : {fit['params_with_margin_billions']:.2f}B parameters")

    assert fit["bytes_per_parameter"] == 2, "fp16 သည် parameter တစ်ခုလျှင် ၂ byte ဖြစ်သည်"
    assert fit["params_at_2_bytes"] == device["free_bytes"] / 2, "params တွက်ချက်မှု မှားနေသည်"
    assert 10.0 < fit["params_billions"] < 14.0, "fit ခန့်မှန်းချက် သည် 24GB class အတွက် မမှန်ပါ"
    assert fit["params_with_margin_billions"] < fit["params_billions"], "margin လျှော့ပြီးနောက် အရေအတွက် နည်းရမည်"

    print("[OK] exercise_2 — fp16 fit ခန့်မှန်းချက် တွက်ချက်ပြီးပါသည်")
    return fit


# ---------------------------------------------------------------------------
# Exercise 3 — benchmark_matmul
# ---------------------------------------------------------------------------
def make_matrix(size: int) -> list:
    """Deterministic matrix တစ်ခု တည်ဆောက်သည် (random မသုံးပါ)။"""
    return [[((i * 7 + j * 13) % 17) - 8 for j in range(size)] for i in range(size)]


def matmul_naive(a: list, b: list) -> list:
    """မူလ (naive) matrix multiply — i, p, j အစဉ်အတိုင်း။"""
    n = len(a)
    k = len(b)
    m = len(b[0])
    out = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        ai = a[i]
        oi = out[i]
        for p in range(k):
            av = ai[p]
            if av == 0:
                continue
            bp = b[p]
            for j in range(m):
                oi[j] += av * bp[j]
    return out


def matmul_transposed(a: list, b: list) -> list:
    """ဒုတိယ လွတ်လပ်သည့် နည်းလမ်း — b ကို transpose ၍ dot product ဖြင့် တွက်သည်။"""
    bt = list(zip(*b))
    return [[sum(av * bv for av, bv in zip(row, col)) for col in bt] for row in a]


def benchmark_matmul(size: int = 64) -> dict:
    """သတ်မှတ်ထားသည့် workload အတွက် pure Python matmul ကို အချိန်တိုင်းသည်။"""
    a = make_matrix(size)
    b = make_matrix(size)
    start = time.perf_counter()
    c = matmul_naive(a, b)
    seconds = time.perf_counter() - start
    checksum = sum(sum(row) for row in c)
    reference = matmul_transposed(a, b)
    return {
        "size": size,
        "shape": (len(c), len(c[0])),
        "checksum": checksum,
        "seconds": seconds,
        "matches_reference": c == reference,
        "multiplies": size ** 3,
    }


def exercise_3() -> dict:
    print("Exercise 3 — benchmark_matmul (pure Python matmul ကို အချိန်တိုင်းခြင်း)")
    result = benchmark_matmul(64)
    print(f"  workload        : {result['size']}x{result['size']} @ {result['size']}x{result['size']}")
    print(f"  output shape    : {result['shape'][0]}x{result['shape'][1]}")
    print(f"  checksum        : {result['checksum']}")
    print(f"  multiply ops    : {result['multiplies']}")
    print("  elapsed seconds : တိုင်းတာပြီးပါသည် — စက် အလိုက် ကွာခြားသဖြင့် ဤနေရာတွင် ဂဏန်းအဖြစ် မပြပါ")

    assert result["matches_reference"] is True, "နည်းလမ်း နှစ်ခု၏ ရလဒ် မတူပါ"
    assert result["shape"] == (64, 64), "output shape မှားနေသည်"
    assert result["seconds"] > 0, "အချိန်တိုင်းတာမှု မမှန်ပါ"
    assert isinstance(result["checksum"], int), "checksum သည် integer ဖြစ်ရမည်"

    print("[OK] exercise_3 — matmul အချိန်တိုင်းတာပြီး နည်းလမ်း နှစ်ခု တိုက်ဆိုင်စစ်ပြီးပါသည်")
    return result


# ---------------------------------------------------------------------------
# Exercise 4 — speedup_line
# ---------------------------------------------------------------------------
def speedup_line(cpu_time: float, gpu_time: float) -> dict:
    """CPU နှင့် GPU အချိန်မှ speedup ကို တွက်ပြီး source format အတိုင်း ဖော်မတ်ချသည်။"""
    speedup = cpu_time / gpu_time
    line = (
        f"CPU matrix multiply: {cpu_time:.3f}s\n"
        f"GPU matrix multiply: {gpu_time:.3f}s\n"
        f"Speedup: {speedup:.0f}x"
    )
    return {"cpu_time": cpu_time, "gpu_time": gpu_time, "speedup": speedup, "line": line}


def exercise_4() -> dict:
    print("Exercise 4 — speedup_line (supplied timings မှ speedup လိုင်း ဖော်မတ်ချခြင်း)")
    result = speedup_line(cpu_time=8.312, gpu_time=0.041)
    for row in result["line"].splitlines():
        print(f"  {row}")
    print(f"  speedup value   : {result['speedup']:.4f}")

    assert result["speedup"] == 8.312 / 0.041, "speedup တွက်ချက်မှု မှားနေသည်"
    assert result["line"].endswith("x"), "speedup လိုင်းသည် 'x' ဖြင့် ဆုံးရမည်"
    assert "Speedup: 203x" in result["line"], "format မမှန်ပါ"

    print("[OK] exercise_4 — CPU/GPU speedup လိုင်း ဖော်မတ်ချပြီးပါသည်")
    return result


# ---------------------------------------------------------------------------
# Exercise 5 — cloud_decision
# ---------------------------------------------------------------------------
def cloud_decision(has_local_gpu: bool, vram_gb: float, required_vram_gb: float) -> dict:
    """Local GPU ရှိ/မရှိ နှင့် VRAM ပမာဏအလိုက် local သို့မဟုတ် cloud route ကို ဆုံးဖြတ်သည်။"""
    if not has_local_gpu:
        route = "cloud"
        reason = "local NVIDIA GPU မရှိပါ — Google Colab (အခမဲ့ T4) သို့မဟုတ် cloud GPU ကို သုံးရမည်"
    elif vram_gb >= required_vram_gb:
        route = "local"
        reason = (
            f"local VRAM {vram_gb:.0f} GB သည် လိုအပ်သည့် {required_vram_gb:.0f} GB ကို "
            "ဖုံးလွှမ်းနိုင်သည်"
        )
    else:
        route = "cloud"
        reason = (
            f"local VRAM {vram_gb:.0f} GB သည် လိုအပ်သည့် {required_vram_gb:.0f} GB အတွက် "
            "မလုံလောက်ပါ — model သည် VRAM ထဲ မဝင်နိုင်ပါ"
        )
    return {
        "route": route,
        "reason": reason,
        "has_local_gpu": has_local_gpu,
        "vram_gb": vram_gb,
        "required_vram_gb": required_vram_gb,
    }


def exercise_5() -> list:
    print("Exercise 5 — cloud_decision (availability အချက်အလက်မှ route ဆုံးဖြတ်ခြင်း)")
    cases = [
        (False, 0.0, 12.0),
        (True, 24.0, 12.0),
        (True, 8.0, 12.0),
    ]
    decisions = []
    for has_gpu, vram, required in cases:
        decision = cloud_decision(has_gpu, vram, required)
        decisions.append(decision)
        print(f"  local_gpu={has_gpu}, vram={vram:.0f}GB, required={required:.0f}GB -> {decision['route']}")
        print(f"    reason: {decision['reason']}")

    assert decisions[0]["route"] == "cloud", "GPU မရှိပါက cloud ဖြစ်ရမည်"
    assert decisions[1]["route"] == "local", "VRAM လုံလောက်ပါက local ဖြစ်ရမည်"
    assert decisions[2]["route"] == "cloud", "VRAM မလုံလောက်ပါက cloud ဖြစ်ရမည်"
    assert len({d["route"] for d in decisions}) == 2, "route နှစ်မျိုး လိုအပ်သည်"

    print("[OK] exercise_5 — local/cloud route ဆုံးဖြတ်ပြီးပါသည်")
    return decisions


# ---------------------------------------------------------------------------
# Exercise 6 — gpu_report
# ---------------------------------------------------------------------------
def gpu_report(device: dict, fit: dict, decision: dict, bench: dict) -> str:
    """device အချက်အလက်၊ fit ခန့်မှန်းချက် နှင့် အကြံပြုချက် စုစည်းချက်။"""
    lines = [
        "=== GPU Report ===",
        f"device            : {device['gpu_name']}",
        f"driver version    : {device['driver_version']}",
        f"vram total/free   : {device['total_mib']} MiB / {device['free_mib']} MiB",
        f"fp16 max params   : ~{fit['params_billions']:.2f}B parameters",
        f"with lab margin   : ~{fit['params_with_margin_billions']:.2f}B parameters",
        f"cpu matmul {bench['size']}x{bench['size']}  : shape {bench['shape'][0]}x{bench['shape'][1]}, checksum {bench['checksum']}",
        f"route             : {decision['route']}",
        f"recommendation    : {decision['reason']}",
    ]
    if decision["route"] == "local":
        lines.append("next step         : pip install torch torchvision torchaudio (CUDA build) ကို run ပါ")
    else:
        lines.append("next step         : Google Colab တွင် Runtime > Change runtime type > T4 GPU ကို ရွေးပါ")
    return "\n".join(lines)


def exercise_6(device=None, fit=None, decision=None, bench=None) -> str:
    print("Exercise 6 — gpu_report (စစ်ဆေးချက် အားလုံး၏ အစီရင်ခံစာ)")
    device = device or parse_nvidia_smi(SAMPLE_NVIDIA_SMI)
    fit = fit or fp16_model_fit(device["free_bytes"])
    decision = decision or cloud_decision(True, device["total_bytes"] / 1e9, 12.0)
    bench = bench or benchmark_matmul(32)
    report = gpu_report(device, fit, decision, bench)
    for row in report.splitlines():
        print(f"  {row}")

    assert "=== GPU Report ===" in report, "report header မပါပါ"
    assert device["gpu_name"] in report, "GPU အမည် report တွင် မပါပါ"
    assert "route" in report, "route မပါပါ"
    assert report.count("\n") >= 8, "report သည် လိုင်း အနည်းဆုံး ၉ လိုင်း ရှိရမည်"

    print("[OK] exercise_6 — GPU အစီရင်ခံစာ ထုတ်ပြီးပါသည်")
    return report


# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 70)
    print("Module 03 — GPU Setup & Cloud — offline lab (simulation)")
    print("=" * 70)
    device = exercise_1()
    print()
    fit = exercise_2()
    print()
    bench = exercise_3()
    print()
    exercise_4()
    print()
    decisions = exercise_5()
    print()
    exercise_6(device, fit, decisions[1], bench)
    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
