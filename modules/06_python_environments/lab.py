#!/usr/bin/env python3
"""Module 06 - Python Environments: offline, deterministic lab.

Standard library only. No network, no pip, no conda, no environment creation.
Every exercise parses or compares text that mirrors the source lesson
(phases/00-setup-and-tooling/06-python-environments).

Run from the repository root:

    python3 modules/06_python_environments/lab.py
"""

from __future__ import annotations

import tempfile
import tomllib
from pathlib import Path

# --------------------------------------------------------------------------
# Fixtures: the same content the source lesson prints for pyproject.toml
# --------------------------------------------------------------------------

PYPROJECT_DEMO = """\
[project]
name = "ai-engineering-from-scratch"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "numpy>=1.26",
    "matplotlib>=3.8",
    "jupyter>=1.0",
    "scikit-learn>=1.4",
]

[project.optional-dependencies]
torch = ["torch>=2.3", "torchvision>=0.18"]
llm = ["anthropic>=0.39", "openai>=1.50"]
"""

LOCKFILE_GOOD = """\
# requirements.lock - every entry pinned
numpy==1.26.4
matplotlib==3.8.4
jupyter==1.0.0
scikit-learn==1.4.2
torch==2.4.0
torchvision==0.19.0
anthropic==0.39.0
openai==1.50.2
"""

LOCKFILE_BAD = """\
# requirements.lock - not reproducible yet
numpy==1.26.4
matplotlib
jupyter==1.0.0
anthropic==0.39.0
"""

PACKAGE_NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")


# --------------------------------------------------------------------------
# Small helpers (shared by the exercises)
# --------------------------------------------------------------------------

def split_requirement(spec: str) -> tuple[str, str]:
    """Split 'numpy>=1.26' into ('numpy', '>=1.26')."""
    for index, char in enumerate(spec):
        if char not in PACKAGE_NAME_CHARS:
            return spec[:index].strip(), spec[index:].strip()
    return spec.strip(), ""


def requirement_names(specs: list[str]) -> list[str]:
    """Return the distribution names of a list of requirement strings."""
    return [split_requirement(spec)[0] for spec in specs]


def parse_lockfile(text: str) -> dict:
    """Parse a requirements-style lockfile into pinned and unpinned entries."""
    pinned: dict[str, str] = {}
    unpinned: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==", 1)
            pinned[name.strip()] = version.strip()
        else:
            unpinned.append(requirement_names([line])[0])
    return {"pinned": pinned, "unpinned": unpinned}


def compare_cuda(torch_cuda: str, driver_cuda: str) -> tuple[bool, str]:
    """Decide whether a torch CUDA build runs on a given driver CUDA version.

    Rule taken from the source lesson: the PyTorch CUDA version must be
    lower than or equal to the driver CUDA version. A differing major
    version is treated as incompatible, as the source lesson states that
    CUDA 11.8 builds do not work with CUDA 12.x drivers.
    """
    torch_parts = tuple(int(part) for part in torch_cuda.split("."))
    driver_parts = tuple(int(part) for part in driver_cuda.split("."))
    if torch_parts[0] != driver_parts[0]:
        return False, "major version mismatch (torch CUDA %s vs driver CUDA %s)" % (
            torch_cuda,
            driver_cuda,
        )
    if torch_parts > driver_parts:
        return False, "torch CUDA %s is newer than driver CUDA %s" % (torch_cuda, driver_cuda)
    return True, "torch CUDA %s <= driver CUDA %s" % (torch_cuda, driver_cuda)


def plan_environments(projects: list[dict]) -> list[dict]:
    """Group projects into environments: identical requirement sets share one.

    Two projects share an environment only when their requirement sets are
    equal, which is the strategy the source lesson shows for this course
    (phases 04 and 05 share the PyTorch environment, phases 08 and 11 get
    their own). A project without requirements joins the shared lightweight
    base environment. The order of the input list decides the order of the
    environments, so the result is deterministic.
    """
    groups: list[dict] = []
    for project in projects:
        requirements = {}
        for spec in project["requires"]:
            name, version_spec = split_requirement(spec)
            requirements[name] = version_spec

        if not requirements:
            target = None
            for group in groups:
                if not group["requirements"]:
                    target = group
                    break
            if target is None:
                target = {"env": "base (.venv)", "projects": [], "requirements": {}}
                groups.append(target)
            target["projects"].append(project["name"])
            continue

        placed = False
        for group in groups:
            if group["requirements"] == requirements:
                group["projects"].append(project["name"])
                placed = True
                break
        if not placed:
            groups.append(
                {
                    "env": "env-%d" % (sum(1 for g in groups if g["requirements"]) + 1),
                    "projects": [project["name"]],
                    "requirements": dict(requirements),
                }
            )

    environments = [group for group in groups if group["requirements"]]
    base = [group for group in groups if not group["requirements"]]
    return environments + base


def find_conflicts(projects: list[dict]) -> list[tuple]:
    """List package specs that appear in two projects with different versions."""
    seen: dict[str, dict[str, str]] = {}
    conflicts = []
    for project in projects:
        for spec in project["requires"]:
            name, version_spec = split_requirement(spec)
            for other_project, other_spec in seen.get(name, {}).items():
                if other_project != project["name"] and other_spec != version_spec:
                    conflicts.append((name, other_project, other_spec, project["name"], version_spec))
            seen.setdefault(name, {})[project["name"]] = version_spec
    return conflicts


# --------------------------------------------------------------------------
# Exercise 1 - parse_pyproject
# --------------------------------------------------------------------------

def parse_pyproject(text: str) -> dict:
    data = tomllib.loads(text)
    project = data["project"]
    optional = project.get("optional-dependencies", {})
    return {
        "name": project["name"],
        "version": project["version"],
        "requires_python": project["requires-python"],
        "dependencies": list(project.get("dependencies", [])),
        "optional": {group: list(specs) for group, specs in optional.items()},
        "uses_setup_py_keys": any(key in data for key in ("build-system", "tool") ),
    }


def exercise_1() -> None:
    """Parse pyproject.toml: base dependencies and optional groups."""
    with tempfile.TemporaryDirectory() as tmp:
        manifest_path = Path(tmp) / "pyproject.toml"
        manifest_path.write_text(PYPROJECT_DEMO, encoding="utf-8")
        parsed = parse_pyproject(manifest_path.read_text(encoding="utf-8"))

    print("=== Exercise 1 - parse pyproject.toml ===")
    print("file                  : %s" % (Path("<tmp>") / "pyproject.toml"))
    print("project name          : %s" % parsed["name"])
    print("project version       : %s" % parsed["version"])
    print("requires-python       : %s" % parsed["requires_python"])
    print("base dependencies     : %d" % len(parsed["dependencies"]))
    for spec in parsed["dependencies"]:
        print("   - %-22s name=%s" % (spec, split_requirement(spec)[0]))
    print("optional groups       : %d" % len(parsed["optional"]))
    for group in sorted(parsed["optional"]):
        print("   - %-6s -> %s" % (group, ", ".join(sorted(parsed["optional"][group]))))

    install_commands = [
        'uv pip install -e ".[%s]"' % group for group in sorted(parsed["optional"])
    ]
    print("extra install commands:")
    for command in install_commands:
        print("   %s" % command)

    assert parsed["name"] == "ai-engineering-from-scratch"
    assert parsed["requires_python"] == ">=3.11"
    assert len(parsed["dependencies"]) == 4
    assert sorted(parsed["optional"]) == ["llm", "torch"]
    assert requirement_names(parsed["optional"]["torch"]) == ["torch", "torchvision"]
    assert requirement_names(parsed["dependencies"]) == [
        "numpy",
        "matplotlib",
        "jupyter",
        "scikit-learn",
    ]
    print("[OK] exercise_1 - parsed pyproject.toml base deps and 2 optional groups")


# --------------------------------------------------------------------------
# Exercise 2 - check_lockfile
# --------------------------------------------------------------------------

def check_lockfile(manifest_text: str, lockfile_text: str) -> dict:
    manifest = parse_pyproject(manifest_text)
    lock = parse_lockfile(lockfile_text)

    wanted = requirement_names(manifest["dependencies"])
    for group in manifest["optional"]:
        wanted.extend(requirement_names(manifest["optional"][group]))
    wanted = sorted(set(wanted))

    pinned_names = set(lock["pinned"])
    missing = sorted(name for name in wanted if name not in pinned_names)
    extra = sorted(name for name in pinned_names if name not in wanted)
    unpinned = sorted(lock["unpinned"])

    return {
        "pinned_count": len(lock["pinned"]),
        "wanted_count": len(wanted),
        "missing": missing,
        "extra": extra,
        "unpinned": unpinned,
        "reproducible": not missing and not unpinned,
    }


def exercise_2() -> None:
    """Check that a lockfile pins every manifest dependency exactly."""
    print("=== Exercise 2 - check lockfile against the manifest ===")
    results = {}
    for label, text in (("requirements.lock (good)", LOCKFILE_GOOD), ("requirements.lock (bad)", LOCKFILE_BAD)):
        result = check_lockfile(PYPROJECT_DEMO, text)
        results[label] = result
        print("%s" % label)
        print("   pinned entries        : %d" % result["pinned_count"])
        print("   manifest names        : %d" % result["wanted_count"])
        print("   missing from lockfile : %s" % (result["missing"] or "none"))
        print("   not in manifest       : %s" % (result["extra"] or "none"))
        print("   unpinned entries      : %s" % (result["unpinned"] or "none"))
        print("   reproducible          : %s" % ("YES" if result["reproducible"] else "NO"))

    good = results["requirements.lock (good)"]
    bad = results["requirements.lock (bad)"]
    assert good["reproducible"] is True
    assert good["missing"] == []
    assert bad["reproducible"] is False
    assert bad["unpinned"] == ["matplotlib"]
    assert "scikit-learn" in bad["missing"]
    assert bad["extra"] == []
    print("[OK] exercise_2 - lockfile pin check found missing and unpinned entries")


# --------------------------------------------------------------------------
# Exercise 3 - env_isolation_check
# --------------------------------------------------------------------------

ENV_A = {
    "name": ".venv",
    "manager": "uv",
    "packages": {"torch": "2.4.0", "numpy": "1.26.4", "transformers": "4.44.0", "matplotlib": "3.8.4"},
}
ENV_B = {
    "name": "myenv",
    "manager": "conda",
    "packages": {"pytorch": "2.4.0", "numpy": "1.26.4", "diffusers": "0.28.0", "requests": "2.32.3"},
}
ENV_B_INSTALLERS = {"pytorch": "conda", "diffusers": "conda", "numpy": "pip", "requests": "pip"}


def env_isolation_check(env_a: dict, env_b: dict, installers: dict) -> dict:
    names_a = set(env_a["packages"])
    names_b = set(env_b["packages"])
    shared = sorted(names_a & names_b)
    only_a = sorted(names_a - names_b)
    only_b = sorted(names_b - names_a)

    same_version = sorted(name for name in shared if env_a["packages"][name] == env_b["packages"][name])
    differing = sorted(name for name in shared if env_a["packages"][name] != env_b["packages"][name])

    pip_over_conda = []
    if env_b["manager"] == "conda":
        pip_over_conda = sorted(
            name for name in env_b["packages"] if installers.get(name) == "pip"
        )
    return {
        "only_a": only_a,
        "only_b": only_b,
        "shared": shared,
        "same_version": same_version,
        "differing": differing,
        "pip_over_conda": pip_over_conda,
        "isolated": bool(only_a and only_b),
    }


def exercise_3() -> None:
    """Compare two environments: catch a pip/conda mix-up and confirm isolation."""
    print("=== Exercise 3 - compare the package sets of two environments ===")
    result = env_isolation_check(ENV_A, ENV_B, ENV_B_INSTALLERS)

    print("environment A         : %s (manager=%s, %d packages)" % (ENV_A["name"], ENV_A["manager"], len(ENV_A["packages"])))
    print("environment B         : %s (manager=%s, %d packages)" % (ENV_B["name"], ENV_B["manager"], len(ENV_B["packages"])))
    print("only in A             : %s" % ", ".join(result["only_a"]))
    print("only in B             : %s" % ", ".join(result["only_b"]))
    print("in both, same version : %s" % (", ".join(result["same_version"]) or "none"))
    print("in both, different    : %s" % (", ".join(result["differing"]) or "none"))
    print("isolation             : %s" % ("CONFIRMED (each environment holds its own copy)" if result["isolated"] else "NOT CONFIRMED"))
    print("pip over conda in B   : %s" % (", ".join(result["pip_over_conda"]) or "none"))
    if result["pip_over_conda"]:
        print("verdict               : MIX-UP - conda env B holds pip installs; let conda manage them")
    else:
        print("verdict               : CLEAN - every package in B comes from conda")

    assert result["isolated"] is True
    assert result["differing"] == []
    assert result["same_version"] == ["numpy"]
    assert result["only_a"] == ["matplotlib", "torch", "transformers"]
    assert result["pip_over_conda"] == ["numpy", "requests"]
    print("[OK] exercise_3 - caught pip/conda mix-up and confirmed env isolation")


# --------------------------------------------------------------------------
# Exercise 4 - torch_cuda_matrix
# --------------------------------------------------------------------------

CUDA_CASES = [
    ("12.4", "12.4", True),
    ("12.1", "12.4", True),
    ("12.4", "12.1", False),
    ("11.8", "12.4", False),
    ("11.8", "11.8", True),
]


def exercise_4() -> None:
    """Decide whether each torch CUDA build matches a driver CUDA version."""
    print("=== Exercise 4 - torch CUDA build vs driver CUDA version ===")
    print("%-14s %-14s %-8s %s" % ("torch CUDA", "driver CUDA", "verdict", "reason"))
    print("-" * 74)
    outcomes = []
    for torch_cuda, driver_cuda, expected in CUDA_CASES:
        ok, reason = compare_cuda(torch_cuda, driver_cuda)
        outcomes.append((torch_cuda, driver_cuda, ok))
        print("%-14s %-14s %-8s %s" % (torch_cuda, driver_cuda, "OK" if ok else "FAIL", reason))
        assert ok is expected, (torch_cuda, driver_cuda, ok)

    failing = [(t, d) for t, d, ok in outcomes if not ok]
    print("command to read the two values:")
    print("   nvidia-smi")
    print('   python -c "import torch; print(torch.version.cuda)"')
    print("mismatching combinations: %d of %d" % (len(failing), len(outcomes)))
    for torch_cuda, driver_cuda in failing:
        print("   rebuild for: uv pip install torch --index-url <cuda%s wheel index>" % driver_cuda)
    assert len(failing) == 2
    print("[OK] exercise_4 - classified 5 torch/driver CUDA combinations")


# --------------------------------------------------------------------------
# Exercise 5 - phase_env_strategy
# --------------------------------------------------------------------------

COURSE_PROJECTS = [
    {"name": "phases/00-setup-and-tooling", "requires": []},
    {"name": "phases/04-neural-networks", "requires": ["torch==2.4.0"]},
    {"name": "phases/05-cnns", "requires": ["torch==2.4.0"]},
    {"name": "phases/08-transformers", "requires": ["torch==2.1.0"]},
    {"name": "phases/11-llm-apis", "requires": ["anthropic>=0.39"]},
]


def exercise_5() -> None:
    """Assign conflicting projects to separate environments."""
    print("=== Exercise 5 - per-phase environment strategy ===")
    print("projects")
    for project in COURSE_PROJECTS:
        requires = ", ".join(project["requires"]) or "(no extra dependency)"
        print("   %-30s %s" % (project["name"], requires))

    environments = plan_environments(COURSE_PROJECTS)
    print("plan: %d environments" % len(environments))
    for env in environments:
        requirements = ", ".join(
            "%s%s" % (name, spec) for name, spec in sorted(env["requirements"].items())
        ) or "shared lightweight base"
        print("   %-12s %-52s %s" % (env["env"], requirements, ", ".join(sorted(env["projects"]))))

    by_env = {env["env"]: sorted(env["projects"]) for env in environments}
    torch_envs = [
        env["env"]
        for env in environments
        if any(name == "torch" for name in env["requirements"])
    ]
    print("environments that hold torch: %s" % ", ".join(sorted(torch_envs)))

    conflicts = find_conflicts(COURSE_PROJECTS)
    print("conflicts detected")
    for name, project_a, spec_a, project_b, spec_b in conflicts:
        print("   %-6s %s needs %s but %s needs %s" % (name, project_a, spec_a, project_b, spec_b))
    print(
        "resolution                   : %d environment groups for %d projects"
        % (len(environments), len(COURSE_PROJECTS))
    )

    assert len(environments) == 4
    assert len(torch_envs) == 2
    assert len(conflicts) == 2
    assert {c[0] for c in conflicts} == {"torch"}
    assert by_env["base (.venv)"] == ["phases/00-setup-and-tooling"]
    assert by_env["env-1"] == ["phases/04-neural-networks", "phases/05-cnns"]
    assert by_env["env-2"] == ["phases/08-transformers"]
    assert by_env["env-3"] == ["phases/11-llm-apis"]
    print("[OK] exercise_5 - split conflicting projects into 4 environments")


# --------------------------------------------------------------------------
# Exercise 6 - env_setup_report
# --------------------------------------------------------------------------

def exercise_6() -> None:
    """Aggregate every check above into one setup report."""
    print("=== Exercise 6 - environment setup report ===")
    parsed = parse_pyproject(PYPROJECT_DEMO)
    good = check_lockfile(PYPROJECT_DEMO, LOCKFILE_GOOD)
    bad = check_lockfile(PYPROJECT_DEMO, LOCKFILE_BAD)
    isolation = env_isolation_check(ENV_A, ENV_B, ENV_B_INSTALLERS)
    cuda_ok, cuda_reason = compare_cuda("12.1", "12.4")
    environments = plan_environments(COURSE_PROJECTS)

    checks = [
        ("manifest pyproject.toml readable", len(parsed["dependencies"]) == 4, "4 base dependencies"),
        ("optional groups declared", len(parsed["optional"]) == 2, "torch, llm"),
        ("lockfile pins every name", good["reproducible"], "%d pinned entries" % good["pinned_count"]),
        (
            "unsafe lockfile detected",
            not bad["reproducible"],
            "%d unpinned, %d missing" % (len(bad["unpinned"]), len(bad["missing"])),
        ),
        ("environment isolation", isolation["isolated"], "no shared package versions to resolve"),
        ("pip/conda mix-up scan", bool(isolation["pip_over_conda"]), "%d pip installs in a conda env" % len(isolation["pip_over_conda"])),
        ("torch CUDA build vs driver", cuda_ok, cuda_reason),
        ("environment plan built", len(environments) == 4, "%d environments for %d projects" % (len(environments), len(COURSE_PROJECTS))),
    ]

    failures = 0
    for label, ok, detail in checks:
        print("   [%s] %-32s %s" % ("PASS" if ok else "FAIL", label, detail))
        if not ok:
            failures += 1

    exit_code = 0 if failures == 0 else 1
    print("checks: %d, failures: %d, exit code: %d" % (len(checks), failures, exit_code))
    assert failures == 0
    assert exit_code == 0
    print("[OK] exercise_6 - setup report passed all 8 checks")


def main() -> int:
    print("Module 06 - Python Environments: offline lab (standard library only)")
    print("")
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
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
