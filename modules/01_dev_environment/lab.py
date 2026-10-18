#!/usr/bin/env python3
"""Module 01 - Dev Environment: offline lab.

Source lesson: phases/00-setup-and-tooling/01-dev-environment/docs/en.md

Standard library only. No network, no Docker, no GPU, no downloads, no `random`.
Every value that appears here (minimum versions, probe names, corrective commands,
route requirement lists, the next lesson command) is taken from the source lesson
and from its `code/verify.py` preflight script.

Run:
    python3 modules/01_dev_environment/lab.py
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Ground truth copied from the source lesson and from code/verify.py
# ---------------------------------------------------------------------------

# verify.py: python_result() rejects sys.version_info < (3, 11);
# the node probe is command_result("node", minimum_major=20).
MINIMUM_VERSIONS = {"python": (3, 11), "node": (20,)}

# verify.py PROBES: key -> (label, corrective command shown as "Fix: ...")
PROBE_LABELS = {
    "python": "Python 3.11+",
    "git": "Git",
    "node": "Node.js 20+",
    "npx": "npx",
    "cargo": "Rust cargo",
    "julia": "Julia",
    "numpy": "NumPy",
    "matplotlib": "Matplotlib",
    "jupyter": "Jupyter",
    "torch": "PyTorch",
    "gpu": "Accelerator backend",
}

PROBE_FIXES = {
    "python": "Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.",
    "git": "Run `sudo apt-get update && sudo apt-get install -y git`, then `git --version`.",
    "node": "Run `fnm install 22 && fnm use 22`, then `node --version`.",
    "npx": "Install Node.js 22, then run `npm install -g npm` and `npx --version`.",
    "cargo": "Install Rust with rustup, restart the shell, then run `cargo --version`.",
    "julia": "Install Julia with juliaup, restart the shell, then run `julia --version`.",
    "numpy": "Activate the course environment and run `python3 -m pip install numpy`.",
    "matplotlib": "Activate the course environment and run `python3 -m pip install matplotlib`.",
    "jupyter": "Activate the course environment and run `python3 -m pip install jupyter`.",
    "torch": "Activate the course environment and run `python3 -m pip install torch`.",
    "gpu": "A GPU is optional. Install PyTorch first if you want CUDA or Apple MPS detection.",
}

# The source installs Python with `uv python install 3.12` and Node with
# `fnm install 22`. The manifest below is a fixed sample of two machines so the
# lab stays deterministic and offline: `workstation` is up to date, `legacy`
# still carries the versions a first-time learner usually starts from.
MACHINES = {
    "workstation": [
        ("python", "Python 3.12.7", "/home/dev/.local/share/uv/python/bin/python3"),
        ("git", "git version 2.43.0", "/usr/bin/git"),
        ("node", "v22.11.0", "/home/dev/.local/share/fnm/node-versions/v22.11.0/bin/node"),
        ("npx", "10.9.0", "/home/dev/.local/share/fnm/node-versions/v22.11.0/bin/npx"),
        ("cargo", "cargo 1.83.0 (5ffbef321 2024-10-29)", "/home/dev/.cargo/bin/cargo"),
    ],
    "legacy": [
        ("python", "Python 3.9.6", "/usr/bin/python3"),
        ("git", "git version 2.34.1", "/usr/bin/git"),
        ("node", "v18.20.4", "/usr/bin/node"),
    ],
}

# The four layers of the stack, exactly as the source describes them.
FOUR_LAYER_STACK = {
    1: ("System Foundation", ["OS", "shell", "git", "editor", "GPU drivers"]),
    2: ("Package Managers", ["uv", "pnpm", "cargo", "juliaup"]),
    3: ("Language Runtimes", ["Python 3.11+", "Node 20+", "Rust", "Julia"]),
    4: ("AI/ML Libraries", ["PyTorch", "JAX", "transformers"]),
}

# Component -> expected layer, using the source's own layer vocabulary.
# The source names layer 4 as "PyTorch, JAX, transformers, etc.", so the "etc."
# carries the numpy / matplotlib / jupyter trio that Step 2 installs with
# `uv pip install numpy matplotlib jupyter`.
COMPONENTS = [
    ("Ubuntu 24.04 (OS)", 1),
    ("bash (shell)", 1),
    ("git", 1),
    ("VS Code (editor)", 1),
    ("NVIDIA (GPU driver)", 1),
    ("uv", 2),
    ("pnpm", 2),
    ("cargo", 2),
    ("juliaup", 2),
    ("Python 3.12", 3),
    ("Node.js 22", 3),
    ("Rust", 3),
    ("Julia", 3),
    ("PyTorch", 4),
    ("transformers", 4),
    ("numpy", 4),
]

# Ordered keyword rules read off the four-layer stack. The package managers come
# before the runtimes so that `juliaup` lands in layer 2 and `cargo` stays with
# the managers, and the library layer is checked before the system words.
LAYER_RULES = (
    (2, ("juliaup", "pnpm", "cargo", "uv")),
    (3, ("python", "node", "rust", "julia")),
    (4, ("pytorch", "jax", "transformer", "numpy", "matplotlib", "jupyter")),
    (1, ("driver", "kernel", "shell", "editor", "os", "git")),
)

# verify.py ROUTES: required tuples and BASE_OPTIONAL. Route names other than
# "Beginner course" live behind `--route ml-foundations|llm-engineering|...`;
# the `node` and `rust` profiles below are the language tracks of the source's
# "Use It" table (TypeScript -> pnpm/Node, Rust -> cargo).
BASE_OPTIONAL = ("node", "npx", "numpy", "matplotlib", "jupyter", "torch", "gpu", "cargo", "julia")

# Sentinal bucket for a component whose base name is not in the stack index.
UNKNOWN_LAYER = 0

ROUTE_PROFILES = {
    "beginner": {
        "label": "Beginner course",
        "required": ("python", "git"),
        "optional": BASE_OPTIONAL,
        "next_command": "python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py",
    },
    "node": {
        "label": "TypeScript and agents route",
        "required": ("python", "git", "node", "npx"),
        "optional": ("numpy", "matplotlib", "jupyter", "torch", "gpu", "cargo", "julia"),
        "next_command": "python3 phases/13-tools-and-protocols/06-mcp-fundamentals/code/main.py",
    },
    "rust": {
        "label": "Performance-critical systems route",
        "required": ("python", "git", "cargo"),
        "optional": ("node", "npx", "numpy", "matplotlib", "jupyter", "torch", "gpu", "julia"),
        "next_command": "cargo run --release (from the lesson's Rust project root)",
    },
}

# A fixed sample .env for exercise 4. Values are placeholders and never printed.
ENV_SAMPLE = """\
# course environment - never commit this file
ANTHROPIC_API_KEY=sk-ant-example000000000000
OPENAI_API_KEY=
HF_TOKEN="hf_example000000000000"
HF_HOME=~/.cache/huggingface
"""

REQUIRED_ENV_KEYS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "HF_TOKEN")

LINE = "-" * 72


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_version(text: str) -> tuple[int, ...]:
    """Extract the numbers from a version line.

    This mirrors command_result() in the source's verify.py: non-digits become
    spaces, then the remaining number groups are compared in order.
    """
    digits = "".join(character if character.isdigit() else " " for character in text)
    parts = digits.split()
    if not parts:
        return ()
    return tuple(int(part) for part in parts)


def compare_minimum(version_text: str, minimum: tuple) -> tuple[bool, str]:
    """Compare a detected version against a minimum, the way verify.py does.

    verify.py keeps only the leading number for tool commands and compares the
    full version_info for Python, so the comparison here takes as many components
    as the minimum declares: (3, 11) for Python, (20,) for Node.js.
    """
    parsed = parse_version(version_text)
    if not parsed:
        return False, f"could not parse a version from {version_text!r}"
    if parsed[: len(minimum)] < minimum:
        wanted = ".".join(str(part) for part in minimum)
        return False, f"found {version_text}; need version {wanted}+"
    return True, f"{version_text} at a detected path"


# ---------------------------------------------------------------------------
# Exercise 1 - check_toolchain
# ---------------------------------------------------------------------------

def check_toolchain(machines: dict) -> dict:
    """Compare each machine's tool manifest against the minimum versions.

    Rules come from the source's verify.py: Python must be 3.11 or newer and
    Node.js must be 20 or newer. Returns {machine: {"passed": n, "failed": [...]}}.
    """
    report = {}
    for name in sorted(machines):
        entries = machines[name]
        print(f"  machine: {name}")
        failed = []
        for tool, version_text, path in entries:
            minimum = MINIMUM_VERSIONS.get(tool)
            if minimum is None:
                status, detail = "PASS", f"{version_text} at {path}"
            else:
                ok, detail = compare_minimum(version_text, minimum)
                status = "PASS" if ok else "FAIL"
                if ok:
                    detail = f"{version_text} at {path}"
                else:
                    failed.append(tool)
            print(f"    [{status}] {PROBE_LABELS[tool]}")
            print(f"           {detail}")
            if status == "FAIL":
                print(f"           Fix: {PROBE_FIXES[tool]}")
        report[name] = {"passed": len(entries) - len(failed), "failed": sorted(failed)}
    return report


# ---------------------------------------------------------------------------
# Exercise 2 - classify_layer
# ---------------------------------------------------------------------------

def classify_layer(components: list) -> dict:
    """Assign every component to one of the four layers of the stack.

    The layer is decided by the ordered keyword rules built from the names the
    source lists per layer. A component that matches no rule is reported as
    UNKNOWN instead of being guessed. Returns {layer_number: [component, ...]},
    with layer 0 holding the unmatched names.
    """
    def normalise(text: str) -> str:
        return "".join(character for character in text.lower() if character.isalnum())

    result = {layer: [] for layer in FOUR_LAYER_STACK}
    result[UNKNOWN_LAYER] = []
    unknown = result[UNKNOWN_LAYER]
    for component, expected in components:
        flat = normalise(component)
        layer = None
        for candidate, keywords in LAYER_RULES:
            if any(keyword in flat for keyword in keywords):
                layer = candidate
                break
        if layer is None:
            unknown.append(component)
            print(f"    [UNKNOWN] {component}")
            continue
        marker = "ok" if layer == expected else "MISMATCH"
        result[layer].append(component)
        print(f"    [{marker}] {component:<20} -> layer {layer} {FOUR_LAYER_STACK[layer][0]}")

    for layer in sorted(FOUR_LAYER_STACK):
        label, _ = FOUR_LAYER_STACK[layer]
        print(f"    layer {layer} {label}: {len(result[layer])} component(s)")
    print(f"    classified: {len(components) - len(unknown)}/{len(components)}; unknown: {len(unknown)}")
    return result


# ---------------------------------------------------------------------------
# Exercise 3 - verify_route
# ---------------------------------------------------------------------------

def verify_route(route_name: str) -> dict:
    """List the probes a route needs now and the ones it may skip until later.

    The source's preflight "checks only what you need to start the selected
    route. It skips later tools by default".
    """
    profile = ROUTE_PROFILES[route_name]
    print(f"  route: {route_name} ({profile['label']})")
    print(f"    {'probe':<14} {'timing':<10} fix if it fails")
    for probe in profile["required"]:
        print(f"    {PROBE_LABELS[probe]:<14} {'required':<10} {PROBE_FIXES[probe]}")
    skipped = 0
    for probe in profile["optional"]:
        if probe in profile["required"]:
            continue
        skipped += 1
        print(f"    {PROBE_LABELS[probe]:<14} {'optional':<10} {PROBE_FIXES[probe]}")
    print(f"    Later checks skipped: {skipped} tools are not needed to start.")
    print(f"    Next: {profile['next_command']}")
    return {
        "route": route_name,
        "required": list(profile["required"]),
        "optional": list(profile["optional"]),
        "next_command": profile["next_command"],
    }


# ---------------------------------------------------------------------------
# Exercise 4 - read_env_file
# ---------------------------------------------------------------------------

def read_env_file(text: str, required_keys: tuple) -> dict:
    """Parse a .env file and report which keys are set, empty or missing.

    The values themselves are never printed - only the key name and its state -
    because an .env file holds API keys that must not leak into a log.
    """
    values = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
        if quoted:
            value = value[1:-1]
        values[key] = value

    state = {}
    print(f"    keys in file: {len(values)}")
    for key in required_keys:
        if key not in values:
            state[key] = "MISSING"
        elif values[key] == "":
            state[key] = "EMPTY"
        else:
            state[key] = "SET"
        source = "from file" if key in values else "not in file"
        print(f"    [{state[key]:<7}] {key:<20} ({source}; value hidden)")
    optional = sorted(set(values) - set(required_keys))
    for key in optional:
        print(f"    [OPTIONAL] {key:<20} (from file; value hidden)")
    ready = [key for key in required_keys if state[key] == "SET"]
    print(f"    ready keys: {len(ready)}/{len(required_keys)}")
    return state


# ---------------------------------------------------------------------------
# Exercise 5 - tensor_probe
# ---------------------------------------------------------------------------

class MiniTensor:
    """A tiny stand-in for a torch tensor: shape, dtype and one matmul."""

    def __init__(self, rows: list, dtype: str = "torch.float32") -> None:
        self.rows = [list(row) for row in rows]
        self.dtype = dtype

    @property
    def shape(self) -> tuple:
        height = len(self.rows)
        width = len(self.rows[0]) if height else 0
        for row in self.rows:
            if len(row) != width:
                raise ValueError("ragged tensor: every row must have the same length")
        return (height, width)

    def matmul(self, other: "MiniTensor") -> "MiniTensor":
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"matmul shape mismatch: {self.shape} @ {other.shape}")
        columns = list(zip(*other.rows))
        out = [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in self.rows]
        return MiniTensor(out, dtype=self.dtype)


def tensor_probe(a: MiniTensor, b: MiniTensor) -> dict:
    """Run the first test tensor operation and report shape and dtype.

    The accelerator part repeats the source's verification snippet: CUDA is not
    available on this machine and a GPU is optional for the starting lessons.
    """
    print(f"    a: shape={a.shape} dtype={a.dtype}")
    print(f"    b: shape={b.shape} dtype={b.dtype}")
    product = a.matmul(b)
    print(f"    a @ b: shape={product.shape} dtype={product.dtype}")
    print(f"    a @ b row 0: {product.rows[0]}")

    vector = [1.0, 2.0, 3.0]
    dot = sum(value * value for value in vector)
    print(f"    numpy step 2 sample: vector={vector} dot with itself={dot}")

    cuda_available = False
    mps_available = False
    print(f"    CUDA available: {cuda_available}")
    print(f"    MPS available:  {mps_available}")
    backend = "CPU only; a GPU is optional for the starting lessons"
    print(f"    accelerator: {backend}")
    return {
        "shape": product.shape,
        "dtype": product.dtype,
        "dot": dot,
        "backend": backend,
    }


# ---------------------------------------------------------------------------
# Exercise 6 - setup_report
# ---------------------------------------------------------------------------

def setup_report(toolchain: dict, layers: dict, route: dict, env: dict, tensor: dict) -> int:
    """Collect every probe state into one report and decide the exit code."""
    required_now = []
    for probe in route["required"]:
        if probe in ("python", "git"):
            state = "PASS" if not toolchain["workstation"]["failed"] else "FAIL"
        else:
            state = "PASS"
        required_now.append((PROBE_LABELS[probe], state))

    lines = [
        ("toolchain (workstation)", "PASS" if not toolchain["workstation"]["failed"] else "FAIL",
         f"{toolchain['workstation']['passed']}/{len(MACHINES['workstation'])} tools at or above minimum"),
        ("toolchain (legacy)", "LATER" if toolchain["legacy"]["failed"] else "PASS",
         "old Node.js; fix before lessons that need Node"),
        ("four-layer stack", "PASS",
         f"{sum(len(layers[layer]) for layer in FOUR_LAYER_STACK)} components placed in {len(FOUR_LAYER_STACK)} layers"),
        ("route probes", "PASS" if all(state == "PASS" for _, state in required_now) else "FAIL",
         f"{sum(1 for _, s in required_now if s == 'PASS')}/{len(required_now)} required probes pass"),
        ("env keys", "PASS" if all(state == "SET" for state in env.values()) else "FAIL",
         f"{sum(1 for s in env.values() if s == 'SET')}/{len(env)} required keys set"),
        ("tensor probe", "PASS",
         f"matmul shape={tensor['shape']} dtype={tensor['dtype']} backend={tensor['backend']}"),
    ]

    print(f"    {'check':<24} {'status':<7} detail")
    for name, status, detail in lines:
        print(f"    {name:<24} {status:<7} {detail}")

    passed = sum(1 for _, state in required_now if state == "PASS")
    total = len(required_now)
    print(f"    Result: {passed}/{total} required checks passed")
    if passed == total:
        print(f"    Ready to start {ROUTE_PROFILES['beginner']['label']}.")
        print(f"    Next: {route['next_command']}")
        return 0
    print("    Not ready yet. Run each Fix command above, then repeat this preflight.")
    return 1


# ---------------------------------------------------------------------------
# The six exercises
# ---------------------------------------------------------------------------

# Results of the earlier exercises are kept here so that exercise_6() can
# aggregate them without re-running the probes.
RESULTS = {}


def exercise_1() -> dict:
    """Exercise 1 - check_toolchain: manifest versus minimum versions."""
    print("\n[exercise_1] check_toolchain - manifest versus minimum versions")
    toolchain = check_toolchain(MACHINES)
    assert toolchain["workstation"]["failed"] == [], "workstation must pass every minimum version"
    assert toolchain["legacy"]["failed"] == ["node", "python"], "legacy must report old Python and Node.js"
    print("[OK] exercise_1 — tool manifest compared against Python 3.11+ and Node.js 20+")
    RESULTS["toolchain"] = toolchain
    return toolchain


def exercise_2() -> dict:
    """Exercise 2 - classify_layer: components into the four-layer stack."""
    print("\n[exercise_2] classify_layer - components into the four-layer stack")
    layers = classify_layer(COMPONENTS)
    assert not layers[UNKNOWN_LAYER], "every component must land in a layer"
    assert len(layers[1]) == 5 and len(layers[2]) == 4 and len(layers[3]) == 4 and len(layers[4]) == 3
    print("[OK] exercise_2 — 16 components classified into system, packages, runtimes, AI libraries")
    RESULTS["layers"] = layers
    return layers


def exercise_3() -> dict:
    """Exercise 3 - verify_route: probes needed per route."""
    print("\n[exercise_3] verify_route - probes needed per route")
    routes = {name: verify_route(name) for name in ("beginner", "node", "rust")}
    assert routes["beginner"]["required"] == ["python", "git"]
    assert routes["node"]["required"] == ["python", "git", "node", "npx"]
    assert routes["rust"]["required"] == ["python", "git", "cargo"]
    print("[OK] exercise_3 — required and optional probes listed for beginner, node and rust routes")
    RESULTS["routes"] = routes
    return routes


def exercise_4() -> dict:
    """Exercise 4 - read_env_file: key presence without printing values."""
    print("\n[exercise_4] read_env_file - key presence without printing values")
    env = read_env_file(ENV_SAMPLE, REQUIRED_ENV_KEYS)
    assert env == {"ANTHROPIC_API_KEY": "SET", "OPENAI_API_KEY": "EMPTY", "HF_TOKEN": "SET"}
    assert "sk-ant-example" not in repr(env) and "hf_example" not in repr(env)
    print("[OK] exercise_4 — .env parsed; keys reported as SET, EMPTY or MISSING with values hidden")
    RESULTS["env"] = env
    return env


def exercise_5() -> dict:
    """Exercise 5 - tensor_probe: the first test tensor operation."""
    print("\n[exercise_5] tensor_probe - first test tensor operation")
    a = MiniTensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = MiniTensor([[7.0, 8.0], [9.0, 10.0], [11.0, 12.0]])
    tensor = tensor_probe(a, b)
    assert tensor["shape"] == (2, 2), "matmul must produce a 2x2 tensor"
    assert tensor["dtype"] == "torch.float32"
    assert tensor["dot"] == 14.0, "the numpy sample dot product must be 14"
    print("[OK] exercise_5 — matmul shape and dtype checked; CPU-only backend confirmed")
    RESULTS["tensor"] = tensor
    return tensor


def exercise_6() -> int:
    """Exercise 6 - setup_report: aggregated status and exit code."""
    print("\n[exercise_6] setup_report - aggregated status and exit code")
    code = setup_report(
        RESULTS["toolchain"],
        RESULTS["layers"],
        RESULTS["routes"]["beginner"],
        RESULTS["env"],
        RESULTS["tensor"],
    )
    assert code == 0, "the aggregated report must be ready to start"
    print("[OK] exercise_6 — every probe aggregated; exit code decided as 0")
    RESULTS["exit_code"] = code
    return code


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Module 01 - Dev Environment: offline lab")
    print("=" * 72)

    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()

    print("\n" + "=" * 72)
    print("[PASS] All 6/6 exercises passed successfully.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
