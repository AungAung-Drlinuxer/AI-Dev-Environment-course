# Module 07 — Docker for AI

## ရည်ရွယ်ချက်

ဤ module သည် AI ပရောဂျက်များအတွက် ပြန်လည် ထုတ်လုပ်နိုင်သည့် (reproducible) container
ပတ်ဝန်းကျင် တည်ဆောက်ခြင်းကို သင်ပေးသည်။ သင်ခန်းစာ အဆုံးတွင် —

- CUDA၊ PyTorch နှင့် AI library များ ပါဝင်သည့် GPU-enabled Docker image ကို
  Dockerfile မှ build လုပ်နိုင်မည်။
- လုပ်ငန်း code၊ model နှင့် dataset များကို volume အဖြစ် mount လုပ်၍ container ပြန်
  build လုပ်သည့်အခါများတွင်ပါ ထိန်းသိမ်းနိုင်မည်။
- NVIDIA Container Toolkit ဖြင့် container အတွင်း GPU ကို ဖော်ထုတ်နိုင်မည်။
- inference service နှင့် vector database ပါသည့် multi-service stack ကို Docker Compose
  ဖြင့် စီမံနိုင်မည်၊ service အမည်ဖြင့် container ချင်း ဆက်သွယ်နိုင်မည်။

## လိုအပ်ချက် (Prerequisites)

| အချက် | အသေးစိတ် |
|---|---|
| ပြီးဆုံးထားရန် | Module 01 (Dev Environment) နှင့် Module 03 (GPU Setup & Cloud) |
| Docker | Docker Engine သို့မဟုတ် Docker Desktop (`docker --version` ဖြင့် စစ်နိုင်သည်) |
| GPU (မဖြစ်မနေ မဟုတ်) | NVIDIA GPU ရှိပါက Linux တွင် NVIDIA Container Toolkit လိုသည်၊ မရှိပါက `--gpus all` ဖယ်ပြီး CPU ဖြင့် လုပ်နိုင်သည် |
| ခန့်မှန်းချိန် | ~60 မိနစ် (ပထမ build တွင် CUDA base image ဒေါင်းလုပ်ချရသဖြင့် အချိန်ပို ကြာနိုင်သည်) |

Command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official
documentation ကို စစ်ပါ။ ဤ module ရှိ image tag၊ port နှင့် service အမည်အားလုံးသည်
သင်ခန်းစာ (source) မှ ယူထားသည်။

## Subtopic စာရင်း

1. Why AI projects need Docker more than most
2. Key vocabulary
3. Common container patterns in AI
4. Step 1: Install Docker
5. Step 2: Install NVIDIA Container Toolkit (Linux with NVIDIA GPU)
6. Step 3: Understand base images
7. Step 4: Write a Dockerfile for AI development
8. Step 5: Volume mounts for data and models
9. Step 6: Docker Compose for multi-service AI apps
10. Step 7: Useful Docker commands for AI work
11. No GPU?

## Exercise တစ်လိုင်းချင်း

| # | Exercise | အနှစ်ချုပ် |
|---|---|---|
| 1 | `parse_dockerfile` | Dockerfile ကို instruction စာရင်း၊ base image နှင့် layer အရေအတွက် အဖြစ် ဖတ်ခြင်း |
| 2 | `devel_vs_runtime` | devel နှင့် runtime base image ၏ အရွယ်အစားနှင့် tooling ကွာခြားချက် ဇယား |
| 3 | `docker_run_command` | `--gpus`၊ volume mount နှင့် port mapping ပါသော `docker run` command ကို spec မှ တည်ဆောက်ခြင်း |
| 4 | `parse_compose` | compose ဖိုင်မှ service၊ `depends_on` နှင့် အတွင်းပိုင်း endpoint ကို ဖတ်ခြင်း |
| 5 | `container_reachability` | AI container မှ Qdrant သို့ `http://qdrant:6333/collections` ရောက်/မရောက် စစ်ခြင်း |
| 6 | `image_report` | image အရွယ်အစားနှင့် layer အစီရင်ခံစာ |

## ဖိုင်စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise စာရင်း၊ ဖိုင်စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — figure ၃ ခု၊ နှိုင်းယှဉ်ချက် ဇယား၊ လက်တွေ့ ပြင်ဆင်ခြင်း၊ သတိပြုရန် ချက်များ၊ self-check |
| `exercise.md` | exercise ၆ ခု၏ လိုအပ်ချက်၊ အဆင့်များနှင့် အောင်မြင်မှု စစ်နည်း |
| `solution.md` | exercise ၆ ခုစီ၏ အဖြေ နှင့် `lab.py` ၏ တကယ့် run ရလဒ် |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်သည်၊ standard library သာ |
| `Dockerfile.example` | သင်ခန်းစာ၏ GPU-enabled Dockerfile (source မှ မိတ္တူ)၊ repository ရှိ `docker-compose.yml` မှ ကိုးကားသည် |

## Lab ကို run ခြင်း

```bash
python3 modules/07_docker_for_ai/lab.py
```

`lab.py` သည် Docker daemon၊ network နှင့် GPU မလိုပါ။ Dockerfile နှင့် compose ဖိုင်၏
အကြောင်းအရာကို parse လုပ်ပြီး ရလဒ်ကို စာဖြင့် ပြသည်။ နောက်ဆုံးလိုင်းတွင်
`[PASS] All 6/6 exercises passed successfully.` ပေါ်ပါက အောင်မြင်သည်။
