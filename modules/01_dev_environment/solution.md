# Solution — Module 01 (Dev Environment)

ဤဖိုင်ရှိ ရလဒ် တိုင်းသည် အောက်ပါ command ကို repository root မှ တကယ် run ၍ ရသည့် output ဖြစ်သည်။

```bash
$ python3 modules/01_dev_environment/lab.py
$ echo $?
0
```

ကုဒ်အပြည့်အစုံသည် `modules/01_dev_environment/lab.py` တွင် ရှိသည်။ အောက်တွင် exercise တိုင်း၏
ဖြေနည်းနှင့် ထွက်လာသည့် output အပိုင်းကို ဖော်ပြထားသည်။

---

## Exercise 1 — Tool Manifest ကို အနည်းဆုံး Version နှင့် နှိုင်းယှဉ်ခြင်း

**ဖြေနည်း။** `verify.py` ၏ `command_result()` သည် version လိုင်းမှ ဂဏန်း မဟုတ်သည့် အက္ခရာ တိုင်းကို
space အဖြစ် ပြောင်းပြီး ပထမဆုံး ဂဏန်း အုပ်စုကို ယူသည်။ ဤ lab တွင် ထို နည်းလမ်းကို
`parse_version()` အဖြစ် ရေးပြီး `MINIMUM_VERSIONS = {"python": (3, 11), "node": (20,)}` နှင့် နှိုင်းယှဉ်သည်။
Python အတွက် `verify.py` သည် `sys.version_info` အပြည့်ကို စစ်သဖြင့် ဤနေရာတွင်လည်း major+minor ကို
နှိုင်းယှဉ်သည်; Node.js အတွက် `minimum_major=20` အတိုင်း major ကို စစ်သည်။ Manifest နှစ်ခု
(`workstation`၊ `legacy`) ကို သုံး၍ အောင်သည့် လမ်းကြောင်းနှင့် ကျရှုံးသည့် လမ်းကြောင်း နှစ်မျိုးလုံးကို
ပြသည်။

```python
def compare_minimum(version_text: str, minimum: tuple) -> tuple[bool, str]:
    parsed = parse_version(version_text)
    if not parsed:
        return False, f"could not parse a version from {version_text!r}"
    if parsed[: len(minimum)] < minimum:
        wanted = ".".join(str(part) for part in minimum)
        return False, f"found {version_text}; need version {wanted}+"
    return True, f"{version_text} at a detected path"
```

**တကယ် run ရလဒ်။**

```text
[exercise_1] check_toolchain - manifest versus minimum versions
  machine: legacy
    [FAIL] Python 3.11+
           found Python 3.9.6; need version 3.11+
           Fix: Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.
    [PASS] Git
           git version 2.34.1 at /usr/bin/git
    [FAIL] Node.js 20+
           found v18.20.4; need version 20+
           Fix: Run `fnm install 22 && fnm use 22`, then `node --version`.
  machine: workstation
    [PASS] Python 3.11+
           Python 3.12.7 at /home/dev/.local/share/uv/python/bin/python3
    [PASS] Git
           git version 2.43.0 at /usr/bin/git
    [PASS] Node.js 20+
           v22.11.0 at /home/dev/.local/share/fnm/node-versions/v22.11.0/bin/node
    [PASS] npx
           10.9.0 at /home/dev/.local/share/fnm/node-versions/v22.11.0/bin/npx
    [PASS] Rust cargo
           cargo 1.83.0 (5ffbef321 2024-10-29) at /home/dev/.cargo/bin/cargo
[OK] exercise_1 — tool manifest compared against Python 3.11+ and Node.js 20+
```

**ရလဒ် ရှင်းလင်းချက်။** `legacy` machine တွင် Python `3.9.6` နှင့် Node.js `v18.20.4` သည် အနည်းဆုံး
version အောက် ရောက်သဖြင့် `[FAIL]` ဖြစ်ပြီး source ၏ ပြုပြင် command ကို ပြသည်။ `workstation` machine
တွင် entry ၅ ခုလုံး `[PASS]` ဖြစ်သည်။ Function သည်
`workstation → failed=[]`, `legacy → failed=["node", "python"]` ကို ပြန်သဖြင့် assert နှစ်ခု အောင်သည်။

---

## Exercise 2 — Four-Layer Stack ထဲ Component ခွဲခြားခြင်း

**ဖြေနည်း။** အလွှာ တိုင်း၏ အမည်စာရင်းမှ `LAYER_RULES` ကို အစဉ်လိုက် တည်ဆောက်သည်။
`juliaup` ကို `julia` မတိုင်မီ စစ်သဖြင့် package manager အလွှာ (2) သို့ ရောက်သည်; `cargo` သည်လည်း
manager အလွှာတွင် ရှိသည် (source ၏ stack တွင် `cargo` ကို layer 2 တွင် ဖော်ပြသည်)။ Component အမည်ကို
lowercase ပြောင်းပြီး အက္ခရာ/ဂဏန်း မဟုတ်သည့် စာလုံးများကို ဖယ်ကာ keyword နှင့် တိုက်ဆိုင်စစ်သည်။

```python
LAYER_RULES = (
    (2, ("juliaup", "pnpm", "cargo", "uv")),
    (3, ("python", "node", "rust", "julia")),
    (4, ("pytorch", "jax", "transformer", "numpy", "matplotlib", "jupyter")),
    (1, ("driver", "kernel", "shell", "editor", "os", "git")),
)
```

**တကယ် run ရလဒ်။**

```text
[exercise_2] classify_layer - components into the four-layer stack
    [ok] Ubuntu 24.04 (OS)    -> layer 1 System Foundation
    [ok] bash (shell)         -> layer 1 System Foundation
    [ok] git                  -> layer 1 System Foundation
    [ok] VS Code (editor)     -> layer 1 System Foundation
    [ok] NVIDIA (GPU driver)  -> layer 1 System Foundation
    [ok] uv                   -> layer 2 Package Managers
    [ok] pnpm                 -> layer 2 Package Managers
    [ok] cargo                -> layer 2 Package Managers
    [ok] juliaup              -> layer 2 Package Managers
    [ok] Python 3.12          -> layer 3 Language Runtimes
    [ok] Node.js 22           -> layer 3 Language Runtimes
    [ok] Rust                 -> layer 3 Language Runtimes
    [ok] Julia                -> layer 3 Language Runtimes
    [ok] PyTorch              -> layer 4 AI/ML Libraries
    [ok] transformers         -> layer 4 AI/ML Libraries
    [ok] numpy                -> layer 4 AI/ML Libraries
    layer 1 System Foundation: 5 component(s)
    layer 2 Package Managers: 4 component(s)
    layer 3 Language Runtimes: 4 component(s)
    layer 4 AI/ML Libraries: 3 component(s)
    classified: 16/16; unknown: 0
[OK] exercise_2 — 16 components classified into system, packages, runtimes, AI libraries
```

**ရလဒ် ရှင်းလင်းချက်။** Component ၁၆ ခုလုံး တိတိကျကျ ခွဲခြားပြီး `[UNKNOWN]` နှင့် `[MISMATCH]` သုည
ဖြစ်သည်။ အလွှာ အရေအတွက်သည် 5 / 4 / 4 / 3 ဖြစ်သဖြင့် assert များ အောင်သည်။

---

## Exercise 3 — Route တိုင်းအတွက် Probe စာရင်း ထုတ်ခြင်း

**ဖြေနည်း။** `verify.py` ၏ `ROUTES` နှင့် `BASE_OPTIONAL` မှ required/optional စာရင်းကို ကူးယူသည်။
`beginner` သည် `("python", "git")` ကို လိုသည်; `agent-skills` route သည် `("python", "git", "node", "npx")`
ကို လိုသဖြင့် `node` route အတွက် ထို စာရင်းကို သုံးသည်။ `rust` route သည် source ၏ "Use It" ဇယားတွင်
Rust ၏ package manager ဖြစ်သည့် `cargo` ကို လိုသည်။ Probe အမည် အားလုံးသည် `verify.py` ၏ `PROBES`
ဇယားမှ ဖြစ်သည်။

**တကယ် run ရလဒ်။**

```text
[exercise_3] verify_route - probes needed per route
  route: beginner (Beginner course)
    probe          timing     fix if it fails
    Python 3.11+   required   Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.
    Git            required   Run `sudo apt-get update && sudo apt-get install -y git`, then `git --version`.
    Node.js 20+    optional   Run `fnm install 22 && fnm use 22`, then `node --version`.
    npx            optional   Install Node.js 22, then run `npm install -g npm` and `npx --version`.
    NumPy          optional   Activate the course environment and run `python3 -m pip install numpy`.
    Matplotlib     optional   Activate the course environment and run `python3 -m pip install matplotlib`.
    Jupyter        optional   Activate the course environment and run `python3 -m pip install jupyter`.
    PyTorch        optional   Activate the course environment and run `python3 -m pip install torch`.
    Accelerator backend optional   A GPU is optional. Install PyTorch first if you want CUDA or Apple MPS detection.
    Rust cargo     optional   Install Rust with rustup, restart the shell, then run `cargo --version`.
    Julia          optional   Install Julia with juliaup, restart the shell, then run `julia --version`.
    Later checks skipped: 9 tools are not needed to start.
    Next: python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py
  route: node (TypeScript and agents route)
    probe          timing     fix if it fails
    Python 3.11+   required   Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.
    Git            required   Run `sudo apt-get update && sudo apt-get install -y git`, then `git --version`.
    Node.js 20+    required   Run `fnm install 22 && fnm use 22`, then `node --version`.
    npx            required   Install Node.js 22, then run `npm install -g npm` and `npx --version`.
    NumPy          optional   Activate the course environment and run `python3 -m pip install numpy`.
    Matplotlib     optional   Activate the course environment and run `python3 -m pip install matplotlib`.
    Jupyter        optional   Activate the course environment and run `python3 -m pip install jupyter`.
    PyTorch        optional   Activate the course environment and run `python3 -m pip install torch`.
    Accelerator backend optional   A GPU is optional. Install PyTorch first if you want CUDA or Apple MPS detection.
    Rust cargo     optional   Install Rust with rustup, restart the shell, then run `cargo --version`.
    Julia          optional   Install Julia with juliaup, restart the shell, then run `julia --version`.
    Later checks skipped: 7 tools are not needed to start.
    Next: python3 phases/13-tools-and-protocols/06-mcp-fundamentals/code/main.py
  route: rust (Performance-critical systems route)
    probe          timing     fix if it fails
    Python 3.11+   required   Install it with `uv python install 3.12`, activate that environment, and rerun with `python3`.
    Git            required   Run `sudo apt-get update && sudo apt-get install -y git`, then `git --version`.
    Rust cargo     required   Install Rust with rustup, restart the shell, then run `cargo --version`.
    Node.js 20+    optional   Run `fnm install 22 && fnm use 22`, then `node --version`.
    npx            optional   Install Node.js 22, then run `npm install -g npm` and `npx --version`.
    NumPy          optional   Activate the course environment and run `python3 -m pip install numpy`.
    Matplotlib     optional   Activate the course environment and run `python3 -m pip install matplotlib`.
    Jupyter        optional   Activate the course environment and run `python3 -m pip install jupyter`.
    PyTorch        optional   Activate the course environment and run `python3 -m pip install torch`.
    Accelerator backend optional   A GPU is optional. Install PyTorch first if you want CUDA or Apple MPS detection.
    Julia          optional   Install Julia with juliaup, restart the shell, then run `julia --version`.
    Later checks skipped: 8 tools are not needed to start.
    Next: cargo run --release (from the lesson's Rust project root)
[OK] exercise_3 — required and optional probes listed for beginner, node and rust routes
```

**ရလဒ် ရှင်းလင်းချက်။** `beginner` route တွင် required probe ၂ ခု၊ `node` route တွင် ၄ ခု၊ `rust` route တွင်
၃ ခု ဖြစ်သည်။ Source ၏ `main()` အတိုင်း route တိုင်းသည် ရွှေ့ဆိုင်းနိုင်သည့် tool အရေအတွက်ကို
`Later checks skipped:` လိုင်းဖြင့် ပြပြီး နောက် lesson command ကို ဖော်ပြသည်။

---

## Exercise 4 — `.env` ဖိုင်ကို Value မပြဘဲ စစ်ခြင်း

**ဖြေနည်း။** ဖိုင်လိုင်း တိုင်းကို `partition("=")` ဖြင့် ခွဲသည်; အလွတ်လိုင်း၊ `#` လိုင်းနှင့် `=` မပါသည့်
လိုင်းကို ကျော်သည်။ Quote ဖြင့် ခြုံထားသည့် value ၏ quote ကို ဖယ်သည်။ ရလဒ် dict တွင် key ၏
အခြေအနေ (`SET`/`EMPTY`/`MISSING`) ကိုသာ ထည့်သည် — value ကို dict ထဲ လုံးဝ မထည့်ရ။

**တကယ် run ရလဒ်။**

```text
[exercise_4] read_env_file - key presence without printing values
    keys in file: 4
    [SET    ] ANTHROPIC_API_KEY    (from file; value hidden)
    [EMPTY  ] OPENAI_API_KEY       (from file; value hidden)
    [SET    ] HF_TOKEN             (from file; value hidden)
    [OPTIONAL] HF_HOME              (from file; value hidden)
    ready keys: 2/3
[OK] exercise_4 — .env parsed; keys reported as SET, EMPTY or MISSING with values hidden
```

**ရလဒ် ရှင်းလင်းချက်။** `OPENAI_API_KEY` သည် ဖိုင်တွင် ရှိသော်လည်း value အလွတ် ဖြစ်သဖြင့် `EMPTY`
ဖြစ်သည်; `ANTHROPIC_API_KEY` နှင့် `HF_TOKEN` သည် `SET` ဖြစ်သည် (double quote ဖြင့် ခြုံထားသည့်
`HF_TOKEN` ၏ quote ကို ဖယ်ပြီး စစ်သည်)။ `HF_HOME` သည် required မဟုတ်သဖြင့် `[OPTIONAL]` ဖြစ်သည်။
Output ထဲတွင် secret value တစ်လုံးမျှ မပေါ်ပါ။

---

## Exercise 5 — ပထမဆုံး Test Tensor Operation

**ဖြေနည်း။** `MiniTensor` သည် row စာရင်းကို သိမ်းပြီး `shape` ကို တွက်သည်; `matmul()` တွင် အတွင်း
dimension ကို စစ်ပြီး column များကို `zip(*other.rows)` ဖြင့် ဖြန့်ကာ row-by-column ကိန်းစဉ် တွက်သည်။
dtype ကို `torch.float32` အဖြစ် သတ်မှတ်သည်။

```python
def matmul(self, other: "MiniTensor") -> "MiniTensor":
    if self.shape[1] != other.shape[0]:
        raise ValueError(f"matmul shape mismatch: {self.shape} @ {other.shape}")
    columns = list(zip(*other.rows))
    out = [[sum(a * b for a, b in zip(row, column)) for column in columns] for row in self.rows]
    return MiniTensor(out, dtype=self.dtype)
```

**တကယ် run ရလဒ်။**

```text
[exercise_5] tensor_probe - first test tensor operation
    a: shape=(2, 3) dtype=torch.float32
    b: shape=(3, 2) dtype=torch.float32
    a @ b: shape=(2, 2) dtype=torch.float32
    a @ b row 0: [58.0, 64.0]
    numpy step 2 sample: vector=[1.0, 2.0, 3.0] dot with itself=14.0
    CUDA available: False
    MPS available:  False
    accelerator: CPU only; a GPU is optional for the starting lessons
[OK] exercise_5 — matmul shape and dtype checked; CPU-only backend confirmed
```

**ရလဒ် ရှင်းလင်းချက်။** `(2, 3)` နှင့် `(3, 2)` ၏ matmul သည် `(2, 2)` ကို ပေးသည်; ပထမဆုံး row သည်
`[58.0, 64.0]` ဖြစ်သည်။ Source ၏ Step 2 snippet အတိုင်း `[1, 2, 3]` ၏ dot product သည် `14.0` ဖြစ်သည်။
CUDA နှင့် MPS နှစ်မျိုးလုံး `False` ဖြစ်သဖြင့် source ၏
`CPU only; a GPU is optional for the starting lessons` လိုင်း ထွက်သည်။

---

## Exercise 6 — စစ်ဆေးချက် စုစည်းချက် နှင့် Exit Code

**ဖြေနည်း။** Exercise ၁–၅ ၏ ရလဒ်များကို စစ်ဆေးချက် ၆ တန်းအဖြစ် စုစည်းပြီး route ၏ required probe များ
အားလုံး အောင်ခြင်းကို `passed == total` ဖြင့် ဆုံးဖြတ်သည်။ `verify.py` ၏ `main()` အတိုင်း
`Result: {passed}/{total} required checks passed` ကို print ပြီး အောင်ပါက `0` ကို ပြန်သည်။

**တကယ် run ရလဒ်။**

```text
[exercise_6] setup_report - aggregated status and exit code
    check                    status  detail
    toolchain (workstation)  PASS    5/5 tools at or above minimum
    toolchain (legacy)       LATER   old Node.js; fix before lessons that need Node
    four-layer stack         PASS    16 components placed in 4 layers
    route probes             PASS    2/2 required probes pass
    env keys                 FAIL    2/3 required keys set
    tensor probe             PASS    matmul shape=(2, 2) dtype=torch.float32 backend=CPU only; a GPU is optional for the starting lessons
    Result: 2/2 required checks passed
    Ready to start Beginner course.
    Next: python3 phases/01-math-foundations/01-linear-algebra-intuition/code/vectors.py
[OK] exercise_6 — every probe aggregated; exit code decided as 0
```

**ရလဒ် ရှင်းလင်းချက်။** `legacy` machine နှင့် `.env` key တစ်ခုသည် ဤ route အတွက် ပိတ်ဆို့သည့်
အချက် မဟုတ်သဖြင့် `LATER`/`FAIL` အဖြစ် မှတ်ထားပြီး required check နှစ်ခု အောင်သဖြင့် exit code
`0` ဖြစ်သည်။

**ဖိုင် တစ်ခုလုံး၏ နောက်ဆုံး လိုင်းများ။**

```text
========================================================================
[PASS] All 6/6 exercises passed successfully.
========================================================================
```

Shell မှ ပြန်သည့် exit code — `0`။
