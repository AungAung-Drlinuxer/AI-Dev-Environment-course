#!/usr/bin/env python3
"""Module 07 — Docker for AI ၏ lab။

ဤ lab သည် Dockerfile၊ base image၊ `docker run` command line နှင့် Docker Compose
service တို့ကို **offline** ဖြင့် parse လုပ်ပြီး စစ်ဆေးသည်။

စည်းမျဉ်း —
  * Python standard library သာ အသုံးပြုသည်။
  * Docker daemon၊ network၊ GPU နှင့် တတိယပါတီ package မလိုပါ။
  * deterministic ဖြစ်သည် — အထွက်သည် run တိုင်း တူညီသည်။

Run:
    python3 modules/07_docker_for_ai/lab.py
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# ဤ lab သည် Docker ကို ကိုယ်တိုင် run မလုပ်ပါ။ သင်ခန်းစာတွင် ဖော်ပြထားသည့်
# Dockerfile နှင့် compose ဖိုင်၏ အကြောင်းအရာကို ကွက်တိ တူညီစွာ ဤနေရာတွင်
# ထည့်သွင်းထားပြီး parse လုပ်သည်။ သို့ဖြစ်၍ network မလိုဘဲ ရလဒ်သည် ခိုင်မာသည်။
# ---------------------------------------------------------------------------

DOCKERFILE_TEXT = """FROM --platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \\
    software-properties-common \\
    git \\
    curl \\
    build-essential \\
    && add-apt-repository -y ppa:deadsnakes/ppa \\
    && apt-get update && apt-get install -y --no-install-recommends \\
    python3.12 \\
    python3.12-venv \\
    python3.12-dev \\
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

RUN curl -sSL https://raw.githubusercontent.com/pypa/get-pip/3b73145063be545b649ad9ca83ea8da5fc915a4f/public/get-pip.py -o /tmp/get-pip.py \\
    && echo "a341e1a43e38001c551a1508a73ff23636a11970b61d901d9a1cad2a18f57055  /tmp/get-pip.py" | sha256sum -c - \\
    && python /tmp/get-pip.py \\
    && rm /tmp/get-pip.py \\
    && update-alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.12 1

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel

RUN python -m pip install --no-cache-dir \\
    torch==2.6.0+cu124 \\
    torchvision==0.21.0+cu124 \\
    torchaudio==2.6.0+cu124 \\
    --index-url https://download.pytorch.org/whl/cu124

RUN python -m pip install --no-cache-dir \\
    numpy \\
    pandas \\
    scikit-learn \\
    matplotlib \\
    jupyter \\
    transformers \\
    datasets \\
    accelerate \\
    safetensors

WORKDIR /workspace

VOLUME ["/workspace", "/models"]

EXPOSE 8888

CMD ["python"]
"""

# သင်ခန်းစာ (source) ၏ code/docker-compose.yml — service နှစ်ခု၊ depends_on မပါ။
LESSON_COMPOSE_TEXT = """services:
  ai-dev:
    build:
      context: .
      dockerfile: Dockerfile
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ../../../:/workspace
      - ~/models:/models
      - ~/datasets:/data
    ports:
      - "8888:8888"
    stdin_open: true
    tty: true
    command: jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

  qdrant:
    image: qdrant/qdrant:v1.12.5
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  qdrant_data:
"""

# ဤ repository ရှိ docker-compose.yml — depends_on နှင့် QDRANT_URL ပါသည်။
REPO_COMPOSE_TEXT = """services:
  qdrant:
    image: qdrant/qdrant:latest
    container_name: aidev-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_storage:/qdrant/storage
    healthcheck:
      test: ["CMD-SHELL", "bash -c ':> /dev/tcp/127.0.0.1/6333' || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  ai-dev:
    build:
      context: .
      dockerfile: modules/07_docker_for_ai/Dockerfile.example
    container_name: aidev-app
    working_dir: /workspace
    volumes:
      - ./:/workspace
      - aidev_cache:/root/.cache
    environment:
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      qdrant:
        condition: service_healthy
    command: ["python", "-c", "print('ai-dev container ready')"]

volumes:
  qdrant_storage:
  aidev_cache:
"""

# Source မှ ဖော်ပြထားသည့် base image အရွယ်အစား ဇယား (MB ဖြင့်)။
BASE_IMAGES = [
    {
        "image": "nvidia/cuda:12.4.1-devel-ubuntu22.04",
        "role": "အပြည့်အစုံ CUDA toolkit၊ compiler ပါသည်",
        "use_for": "nvcc လိုအပ်သည့် package များ (flash-attn, bitsandbytes) build လုပ်ရန်",
        "size_mb": 4096,
        "size_label": "~4 GB",
        "compilers": True,
    },
    {
        "image": "nvidia/cuda:12.4.1-runtime-ubuntu22.04",
        "role": "CUDA runtime သာ၊ compiler မပါ",
        "use_for": "build ပြီးသား code ကို run ရန်",
        "size_mb": 1536,
        "size_label": "~1.5 GB",
        "compilers": False,
    },
    {
        "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime",
        "role": "CUDA အပေါ် PyTorch တင်ပြီးသား",
        "use_for": "PyTorch install အဆင့်ကို ကျော်ရန်",
        "size_mb": 6144,
        "size_label": "~6 GB",
        "compilers": False,
    },
    {
        "image": "python:3.12-slim",
        "role": "CUDA မပါ၊ CPU သာ",
        "use_for": "CPU inference နှင့် အလေးချိန်နည်း tool များ",
        "size_mb": 150,
        "size_label": "~150 MB",
        "compilers": False,
    },
]

# Exercise 3 အတွက် run spec။
RUN_SPEC = {
    "image": "ai-dev",
    "gpus": "all",
    "interactive": True,
    "rm": True,
    "volumes": [
        {"host": "$(pwd)", "container": "/workspace"},
        {"host": "~/models", "container": "/models"},
        {"host": "~/datasets", "container": "/data"},
    ],
    "ports": [{"host": 8888, "container": 8888}],
    "command": 'python -c "import torch; print(torch.__version__)"',
}


# ===========================================================================
# Dockerfile parser
# ===========================================================================

def logical_lines(text):
    """Line continuation (`\\`) ကို ပေါင်းပြီး comment နှင့် လိုင်းလွတ် ကို ဖယ်သည်။"""
    out = []
    buffer = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.endswith("\\"):
            buffer += line[:-1] + " "
            continue
        buffer += line
        out.append(buffer.strip())
        buffer = ""
    if buffer.strip():
        out.append(buffer.strip())
    return out


def parse_dockerfile(text):
    """Dockerfile ကို (INSTRUCTION, arguments) tuple စာရင်း အဖြစ် ပြန်သည်။"""
    parsed = []
    for logical in logical_lines(text):
        match = re.match(r"^([A-Za-z]+)\s*(.*)$", logical)
        if not match:
            continue
        parsed.append((match.group(1).upper(), match.group(2).strip()))
    return parsed


def extract_base_image(instructions):
    """FROM ၏ argument မှ platform flag ကို ချန်ပြီး base image အမည်ကို ထုတ်သည်။"""
    for name, args in instructions:
        if name != "FROM":
            continue
        for token in args.split():
            if token.startswith("--"):
                continue
            if token.upper() == "AS":
                break
            return token
    return ""


def extract_platform(instructions):
    for name, args in instructions:
        if name != "FROM":
            continue
        for token in args.split():
            if token.startswith("--platform="):
                return token.split("=", 1)[1]
    return ""


def count_layers(instructions):
    """FROM နောက်ပိုင်း instruction တိုင်းသည် layer တစ်ခု ဖန်တီးသည်။"""
    seen_from = False
    layers = 0
    for name, _args in instructions:
        if name == "FROM":
            seen_from = True
            continue
        if seen_from:
            layers += 1
    return layers


def find_instruction(instructions, name):
    for instr, args in instructions:
        if instr == name:
            return args
    return None


def find_all(instructions, name):
    return [args for instr, args in instructions if instr == name]


# ===========================================================================
# `docker run` command builder
# ===========================================================================

def build_docker_run(spec):
    parts = ["docker"]
    if spec.get("rm"):
        parts.append("run")
        parts.append("--rm")
    else:
        parts.append("run")
    if spec.get("interactive"):
        parts.append("-it")
    if spec.get("gpus"):
        parts.extend(["--gpus", spec["gpus"]])
    for mount in spec.get("volumes", []):
        parts.extend(["-v", "%s:%s" % (mount["host"], mount["container"])])
    for port in spec.get("ports", []):
        parts.extend(["-p", "%d:%d" % (port["host"], port["container"])])
    parts.append(spec["image"])
    if spec.get("command"):
        parts.append(spec["command"])
    return " ".join(parts)


# ===========================================================================
# Compose parser (YAML subset)
# ===========================================================================

MAP_KEY = re.compile(r"^([A-Za-z0-9_.\-]+):(?:\s+(.*))?$")


def _split_flow(inner):
    parts, buffer, quote = [], "", None
    for ch in inner:
        if quote:
            buffer += ch
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
            buffer += ch
        elif ch == ",":
            parts.append(buffer)
            buffer = ""
        else:
            buffer += ch
    if buffer.strip():
        parts.append(buffer)
    return parts


def _scalar(text):
    text = text.strip()
    if not text:
        return None
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_scalar(part) for part in _split_flow(inner)] if inner else []
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        return text[1:-1]
    low = text.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "~"):
        return None
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return text


def parse_yaml(text):
    """compose ဖိုင်အတွက် လိုအပ်သည့် YAML အစိတ်အပိုင်းကို ဖတ်သည့် parser။"""
    entries = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        entries.append((indent, raw.strip()))
    if not entries:
        return {}
    pos = 0

    def parse_block(indent):
        nonlocal pos
        if entries[pos][1].startswith("- "):
            items = []
            while pos < len(entries) and entries[pos][0] == indent and entries[pos][1].startswith("- "):
                content = entries[pos][1][2:].strip()
                pos += 1
                match = MAP_KEY.match(content)
                if match:
                    item = {}
                    key = match.group(1)
                    value = (match.group(2) or "").strip()
                    if value:
                        item[key] = _scalar(value)
                    elif pos < len(entries) and entries[pos][0] > indent:
                        item[key] = parse_block(entries[pos][0])
                    else:
                        item[key] = None
                    if pos < len(entries) and entries[pos][0] > indent:
                        sub = parse_block(entries[pos][0])
                        if isinstance(sub, dict):
                            item.update(sub)
                    items.append(item)
                else:
                    items.append(_scalar(content))
            return items

        mapping = {}
        while pos < len(entries) and entries[pos][0] == indent and not entries[pos][1].startswith("- "):
            match = MAP_KEY.match(entries[pos][1])
            if not match:
                pos += 1
                continue
            key = match.group(1)
            value = (match.group(2) or "").strip()
            pos += 1
            if value:
                mapping[key] = _scalar(value)
            elif pos < len(entries) and entries[pos][0] > indent:
                mapping[key] = parse_block(entries[pos][0])
            else:
                mapping[key] = None
        return mapping

    return parse_block(entries[0][0])


def service_env(service):
    env = service.get("environment") or []
    result = {}
    if isinstance(env, dict):
        return dict(env)
    for item in env:
        if isinstance(item, str) and "=" in item:
            key, _, value = item.partition("=")
            result[key] = value
    return result


def depends_on_names(service):
    dep = service.get("depends_on")
    if dep is None:
        return []
    if isinstance(dep, dict):
        return list(dep.keys())
    if isinstance(dep, list):
        return [str(item) for item in dep]
    return [str(dep)]


def startup_order(services):
    """depends_on ကို လိုက်နာသည့် အနိမ့်ဆုံး အစဉ်လိုက် စာရင်း။"""
    remaining = dict((name, depends_on_names(body)) for name, body in services.items())
    order = []
    while remaining:
        ready = sorted(name for name, deps in remaining.items() if not deps)
        if not ready:
            order.extend(sorted(remaining))
            break
        for name in ready:
            order.append(name)
            remaining.pop(name)
        for name in remaining:
            remaining[name] = [d for d in remaining[name] if d not in order]
    return order


def container_ports(service):
    """ports mapping စာရင်းမှ container port များကို ထုတ်သည်။"""
    result = []
    for entry in service.get("ports") or []:
        text = str(entry)
        if ":" in text:
            host, _, container = text.rpartition(":")
            result.append(int(container))
        else:
            result.append(int(text))
    return result


# ===========================================================================
# Exercise 1 — parse_dockerfile
# ===========================================================================

def exercise_1():
    print("=" * 72)
    print("Exercise 1 — Dockerfile ကို instruction နှင့် layer အဖြစ် parse လုပ်ခြင်း")
    print("=" * 72)
    instructions = parse_dockerfile(DOCKERFILE_TEXT)
    print("instruction စုစုပေါင်း : %d" % len(instructions))
    for index, (name, args) in enumerate(instructions, start=1):
        shown = args if len(args) <= 58 else args[:55] + "..."
        print("  [%2d] %-8s %s" % (index, name, shown))

    base = extract_base_image(instructions)
    platform = extract_platform(instructions)
    layers = count_layers(instructions)
    runs = len(find_all(instructions, "RUN"))
    print("")
    print("base image          : %s" % base)
    print("platform            : %s" % platform)
    print("RUN instruction     : %d ခု" % runs)
    print("layer အရေအတွက်      : %d ခု (FROM နောက်ပိုင်း instruction တိုင်း layer တစ်ခု)" % layers)

    assert base == "nvidia/cuda:12.4.1-devel-ubuntu22.04", base
    assert platform == "linux/amd64", platform
    assert len(instructions) == 13, len(instructions)
    assert layers == 12, layers
    assert runs == 6, runs
    assert find_instruction(instructions, "EXPOSE") == "8888"
    assert find_instruction(instructions, "WORKDIR") == "/workspace"
    print("")
    print("[OK] exercise_1 — instruction ၁၃ ခု၊ layer ၁၂ ခု နှင့် base image ကို parse လုပ်ပြီးပါသည်")


# ===========================================================================
# Exercise 2 — devel_vs_runtime
# ===========================================================================

def exercise_2():
    print("=" * 72)
    print("Exercise 2 — base image ရွေးချယ်မှု — devel နှင့် runtime နှိုင်းယှဉ်ချက်")
    print("=" * 72)
    header = "%-46s %-10s %-12s" % ("image", "size", "compiler")
    print(header)
    print("-" * len(header))
    for entry in BASE_IMAGES:
        print("%-46s %-10s %-12s" % (
            entry["image"], entry["size_label"], "ပါသည်" if entry["compilers"] else "မပါ"
        ))
    print("")
    for entry in BASE_IMAGES:
        print("  %s" % entry["image"])
        print("    အခန်းကဏ္ဍ : %s" % entry["role"])
        print("    အသုံးပြုရန် : %s" % entry["use_for"])

    devel = BASE_IMAGES[0]
    runtime = BASE_IMAGES[1]
    delta_mb = devel["size_mb"] - runtime["size_mb"]
    delta_gb = delta_mb / 1024.0
    print("")
    print("devel (%s) မှ runtime (%s) သို့ ပြောင်းလျှင်" % (devel["size_label"], runtime["size_label"]))
    print("  လျော့နည်းသည့် ပမာဏ : %d MB (%.1f GB ခန့်)" % (delta_mb, delta_gb))
    print("  ဆုံးရှုံးသည့် အရာ  : nvcc compiler နှင့် CUDA header များ (build အဆင့်တွင်သာ လိုသည်)")
    print("  သတိပြုရန်       : အရွယ်အစားသည် သင်ခန်းစာတွင် ဖော်ပြထားသည့် ခန့်မှန်းတန်ဖိုး ဖြစ်သည်၊")
    print("                    မိမိ image ၏ တိကျသည့် အရွယ်ကို `docker images` ဖြင့် တိုင်းရမည်။")

    assert devel["compilers"] is True
    assert runtime["compilers"] is False
    assert delta_mb == 2560
    assert round(delta_gb, 1) == 2.5
    assert [e["image"] for e in BASE_IMAGES][2] == "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime"
    print("")
    print("[OK] exercise_2 — base image ၄ မျိုး၏ အရွယ်အစားနှင့် tooling ကွာခြားချက်ကို ဇယားဖြင့် ပြပြီးပါသည်")


# ===========================================================================
# Exercise 3 — docker_run_command
# ===========================================================================

def exercise_3():
    print("=" * 72)
    print("Exercise 3 — spec မှ `docker run` command line တည်ဆောက်ခြင်း")
    print("=" * 72)
    spec = dict(RUN_SPEC)
    print("spec —")
    print("  image         : %s" % spec["image"])
    print("  gpus          : %s" % spec["gpus"])
    print("  volumes       : %s" % ", ".join("%s:%s" % (v["host"], v["container"]) for v in spec["volumes"]))
    print("  ports         : %s" % ", ".join("%d:%d" % (p["host"], p["container"]) for p in spec["ports"]))
    print("  command       : %s" % spec["command"])
    command = build_docker_run(spec)
    print("")
    print("တည်ဆောက်သည့် command —")
    print("  %s" % command)

    expected = (
        'docker run --rm -it --gpus all -v $(pwd):/workspace -v ~/models:/models '
        '-v ~/datasets:/data -p 8888:8888 ai-dev python -c "import torch; print(torch.__version__)"'
    )
    assert command == expected, command
    print("")
    print("flag တစ်ခုချင်း၏ လုပ်ဆောင်ချက် —")
    print("  --rm                 : container ရပ်သည့်အခါ ဖျက်ပစ်သည်")
    print("  -it                  : interactive terminal ဖွင့်သည်")
    print("  --gpus all           : NVIDIA Container Toolkit မှ host GPU အားလုံးကို ဖော်ထုတ်သည်")
    print("  -v host:container    : host directory ကို container အတွင်း mount လုပ်သည်")
    print("  -p 8888:8888         : host port 8888 ကို container port 8888 သို့ ချိတ်သည်")

    cpu_spec = dict(spec)
    cpu_spec["gpus"] = None
    cpu_command = build_docker_run(cpu_spec)
    print("")
    print("GPU မရှိသည့် စက်အတွက် (`--gpus all` ဖယ်သည့်အခါ) —")
    print("  %s" % cpu_command)
    assert "--gpus" not in cpu_command
    print("")
    print("[OK] exercise_3 — GPU flag၊ volume mount ၃ ခုနှင့် port mapping ပါသော run command ကို တည်ဆောက်ပြီးပါသည်")


# ===========================================================================
# Exercise 4 — parse_compose
# ===========================================================================

def exercise_4():
    print("=" * 72)
    print("Exercise 4 — compose ဖိုင်မှ service၊ depends_on နှင့် အတွင်းပိုင်း endpoint")
    print("=" * 72)
    lesson = parse_yaml(LESSON_COMPOSE_TEXT)
    repo = parse_yaml(REPO_COMPOSE_TEXT)

    for label, doc in (("သင်ခန်းစာ၏ docker-compose.yml", lesson), ("ဤ repository ၏ docker-compose.yml", repo)):
        services = doc.get("services") or {}
        print("")
        print("%s — service %d ခု" % (label, len(services)))
        for name, body in services.items():
            image = body.get("image")
            build = body.get("build")
            if image:
                source = "image: %s" % image
            elif isinstance(build, dict):
                source = "build: %s" % build.get("dockerfile", build.get("context"))
            else:
                source = "build: %s" % build
            ports = ", ".join(str(p) for p in (body.get("ports") or []))
            volumes = ", ".join(str(v) for v in (body.get("volumes") or []))
            deps = ", ".join(depends_on_names(body)) or "-"
            print("  %-8s | %s" % (name, source))
            print("           | ports      : %s" % (ports or "-"))
            print("           | volumes    : %s" % (volumes or "-"))
            print("           | depends_on : %s" % deps)
            env = service_env(body)
            if env:
                for key in sorted(env):
                    print("           | env        : %s=%s" % (key, env[key]))
        order = startup_order(services)
        print("  စတင်ရန် အစဉ်လိုက် : %s" % " -> ".join(order))

    ai_dev = (repo.get("services") or {}).get("ai-dev") or {}
    env = service_env(ai_dev)
    assert "qdrant" in (lesson.get("services") or {})
    assert "ai-dev" in (lesson.get("services") or {})
    assert (lesson["services"]["qdrant"].get("image")) == "qdrant/qdrant:v1.12.5"
    assert depends_on_names(ai_dev) == ["qdrant"], depends_on_names(ai_dev)
    assert env.get("QDRANT_URL") == "http://qdrant:6333", env
    assert startup_order(repo["services"])[0] == "qdrant"
    print("")
    print("[OK] exercise_4 — service စာရင်း၊ depends_on နှင့် QDRANT_URL endpoint ကို parse လုပ်ပြီးပါသည်")


# ===========================================================================
# Exercise 5 — container_reachability
# ===========================================================================

def check_reachability(compose, client_name, target_name, port, path):
    """compose network ပေါ်တွင် client မှ target သို့ service name ဖြင့် ရောက်/မရောက် စစ်သည်။"""
    services = compose.get("services") or {}
    result = {"url": "http://%s:%d%s" % (target_name, port, path), "reachable": True, "notes": []}
    if target_name not in services:
        result["reachable"] = False
        result["notes"].append("service '%s' သည် compose ဖိုင်တွင် မရှိပါ" % target_name)
    if client_name not in services:
        result["reachable"] = False
        result["notes"].append("service '%s' သည် compose ဖိုင်တွင် မရှိပါ" % client_name)
    if not result["reachable"]:
        return result

    result["notes"].append(
        "service နှစ်ခုစလုံးသည် Compose ဖန်တီးသည့် default network တွင် ပါဝင်သည်"
    )
    declared = compose.get("networks")
    if declared:
        result["notes"].append("top-level networks ကို ဖော်ပြထားသည် — network အမည်များ ကိုက်ညီမှုကို စစ်ရမည်")
    ports = container_ports(services[target_name])
    if port in ports:
        result["notes"].append("target ၏ container port %d သည် ရရှိနိုင်သည် (%s)" % (port, ", ".join(str(p) for p in ports)))
    else:
        result["reachable"] = False
        result["notes"].append("target တွင် container port %d မဖော်ပြထားပါ (%s)" % (port, ", ".join(str(p) for p in ports)))
    return result


def exercise_5():
    print("=" * 72)
    print("Exercise 5 — AI container မှ vector database သို့ ရောက်နိုင်ခြင်း စစ်ဆေးခြင်း")
    print("=" * 72)
    repo = parse_yaml(REPO_COMPOSE_TEXT)
    target_url = "http://qdrant:6333/collections"
    probe = check_reachability(repo, "ai-dev", "qdrant", 6333, "/collections")
    print("စစ်ဆေးချက် ၁ — service name ဖြင့် ဆက်သွယ်ခြင်း")
    print("  URL      : %s" % probe["url"])
    print("  ရောက်နိုင်မှု : %s" % ("ရောက်နိုင်သည်" if probe["reachable"] else "မရောက်နိုင်ပါ"))
    for note in probe["notes"]:
        print("  - %s" % note)

    missing = check_reachability(repo, "ai-dev", "postgres", 6333, "/collections")
    print("")
    print("  တူညီသည့် စစ်ဆေးမှုကို မရှိသည့် service အမည်ဖြင့် ပြန်လုပ်ခြင်း —")
    print("  service 'postgres' — ရောက်နိုင်မှု : %s" % ("ရောက်နိုင်သည်" if missing["reachable"] else "မရောက်နိုင်ပါ"))
    for note in missing["notes"]:
        print("  - %s" % note)

    print("")
    print("စစ်ဆေးချက် ၂ — host မှ published port ဖြင့် ဆက်သွယ်ခြင်း")
    host_ports = []
    for entry in repo["services"]["qdrant"].get("ports") or []:
        host_ports.append(str(entry))
    print("  host port mapping : %s" % ", ".join(host_ports))
    print("  host မှ URL        : http://localhost:6333/collections")
    print("  ရလဒ်              : host အတွက် ရောက်နိုင်သည် (port 6333 ကို publish လုပ်ထားသည်)")

    print("")
    print("စစ်ဆေးချက် ၃ — container အတွင်းမှ `localhost` သုံးခြင်း (လွဲမှားသည့် နည်းလမ်း)")
    wrong_url = "http://localhost:6333/collections"
    print("  URL      : %s" % wrong_url)
    print("  ရလဒ်      : မရောက်နိုင်ပါ — container အတွင်း `localhost` သည် qdrant မဟုတ်ဘဲ")
    print("             client container ကိုယ်တိုင်ကို ညွှန်သည်။ service name ကို သုံးရမည်။")

    assert probe["url"] == target_url
    assert probe["reachable"] is True
    assert "6333" in " ".join(host_ports)
    assert missing["reachable"] is False
    print("")
    print("[OK] exercise_5 — ai-dev မှ http://qdrant:6333/collections သို့ ရောက်နိုင်ကြောင်း စစ်ပြီးပါသည်")


# ===========================================================================
# Exercise 6 — image_report
# ===========================================================================

def installed_packages(instructions):
    pinned, loose = [], []
    for args in find_all(instructions, "RUN"):
        if "pip install" not in args:
            continue
        tokens = args.split()
        skip_next = False
        for token in tokens:
            if skip_next:
                skip_next = False
                continue
            if token.startswith("--"):
                if token in ("--index-url", "--extra-index-url", "-i"):
                    skip_next = True
                continue
            if token in ("python", "-m", "pip", "install", "&&", "|", ">"):
                continue
            if "==" in token:
                pinned.append(token)
            elif re.fullmatch(r"[A-Za-z][A-Za-z0-9_.\-]*", token):
                loose.append(token)
    return pinned, loose


def exercise_6():
    print("=" * 72)
    print("Exercise 6 — image အစီရင်ခံစာ — အရွယ်အစားနှင့် layer")
    print("=" * 72)
    instructions = parse_dockerfile(DOCKERFILE_TEXT)
    base = extract_base_image(instructions)
    platform = extract_platform(instructions)
    layers = count_layers(instructions)
    expose = find_instruction(instructions, "EXPOSE")
    workdir = find_instruction(instructions, "WORKDIR")
    cmd = find_instruction(instructions, "CMD")
    volumes = find_all(instructions, "VOLUME")
    declared = []
    for entry in volumes:
        declared.extend(re.findall(r'"([^"]+)"', entry))
    pinned, loose = installed_packages(instructions)

    run_names = [args for args in find_all(instructions, "RUN")]
    python_version = "3.12" if any("python3.12" in args for args in run_names) else "?"

    print("IMAGE REPORT — ai-dev")
    print("  base image        : %s" % base)
    print("  platform          : %s" % platform)
    print("  instruction       : %d ခု" % len(instructions))
    print("  layer             : %d ခု (base layer အပေါ် ထပ်သည့် layer)" % layers)
    print("  Python            : %s (deadsnakes PPA မှ တင်သည်)" % python_version)
    print("  WORKDIR           : %s" % workdir)
    print("  EXPOSE            : %s (Jupyter)" % expose)
    print("  VOLUME            : %s" % ", ".join(declared))
    print("  CMD               : %s" % cmd)
    print("  pinned package    : %s" % ", ".join(pinned))
    print("  unpinned package  : %s" % ", ".join(loose))

    layer_kinds = {}
    for name, _args in instructions:
        layer_kinds[name] = layer_kinds.get(name, 0) + 1
    print("  layer အမျိုးအစား    : %s" % ", ".join("%s x %d" % (k, layer_kinds[k]) for k in sorted(layer_kinds)))

    devel = BASE_IMAGES[0]
    runtime = BASE_IMAGES[1]
    print("")
    print("  base layer အရွယ်   : devel %s / runtime %s" % (devel["size_label"], runtime["size_label"]))
    print("  ကွာခြားချက်        : %d MB (%.1f GB)" % (devel["size_mb"] - runtime["size_mb"],
                                                   (devel["size_mb"] - runtime["size_mb"]) / 1024.0))
    print("  သတိပြုရန်          : image တစ်ခုလုံး၏ တိကျသည့် အရွယ်ကို သင်ခန်းစာတွင် မဖော်ပြထားပါ၊")
    print("                      build ပြီးနောက် `docker images ai-dev` ဖြင့် တိုင်းရမည်။")
    print("  layer ပြန်သုံးခြင်း  : မပြောင်းသည့် layer များကို cache မှ ပြန်သုံးသဖြင့် ဒုတိယ build သည် လျင်မြန်သည်။")

    assert base == "nvidia/cuda:12.4.1-devel-ubuntu22.04"
    assert layers == 12
    assert expose == "8888"
    assert declared == ["/workspace", "/models"], declared
    assert "torch==2.6.0+cu124" in pinned
    assert "torchvision==0.21.0+cu124" in pinned
    assert "torchaudio==2.6.0+cu124" in pinned
    assert "transformers" in loose and "safetensors" in loose
    assert python_version == "3.12"
    print("")
    print("[OK] exercise_6 — image ၏ layer၊ package နှင့် port အစီရင်ခံစာကို ထုတ်ပြီးပါသည်")


# ===========================================================================
# Runner
# ===========================================================================

def main():
    exercise_1()
    print("")
    exercise_2()
    print("")
    exercise_3()
    print("")
    exercise_4()
    print("")
    exercise_5()
    print("")
    exercise_6()
    print("")
    print("=" * 72)
    print("[PASS] All 6/6 exercises passed successfully.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
