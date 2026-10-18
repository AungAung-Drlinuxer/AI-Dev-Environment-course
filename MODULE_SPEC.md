# Module Spec — AI Development Environment (Phase 00)

ဤဖိုင်သည် ဤ course ၏ **load-bearing spec** ဖြစ်သည်။ စာရေးသူ (လူ သို့မဟုတ် agent) တိုင်းသည် `WRITING_RULES.md` ပြီးနောက်
မိမိ module ၏ အပိုင်းကို ဤဖိုင်မှ ဖတ်ရမည်။ ဤနေရာတွင် ဖော်ပြထားသည့် subtopic နှင့် lab exercise ၆ ခုသည် မဖြစ်မနေ ပါရမည်။

## Source (ground truth)

| အချက် | တန်ဖိုး |
|---|---|
| Repository | `rohitg00/ai-engineering-from-scratch` (MIT) |
| Phase folder | `phases/00-setup-and-tooling/` |
| Lesson document | `phases/00-setup-and-tooling/<slug>/docs/en.md` |
| Lesson web page | `https://aiengineeringfromscratch.com/lesson?path=phases/00-setup-and-tooling/<slug>` |
| Lesson extras | `<slug>/code/`, `<slug>/quiz.json`, `<slug>/outputs/` |
| Captured copies | `~/.hermes/profiles/ai-engineer/cache/scratch/aidev/raw/<slug>__en.md`, `.../raw/code/` |

Source သည် **၁၃ ခု** သော lesson ရှိသည် (01–13)။ အသုံးပြုသူ ပေးခဲ့သည့် စာရင်းတွင် 12 အထိ ပါပြီး၊ 13 ခုမြောက်
`13-python-for-ai-engineering` ကို ဤ course တွင် ထည့်ထားသည်။

### Rules for every module

1. Subtopic အားလုံးကို ဖုံးလွှမ်းရမည် — source ၏ အစဉ်အတိုင်း။
2. Command, version, image tag, package name — **source တွင် ပါသည့်အတိုင်း** ရေးရမည်။ မပါသော version ကို မတီးရ။
3. Version-dependent ဖြစ်သည့် အချက်ကို "version အလိုက် ပြန်စစ်ရန် လိုသည်" ဟု မှတ်ရမည်။
4. `lab.py` သည် **Python standard library သာ** သုံးရမည်။ တတိယပါတီ package၊ network၊ GPU၊ Docker မလိုရ။
5. Lab သည် deterministic ဖြစ်ရမည် (`random` မသုံးရ — module 13 တွင် seeded `random.Random(seed)` ကို ခွင့်ပြုသည်)။
6. `python3 modules/<folder>/lab.py` သည် exit code 0 ဖြင့် ပြီးရမည်၊ `[PASS] All 6/6 exercises passed successfully.` ဟု ပြရမည်။

## Module 01 — Dev Environment

- **Folder:** `modules/01_dev_environment/`
- **Source:** `phases/00-setup-and-tooling/01-dev-environment/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F01-dev-environment
- **Type / Languages / Time:** Build · Python, Node.js, Rust · ~45 min
- **အနှစ်ချုပ်:** Set up Python 3.11+, Node.js 20+ and Rust from scratch; understand the four-layer stack and verify GPU access.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: System Foundation
- Step 2: Python with uv
- Step 3: Node.js with pnpm
- Step 4: Rust
- Step 5: Julia (Optional)
- Step 6: GPU Setup (If You Have One)
- Step 7: Verify the route you want to start

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `check_toolchain` — a tool manifest ကို အနည်းဆုံး version (Python 3.11, Node.js 20) နှင့် နှိုင်းယှဉ်စစ်ခြင်း
2. `classify_layer` — component တစ်ခုစီကို four-layer stack (system, packages, runtimes, AI libraries) ထဲ ခွဲခြားခြင်း
3. `verify_route` — beginner / node / rust route တစ်ခုစီအတွက် လိုအပ်သော probe စာရင်း ထုတ်ခြင်း
4. `read_env_file` — `.env` ကို parse လုပ်ပြီး key ရှိ/မရှိကို value မပြဘဲ စစ်ခြင်း
5. `tensor_probe` — torch ၏ test tensor operation ကို pure Python ဖြင့် တုပပြီး shape/dtype ကို စစ်ခြင်း
6. `setup_report` — probe အားလုံး၏ အခြေအနေ စုစည်းချက် နှင့် exit code ကို ဆုံးဖြတ်ခြင်း

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 02 — Git & Collaboration

- **Folder:** `modules/02_git_and_collaboration/`
- **Source:** `phases/00-setup-and-tooling/02-git-and-collaboration/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F02-git-and-collaboration
- **Type / Languages / Time:** Build · — · ~30 min
- **အနှစ်ချုပ်:** Configure git identity and use the daily add, commit, push workflow with branches for experiments.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Configure git
- Step 2: The daily workflow
- Step 3: Branching for experiments
- Step 4: Working with this course repo

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_git_config` — `user.name` / `user.email` ကို parse လုပ်ပြီး identity ပြည့်စုံခြင်းကို စစ်ခြင်း
2. `build_gitignore` — `.pt`, `.pth`, `.safetensors` checkpoint များကို ဖုံးလွှမ်းသော `.gitignore` တည်ဆောက်ခြင်း
3. `commit_workflow` — add → commit → push လုပ်ငန်းစဉ်ကို state machine အဖြစ် တုပခြင်း
4. `branch_experiment` — branch ဖန်တီး၊ merge လုပ်၍ conflict ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း
5. `read_log` — `git log --oneline` output ကို parse လုပ်ပြီး အနှစ်ချုပ် ထုတ်ခြင်း
6. `status_report` — untracked / modified / staged ကို ခွဲထုတ်ပြီး push ရန် အဆင်သင့် ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 03 — GPU Setup & Cloud

- **Folder:** `modules/03_gpu_setup_and_cloud/`
- **Source:** `phases/00-setup-and-tooling/03-gpu-setup-and-cloud/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F03-gpu-setup-and-cloud
- **Type / Languages / Time:** Build · Python · ~40 min
- **အနှစ်ချုပ်:** Verify local GPU availability with nvidia-smi and PyTorch's CUDA API; benchmark CPU against GPU.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Option 1: Local NVIDIA GPU
- Option 2: Google Colab
- Option 3: Cloud GPU
- No GPU? No problem.
- Build It: GPU vs CPU benchmark

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_nvidia_smi` — `nvidia-smi` ဇယား output မှ GPU အမည်၊ total memory၊ driver version ကို ဖတ်ခြင်း
2. `fp16_model_fit` — parameter တစ်ခုလျှင် ၂ byte ဆိုသော rule of thumb ဖြင့် အနီးစပ်ဆုံး အနိမ့်ဆုံး model အရွယ်ကို တွက်ခြင်း
3. `benchmark_matmul` — CPU matmul ကို pure Python ဖြင့် အတိအကျ တွက်ပြီး အချိန်ကို တိုင်းခြင်း
4. `speedup_line` — CPU နှင့် GPU အချိန်မှ speedup ကို တွက်ပြီး ဖော်မတ်ချခြင်း
5. `cloud_decision` — local GPU ရှိ/မရှိ၊ VRAM ပမာဏအလိုက် local သို့မဟုတ် cloud route ကို ဆုံးဖြတ်ခြင်း
6. `gpu_report` — device အချက်အလက်၊ fit ခန့်မှန်းချက် နှင့် အကြံပြုချက် စုစည်းချက်

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 04 — APIs & Keys

- **Folder:** `modules/04_apis_and_keys/`
- **Source:** `phases/00-setup-and-tooling/04-apis-and-keys/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F04-apis-and-keys
- **Type / Languages / Time:** Build · Python · ~30 min
- **အနှစ်ချုပ်:** Store API keys securely in environment variables and .env files; call an LLM API through an SDK and raw HTTP.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Store API keys safely
- Step 2: First API call (Python)
- Step 3: First API call (TypeScript)
- Step 4: Raw HTTP (no SDK)

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `load_dotenv` — `.env` ဖိုင်ကို parse လုပ်ပြီး secret များကို မပြဘဲ key အမည်စာရင်း ထုတ်ခြင်း
2. `mask_secret` — key ကို ပြသင့်သည့် အနည်းဆုံး အပိုင်းသာ ပြသော masked preview
3. `build_messages_payload` — Anthropic messages payload ကို dict အဖြစ် တည်ဆောက်ခြင်း
4. `parse_response` — documented response shape မှ text နှင့် token usage ကို ထုတ်ခြင်း
5. `classify_api_error` — 401 / 429 / 5xx ကို လုပ်ဆောင်ရမည့် အပြုအမူ (stop / backoff-retry) အဖြစ် ခွဲခြားခြင်း
6. `api_call_report` — offline ဖြင့် ခေါ်ဆိုမှု တစ်ခုလုံးကို တုပပြီး အစီရင်ခံစာ ထုတ်ခြင်း

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 05 — Jupyter Notebooks

- **Folder:** `modules/05_jupyter_notebooks/`
- **Source:** `phases/00-setup-and-tooling/05-jupyter-notebooks/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F05-jupyter-notebooks
- **Type / Languages / Time:** Build · Python · ~30 min
- **အနှစ်ချုပ်:** Install and launch JupyterLab; use magic commands to benchmark and visualise inline.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Pick your interface
- Step 2: Keyboard shortcuts that matter
- Step 3: Cell types
- Step 4: Magic commands
- Step 5: Display rich output inline
- Step 6: Google Colab
- Notebooks vs Scripts: When to use which
- Common traps
- Further Reading

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `read_notebook` — `.ipynb` JSON ကို parse လုပ်ပြီး cell အရေအတွက်၊ အမျိုးအစား ခွဲခြင်း
2. `execution_order_check` — `execution_count` အစဉ်မမှန်ခြင်း (out-of-order run) ကို ဖမ်းခြင်း
3. `hidden_state_scan` — restart & run all လုပ်လျှင် ကျရှုံးမည့် cell ကို variable မှီခိုမှုမှ ခန့်မှန်းခြင်း
4. `timeit_compare` — list comprehension နှင့် pure Python နည်းလမ်း နှစ်ခုကို တူညီသော အလုပ်အတွက် တိုင်းတာခြင်း
5. `notebook_or_script` — အလုပ် အမျိုးအစားအလိုက် notebook / script ကို ဆုံးဖြတ်ခြင်း
6. `notebook_health_report` — trap စစ်ဆေးချက် စုစည်းချက်

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 06 — Python Environments

- **Folder:** `modules/06_python_environments/`
- **Source:** `phases/00-setup-and-tooling/06-python-environments/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F06-python-environments
- **Type / Languages / Time:** Build · Python · ~35 min
- **အနှစ်ချုပ်:** Create isolated environments with uv, venv or conda and write a pyproject.toml with lockfiles.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Option 1: uv venv (Recommended)
- Option 2: venv (Built-in)
- Option 3: conda (When You Need It)
- For This Course: Per-Phase Strategy
- pyproject.toml Basics
- Lockfiles
- Common Mistakes
- 1. Installing globally
- 2. Mixing pip and conda
- 3. Forgetting to activate
- 4. Committing .venv to git
- 5. CUDA version mismatch

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_pyproject` — `pyproject.toml` မှ dependency နှင့် optional group များကို ဖတ်ခြင်း
2. `check_lockfile` — lockfile ရှိ pinned version များ ပြည့်စုံ/မပြည့်စုံ စစ်ခြင်း
3. `env_isolation_check` — environment နှစ်ခု၏ package စာရင်းကို နှိုင်းယှဉ်ပြီး ရောနှောမှုကို ဖမ်းခြင်း
4. `torch_cuda_matrix` — torch ၏ CUDA build နှင့် driver/CUDA version တိုက်ဆိုင်မှုကို ဆုံးဖြတ်ခြင်း
5. `phase_env_strategy` — ဆန့်ကျင်ဘက် dependency ရှိသော project များကို environment များသို့ ခွဲခြားခြင်း
6. `env_setup_report` — စစ်ဆေးချက် အားလုံး၏ အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 07 — Docker for AI

- **Folder:** `modules/07_docker_for_ai/`
- **Source:** `phases/00-setup-and-tooling/07-docker-for-ai/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F07-docker-for-ai
- **Type / Languages / Time:** Build · Docker · ~60 min
- **အနှစ်ချုပ်:** Build a GPU-enabled Docker image with CUDA, PyTorch and AI libraries; run a multi-service stack with Compose.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Why AI projects need Docker more than most
- Key vocabulary
- Common container patterns in AI
- Step 1: Install Docker
- Step 2: Install NVIDIA Container Toolkit (Linux with NVIDIA GPU)
- Step 3: Understand base images
- Step 4: Write a Dockerfile for AI development
- Step 5: Volume mounts for data and models
- Step 6: Docker Compose for multi-service AI apps
- Step 7: Useful Docker commands for AI work
- No GPU?

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_dockerfile` — instruction စာရင်း၊ base image နှင့် layer အရေအတွက် ကို ဖတ်ခြင်း
2. `devel_vs_runtime` — base image ရွေးချယ်မှု၏ အရွယ်အစား နှင့် tooling ကွာခြားချက် ဇယား
3. `docker_run_command` — `--gpus`၊ volume နှင့် port mapping ပါသော run command ကို spec မှ တည်ဆောက်ခြင်း
4. `parse_compose` — service၊ `depends_on` နှင့် အတွင်းပိုင်း endpoint ကို ဖတ်ခြင်း
5. `container_reachability` — AI container မှ Qdrant သို့ `http://qdrant:6333/collections` ရောက်/မရောက် စစ်ခြင်း
6. `image_report` — image အရွယ်အစား နှင့် layer အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 08 — Editor Setup

- **Folder:** `modules/08_editor_setup/`
- **Source:** `phases/00-setup-and-tooling/08-editor-setup/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F08-editor-setup
- **Type / Languages / Time:** Build · — · ~20 min
- **အနှစ်ချုပ်:** Install VS Code with essential extensions and configure format-on-save, type checking and Remote SSH.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Install VS Code
- Step 2: Install Essential Extensions
- Step 3: Configure Settings
- Step 4: Terminal Integration
- Step 5: Remote Development (SSH into GPU Boxes)
- Alternatives
- Cursor
- Windsurf
- Vim/Neovim

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_settings` — VS Code `settings.json` မှ key များကို စစ်ဆေးခြင်း
2. `extension_diff` — လိုအပ်သော extension နှင့် `code --list-extensions` output ကို နှိုင်းယှဉ်ခြင်း
3. `ssh_config_entry` — Remote SSH အတွက် host entry တည်ဆောက်ခြင်း
4. `format_on_save_policy` — language အလိုက် format-on-save မူဝါဒ ဆုံးဖြတ်ခြင်း
5. `editor_choice_matrix` — VS Code / Cursor / Windsurf / Neovim ကို လိုအပ်ချက်အလိုက် ရွေးချယ်ခြင်း
6. `editor_report` — setup စစ်ဆေးချက် အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 09 — Data Management

- **Folder:** `modules/09_data_management/`
- **Source:** `phases/00-setup-and-tooling/09-data-management/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F09-data-management
- **Type / Languages / Time:** Build · Python · ~45 min
- **အနှစ်ချုပ်:** Load, stream and cache datasets with the Hugging Face datasets library; convert between formats.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Install the datasets library
- Step 2: Load a dataset
- Step 3: Stream large datasets
- Step 4: Dataset formats
- Step 5: Data splits
- Step 6: Download and cache models
- Step 7: Handle large files
- Step 8: Storage patterns
- Datasets Used in This Course

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `load_csv_records` — CSV ဖိုင်ကို record စာရင်း အဖြစ် ဖတ်ခြင်း
2. `stream_vs_load` — generator နှင့် အပြည့်ဖတ်ခြင်း၏ peak memory ကို `tracemalloc` ဖြင့် နှိုင်းယှဉ်ခြင်း
3. `split_dataset` — seed သတ်မှတ်ပြီး 70/15/15 split ခွဲခြင်း
4. `format_tradeoffs` — CSV / JSON / Parquet / Arrow ကို ရွေးချယ်ခြင်း
5. `large_file_policy` — checkpoint/data အတွက် `.gitignore` / Git LFS / DVC ကို ဆုံးဖြတ်ခြင်း
6. `dataset_report` — dataset အချက်အလက် အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 10 — Terminal & Shell

- **Folder:** `modules/10_terminal_and_shell/`
- **Source:** `phases/00-setup-and-tooling/10-terminal-and-shell/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F10-terminal-and-shell
- **Type / Languages / Time:** Learn · — · ~35 min
- **အနှစ်ချုပ်:** Use piping, redirects and grep to filter training logs; run persistent tmux sessions to watch a GPU.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Step 1: Know your shell
- Step 2: Piping and redirects
- Step 3: Background processes
- Step 4: tmux
- Step 5: Monitoring with htop and nvtop
- Step 6: SSH for remote GPU boxes
- Step 7: Useful aliases for AI work
- Step 8: Common AI terminal patterns

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `parse_training_log` — epoch/loss လိုင်းများကို parse လုပ်ခြင်း
2. `filter_lines` — grep semantics ဖြင့် စစ်ထုတ်ခြင်း
3. `run_pipeline` — pipe နှင့် redirect လုပ်ငန်းစဉ်ကို အဆင့်လိုက် ချိတ်ခြင်း
4. `loss_statistics` — tail နှင့် စာရင်းအင်းဖြင့် loss ကို အနှစ်ချုပ်ခြင်း
5. `tmux_plan` — pane များအတွက် tmux command စာရင်း တည်ဆောက်ခြင်း
6. `log_ops_report` — လုပ်ငန်းစဉ် အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 11 — Linux for AI

- **Folder:** `modules/11_linux_for_ai/`
- **Source:** `phases/00-setup-and-tooling/11-linux-for-ai/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F11-linux-for-ai
- **Type / Languages / Time:** Learn · — · ~30 min
- **အနှစ်ချုပ်:** Navigate the Linux file system, manage permissions with chmod and chown, and install packages with apt.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- File System Layout
- Essential Commands
- Moving Around
- Files and Directories
- Reading Files
- Searching
- Permissions
- Package Management (apt)
- Users and sudo
- Processes and systemd
- Disk Space
- Networking
- tmux: Keep Sessions Alive
- WSL2 for Windows Users
- Gotchas: macOS to Linux
- Quick Reference Card

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `permission_bits` — symbolic နှင့် octal mode ကို အပြန်အလှန် ပြောင်းခြင်း
2. `diagnose_permission_denied` — `ls -la` မှ owner/permission အခြေအနေကို ရှာဖွေခြင်း
3. `disk_report` — `df -h` နှင့် `du -sh` output ကို parse လုပ်ခြင်း
4. `apt_install_plan` — GPU box အသစ်အတွက် package စာရင်း နှင့် အစဉ်လိုက် အစီအစဉ်
5. `macos_vs_linux` — macOS နှင့် Linux ကွာခြားချက် နှင့် ကျရှုံးမှု အဖြစ်များသည့် နေရာ
6. `linux_ops_report` — စစ်ဆေးချက် အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 12 — Debugging & Profiling

- **Folder:** `modules/12_debugging_and_profiling/`
- **Source:** `phases/00-setup-and-tooling/12-debugging-and-profiling/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F12-debugging-and-profiling
- **Type / Languages / Time:** Build · Python · ~45 min
- **အနှစ်ချုပ်:** Use conditional breakpoint() and debug_print to inspect tensor shapes, dtypes and NaN values; profile training loops.

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- Part 1: Print Debugging (Yes, It Works)
- Part 2: Python Debugger (pdb and breakpoint)
- Part 3: Python Logging
- Part 4: Timing Code Sections
- Part 5: cProfile and line_profiler
- Part 6: Memory Profiling
- Part 7: Common AI Bugs and How to Catch Them
- Part 8: TensorBoard Basics
- Part 9: VS Code Debugger

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `debug_print` — shape/dtype/NaN ကို ကြည့်ရှုသည့် helper
2. `nan_detector` — forward pass တွင် သုညဖြင့် စားခြင်းမှ ဖြစ်သော NaN ကို ဖမ်းခြင်း
3. `check_shapes` — matmul shape မတိုက်ဆိုင်ခြင်းကို ကြိုတင် ဖမ်းခြင်း
4. `profile_hotspot` — cProfile-style stats မှ အချိန်အများဆုံး function ကို ရှာခြင်း
5. `memory_hotspot` — `tracemalloc` snapshot မှ အများဆုံး allocate လုပ်သည့် နေရာကို ရှာခြင်း
6. `training_health_report` — loss curve မှ overfit ဖြစ်/မဖြစ် ဆုံးဖြတ်ခြင်း

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

## Module 13 — Python for AI Engineering

- **Folder:** `modules/13_python_for_ai_engineering/`
- **Source:** `phases/00-setup-and-tooling/13-python-for-ai-engineering/docs/en.md`
- **Web:** https://aiengineeringfromscratch.com/lesson?path=phases%2F00-setup-and-tooling%2F13-python-for-ai-engineering
- **Type / Languages / Time:** Build · Python · ~120 min
- **အနှစ်ချုပ်:** Most code in this course uses the same small set of Python idioms. Learn that set here, before the math and
  model lessons depend on it.
- **Time note:** source တွင် ~120 min (module 13 ခုအနက် အရှည်ဆုံး lesson)

### Must cover (source ၏ subtopic အစဉ်အတိုင်း)

- What the course code uses
- Names refer to objects
- A list holds pointers, an array holds numbers
- A list holds every item, a generator holds one
- The Idioms You Need
- 1. Values, collections, and unpacking
- 2. Comprehensions
- 3. Functions, arguments, and closures
- 4. Classes and dataclasses
- 5. Iterators and generators
- 6. Context managers and exceptions
- 7. Type hints, modules, and the main guard
- 8. Files, JSON, CSV, and sorting
- 9. Counting, grouping, and iterator tools
- 10. Why loops over numbers are slow
- Step 1: A record type and a dataset loader
- Step 2: A seeded train and test split
- Step 3: A mini-batch generator
- Step 4: Vector math and a standardizer
- Step 5: A complete run
- Step 6: Measure speed and memory
- The standard library versions
- The same math with compiled arrays
- Broadcasting
- Further Reading

### Lab exercises (၆ ခု — `def exercise_N()` တစ်ခုစီ)

1. `Record` နှင့် `load_records` — dataclass နှင့် CSV loader
2. `train_test_split` — seed သတ်မှတ်ပြီး split ခွဲခြင်း
3. `minibatch` — mini-batch generator
4. `vecmath` — dot product၊ mean နှင့် standardizer
5. `silent_bugs` — shared list၊ mutable default နှင့် used-up generator သုံးမျိုးကို သရုပ်ပြပြီး ဖမ်းခြင်း
6. `run_demo` — အချိန်နှင့် memory တိုင်းတာချက် အစီရင်ခံစာ

### Facts to keep exact

- ဤ module ၏ command/flag/version အားလုံးကို `../../README.md` နှင့် `explanation.md` တွင် source အတိုင်း ဖော်ပြရမည်။

