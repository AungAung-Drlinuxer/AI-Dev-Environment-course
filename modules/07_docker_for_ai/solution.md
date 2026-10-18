# Module 07 — Solution

## ဤ အဖြေများ မည်သို့ ထုတ်ခဲ့သည်

ဤ စက်တွင် **Docker မရှိပါ** (`docker` command မရနိုင်ပါ)။ ထို့ကြောင့်
`docker build`၊ `docker run` နှင့် `docker compose up` တို့၏ တကယ့် output ကို
မပြသနိုင်ပါ။ မရှိသည့် output ကို လုပ်ကြံ မရေးထားပါ။

ထို အစား ဤ exercise များ၏ ရလဒ်ကို **ကိုယ်တိုင် run ခဲ့သည့် code** မှ ပြသည်။
`lab.py` သည် သင်ခန်းစာ၏ Dockerfile နှင့် compose ဖိုင်၏ အကြောင်းအရာကို embed
လုပ်ထားပြီး parse လုပ်သည်၊ ထို့ကြောင့် output တိုင်းသည် ဖိုင်များမှ တွက်ချက်ထားသည့်
တကယ့် ရလဒ် ဖြစ်သည်။

Run ခဲ့သည့် command နှင့် ရလဒ် —

```
$ cd /home/aungaung/Documents/AI-Dev-Environment-course
$ python3 modules/07_docker_for_ai/lab.py
...
[PASS] All 6/6 exercises passed successfully.
$ echo $?
0
```

အောက်တွင် exercise တစ်ခုစီ၏ အဖြေ နှင့် ၎င်း၏ တကယ့် output အပိုင်းကို ဖော်ပြသည်။

---

## Exercise 1 — `parse_dockerfile`

**အဖြေ။** Dockerfile ကို first-token အလိုက် `(INSTRUCTION, arguments)` tuple အဖြစ်
ခွဲသည်။ Line continuation ကို မပေါင်းပါက `RUN` တစ်ခုတည်းကို လိုင်းများစွာ အဖြစ်
မှားယွင်း ရေတွက်မည် ဖြစ်သဖြင့် `\` ဖြင့် ဆက်ထားသည့် လိုင်းများကို အရင် ပေါင်းသည်။
`FROM` ၏ argument ထဲမှ `--platform=linux/amd64` ကို ဖယ်၍ base image ကို ရယူသည်။
Layer အရေအတွက်သည် `FROM` နောက်ပိုင်း instruction အရေအတွက် ဖြစ်သည်။

**တကယ့် output။**

```
instruction စုစုပေါင်း : 13
  [ 1] FROM     --platform=linux/amd64 nvidia/cuda:12.4.1-devel-ubuntu2...
  [ 2] ENV      DEBIAN_FRONTEND=noninteractive
  [ 3] ENV      PYTHONUNBUFFERED=1
  [ 4] RUN      apt-get update && apt-get install -y --no-install-recom...
  [ 5] RUN      update-alternatives --install /usr/bin/python python /u...
  [ 6] RUN      curl -sSL https://raw.githubusercontent.com/pypa/get-pi...
  [ 7] RUN      python -m pip install --no-cache-dir --upgrade pip setu...
  [ 8] RUN      python -m pip install --no-cache-dir      torch==2.6.0+...
  [ 9] RUN      python -m pip install --no-cache-dir      numpy      pa...
  [10] WORKDIR  /workspace
  [11] VOLUME   ["/workspace", "/models"]
  [12] EXPOSE   8888
  [13] CMD      ["python"]

base image          : nvidia/cuda:12.4.1-devel-ubuntu22.04
platform            : linux/amd64
RUN instruction     : 6 ခု
layer အရေအတွက်      : 12 ခု (FROM နောက်ပိုင်း instruction တိုင်း layer တစ်ခု)
```

---

## Exercise 2 — `devel_vs_runtime`

**အဖြေ။** Base image လေးမျိုးကို သင်ခန်းစာတွင် ဖော်ပြသည့် အရွယ်အစားနှင့် အသုံးပြုရမည့်
နေရာ အလိုက် ဇယားဖြင့် ပြသည်။ `devel` တွင် compiler ပါပြီး `runtime` တွင် မပါသဖြင့်
build အဆင့်တွင်သာ `devel` လိုသည်။ ကွာခြားချက်သည် 4096 − 1536 = 2560 MB ဖြစ်သည်။

**တကယ့် output။**

```
image                                          size       compiler    
----------------------------------------------------------------------
nvidia/cuda:12.4.1-devel-ubuntu22.04           ~4 GB      ပါသည်       
nvidia/cuda:12.4.1-runtime-ubuntu22.04         ~1.5 GB    မပါ         
pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime  ~6 GB      မပါ         
python:3.12-slim                               ~150 MB    မပါ         

devel (~4 GB) မှ runtime (~1.5 GB) သို့ ပြောင်းလျှင်
  လျော့နည်းသည့် ပမာဏ : 2560 MB (2.5 GB ခန့်)
  ဆုံးရှုံးသည့် အရာ  : nvcc compiler နှင့် CUDA header များ (build အဆင့်တွင်သာ လိုသည်)
  သတိပြုရန်       : အရွယ်အစားသည် သင်ခန်းစာတွင် ဖော်ပြထားသည့် ခန့်မှန်းတန်ဖိုး ဖြစ်သည်၊
                    မိမိ image ၏ တိကျသည့် အရွယ်ကို `docker images` ဖြင့် တိုင်းရမည်။
```

**မှတ်ချက်။** သင်ခန်းစာတွင် ဖော်ပြထားသည့် `~4 GB` နှင့် `~1.5 GB` သည်
ခန့်မှန်းတန်ဖိုး ဖြစ်သည်။ ဤ lab သည် ထို တန်ဖိုးများကို အသုံးပြုပြီး ကွာခြားချက်ကို
တွက်သည်၊ တကယ့် image အရွယ်ကို `docker images` ဖြင့် တိုင်းရမည်။

---

## Exercise 3 — `docker_run_command`

**အဖြေ။** Spec dictionary မှ flag များကို အစဉ်လိုက် ဆက်စပ်သည်။

**တကယ့် output။**

```
spec —
  image         : ai-dev
  gpus          : all
  volumes       : $(pwd):/workspace, ~/models:/models, ~/datasets:/data
  ports         : 8888:8888
  command       : python -c "import torch; print(torch.__version__)"

တည်ဆောက်သည့် command —
  docker run --rm -it --gpus all -v $(pwd):/workspace -v ~/models:/models -v ~/datasets:/data -p 8888:8888 ai-dev python -c "import torch; print(torch.__version__)"

flag တစ်ခုချင်း၏ လုပ်ဆောင်ချက် —
  --rm                 : container ရပ်သည့်အခါ ဖျက်ပစ်သည်
  -it                  : interactive terminal ဖွင့်သည်
  --gpus all           : NVIDIA Container Toolkit မှ host GPU အားလုံးကို ဖော်ထုတ်သည်
  -v host:container    : host directory ကို container အတွင်း mount လုပ်သည်
  -p 8888:8888         : host port 8888 ကို container port 8888 သို့ ချိတ်သည်

GPU မရှိသည့် စက်အတွက် (`--gpus all` ဖယ်သည့်အခါ) —
  docker run --rm -it -v $(pwd):/workspace -v ~/models:/models -v ~/datasets:/data -p 8888:8888 ai-dev python -c "import torch; print(torch.__version__)"
```

ဤ command သည် သင်ခန်းစာ၏ `docker run --rm -it --gpus all -v $(pwd):/workspace
-v ~/models:/models ai-dev python -c "..."` ပုံစံနှင့် တူညီသည်။ ကွာခြားချက်မှာ
dataset mount တစ်ခု ထပ်ပါလာခြင်း ဖြစ်ပြီး ၎င်းသည် သင်ခန်းစာ၏ Step 5 တွင်
ဖော်ပြထားသည့် `-v ~/datasets:/data` ဖြစ်သည်။

**Docker မရှိသည့်အတွက် ဤ command ကို တကယ် run နိုင်ခြင်း မရှိပါ** — ထို့ကြောင့် ရလဒ်ကို
command line အဆင့်တွင်သာ ပြထားသည်။ ဤ command အတွက် မျှော်မှန်းရသည့် output သည်
သင်ခန်းစာ hint တွင် ဖော်ပြသည့်အတိုင်း `2.6.0` ဖြင့် စသည့် version လိုင်း ဖြစ်သည်။

---

## Exercise 4 — `parse_compose`

**အဖြေ။** Compose ဖိုင်ကို YAML subset parser ဖြင့် ဖတ်သည်။ Indentation အလိုက်
mapping/list ခွဲပြီး `depends_on` မှ service များအကြား မှီခိုမှုကို ရယူသည်။
ထိုနောက် topological order ဖြင့် စတင်ရန် အစဉ်လိုက်ကို ထုတ်သည်။

**တကယ့် output။**

```
သင်ခန်းစာ၏ docker-compose.yml — service 2 ခု
  ai-dev   | build: Dockerfile
           | ports      : 8888:8888
           | volumes    : ../../../:/workspace, ~/models:/models, ~/datasets:/data
           | depends_on : -
  qdrant   | image: qdrant/qdrant:v1.12.5
           | ports      : 6333:6333, 6334:6334
           | volumes    : qdrant_data:/qdrant/storage
           | depends_on : -
  စတင်ရန် အစဉ်လိုက် : ai-dev -> qdrant

ဤ repository ၏ docker-compose.yml — service 2 ခု
  qdrant   | image: qdrant/qdrant:latest
           | ports      : 6333:6333, 6334:6334
           | volumes    : qdrant_storage:/qdrant/storage
           | depends_on : -
  ai-dev   | build: modules/07_docker_for_ai/Dockerfile.example
           | ports      : -
           | volumes    : ./:/workspace, aidev_cache:/root/.cache
           | depends_on : qdrant
           | env        : QDRANT_URL=http://qdrant:6333
  စတင်ရန် အစဉ်လိုက် : qdrant -> ai-dev
```

**ရှင်းလင်းချက်။** သင်ခန်းစာ၏ ဖိုင်တွင် `depends_on` မပါသဖြင့် အစဉ်လိုက်သည်
ဖိုင်ထဲတွင် ပေါ်သည့် အစဉ်အတိုင်း (`ai-dev -> qdrant`) ဖြစ်ပြီး service နှစ်ခုသည်
တစ်ပြိုင်နက် စတင်သည်။ ဤ repository ၏ ဖိုင်တွင် `ai-dev` သည် `qdrant` ကို
မှီသဖြင့် qdrant အရင် စတင်သည်။ ထို ဖိုင်သည် `Dockerfile.example` ကို
ကိုးကားသဖြင့် ဤ module ၏ Dockerfile ကို အသုံးပြုသည်။

---

## Exercise 5 — `container_reachability`

**အဖြေ။** စစ်ဆေးချက် သုံးမျိုး —

1. Service name ဖြင့် — Compose သည် default network တစ်ခု ဖန်တီးပြီး service အမည်ကို
   hostname အဖြစ် မှတ်ပုံတင်သဖြင့် `http://qdrant:6333` ရောက်နိုင်သည်။
2. Host မှ — `6333:6333` port mapping ရှိသဖြင့် host မှ `http://localhost:6333`
   ရောက်နိုင်သည်။
3. Container အတွင်းမှ `localhost` — မရောက်နိုင်ပါ၊ အကြောင်းမှာ container အတွင်း
   `localhost` သည် ထို container ကိုယ်တိုင်ကို ညွှန်သောကြောင့် ဖြစ်သည်။

**တကယ့် output။**

```
စစ်ဆေးချက် ၁ — service name ဖြင့် ဆက်သွယ်ခြင်း
  URL      : http://qdrant:6333/collections
  ရောက်နိုင်မှု : ရောက်နိုင်သည်
  - service နှစ်ခုစလုံးသည် Compose ဖန်တီးသည့် default network တွင် ပါဝင်သည်
  - target ၏ container port 6333 သည် ရရှိနိုင်သည် (6333, 6334)

  တူညီသည့် စစ်ဆေးမှုကို မရှိသည့် service အမည်ဖြင့် ပြန်လုပ်ခြင်း —
  service 'postgres' — ရောက်နိုင်မှု : မရောက်နိုင်ပါ
  - service 'postgres' သည် compose ဖိုင်တွင် မရှိပါ

စစ်ဆေးချက် ၂ — host မှ published port ဖြင့် ဆက်သွယ်ခြင်း
  host port mapping : 6333:6333, 6334:6334
  host မှ URL        : http://localhost:6333/collections
  ရလဒ်              : host အတွက် ရောက်နိုင်သည် (port 6333 ကို publish လုပ်ထားသည်)

စစ်ဆေးချက် ၃ — container အတွင်းမှ `localhost` သုံးခြင်း (လွဲမှားသည့် နည်းလမ်း)
  URL      : http://localhost:6333/collections
  ရလဒ်      : မရောက်နိုင်ပါ — container အတွင်း `localhost` သည် qdrant မဟုတ်ဘဲ
             client container ကိုယ်တိုင်ကို ညွှန်သည်။ service name ကို သုံးရမည်။
```

**မှတ်ချက်။** ဤ စစ်ဆေးချက်သည် compose ဖိုင်၏ အကြောင်းအရာမှ တွက်ချက်သည့်
ရလဒ် ဖြစ်သည် — တကယ့် HTTP request မပို့ပါ။ သင်ခန်းစာ hint တွင် ဖော်ပြသည့်
`docker compose exec ai-dev bash` နှင့် `curl http://qdrant:6333/collections` ကို
Docker ရှိသည့် စက်တွင် run ပါက JSON ပြန်လာမည် ဖြစ်သည်။

---

## Exercise 6 — `image_report`

**အဖြေ။** Parse လုပ်ထားသည့် instruction များမှ image ၏ metadata ကို စုစည်းသည်။
Package စာရင်းကို `RUN` လိုင်းများထဲမှ `pip install` ပါသည့် လိုင်းများမှ ထုတ်ပြီး
`==` ပါသည့် အရာကို pin လုပ်ထားသည့် အုပ်စုတွင် ထည့်သည်။

**တကယ့် output။**

```
IMAGE REPORT — ai-dev
  base image        : nvidia/cuda:12.4.1-devel-ubuntu22.04
  platform          : linux/amd64
  instruction       : 13 ခု
  layer             : 12 ခု (base layer အပေါ် ထပ်သည့် layer)
  Python            : 3.12 (deadsnakes PPA မှ တင်သည်)
  WORKDIR           : /workspace
  EXPOSE            : 8888 (Jupyter)
  VOLUME            : /workspace, /models
  CMD               : ["python"]
  pinned package    : torch==2.6.0+cu124, torchvision==0.21.0+cu124, torchaudio==2.6.0+cu124
  unpinned package  : setuptools, wheel, numpy, pandas, scikit-learn, matplotlib, jupyter, transformers, datasets, accelerate, safetensors
  layer အမျိုးအစား    : CMD x 1, ENV x 2, EXPOSE x 1, FROM x 1, RUN x 6, VOLUME x 1, WORKDIR x 1

  base layer အရွယ်   : devel ~4 GB / runtime ~1.5 GB
  ကွာခြားချက်        : 2560 MB (2.5 GB)
  သတိပြုရန်          : image တစ်ခုလုံး၏ တိကျသည့် အရွယ်ကို သင်ခန်းစာတွင် မဖော်ပြထားပါ၊
                      build ပြီးနောက် `docker images ai-dev` ဖြင့် တိုင်းရမည်။
  layer ပြန်သုံးခြင်း  : မပြောင်းသည့် layer များကို cache မှ ပြန်သုံးသဖြင့် ဒုတိယ build သည် လျင်မြန်သည်။
```

**သင်ခန်းစာ exercise 4 နှင့် ချိတ်ဆက်ချက်။** သင်ခန်းစာတွင် `docker images` ဖြင့်
အရွယ်အစားကို မှတ်ပြီး `devel` မှ `runtime` သို့ ပြောင်း၍ နှိုင်းယှဉ်ရန် လိုသည်။
Docker မရှိသည့် ဤ ပတ်ဝန်းကျင်တွင် ထို တိုင်းတာမှုကို မလုပ်နိုင်သဖြင့် ဤ အစီရင်ခံစာသည်
သင်ခန်းစာတွင် ဖော်ပြထားသည့် base layer အရွယ်အစား (~4 GB / ~1.5 GB) နှင့်
layer အရေအတွက်ကို ပြသည်။ Build ပြီးနောက် `docker images ai-dev` ဖြင့် တကယ့်
အရွယ်အစားကို ရယူရမည်။
