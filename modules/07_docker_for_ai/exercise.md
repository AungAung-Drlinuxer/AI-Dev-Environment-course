# Module 07 — Exercise

ဤ exercise ၆ ခုကို `lab.py` တွင် `def exercise_1()` မှ `def exercise_6()` အထိ
implement လုပ်ထားသည်။ Exercise တိုင်းသည် **standard library သာ** အသုံးပြုပြီး
Docker daemon၊ network နှင့် GPU မလိုဘဲ run နိုင်သည်။ အဖြေများကို
`solution.md` တွင် ကြည့်ပါ။

---

## Exercise 1 — `parse_dockerfile`

**လိုအပ်ချက်။** သင်ခန်းစာ၏ Dockerfile ကို instruction စာရင်း အဖြစ် parse လုပ်ပြီး
base image၊ platform၊ `RUN` instruction အရေအတွက်နှင့် layer အရေအတွက်ကို ဖော်ပြရမည်။

**လုပ်ရမည့် အဆင့်။**

1. Line continuation (`\`) ဖြင့် ဆက်ထားသည့် လိုင်းများကို လိုင်းတစ်လိုင်း အဖြစ်
   ပေါင်းပါ။ Comment နှင့် လိုင်းလွတ် ကို ဖယ်ပါ။
2. လိုင်းတိုင်းကို `INSTRUCTION` နှင့် `arguments` အဖြစ် ခွဲပါ။
3. `FROM` ၏ argument မှ `--platform=...` flag ကို ခွဲထုတ်၍ base image အမည်ကို ရယူပါ။
4. `FROM` နောက်ပိုင်း instruction တိုင်းသည် layer တစ်ခု ဖန်တီးသည်ဟု သတ်မှတ်၍
   layer အရေအတွက် ရေတွက်ပါ (`FROM` ကိုယ်တိုင် base layer ဖြစ်သဖြင့် မရေတွက်ပါ)။

**အောင်မြင်မှု စစ်နည်း။** Instruction အရေအတွက် ၁၃ ခု၊ layer ၁၂ ခု၊ `RUN` ၆ ခု
ဖြစ်ရမည်။ Base image သည် `nvidia/cuda:12.4.1-devel-ubuntu22.04` ဖြစ်ရမည်။
`EXPOSE` ၏ တန်ဖိုးသည် `8888`၊ `WORKDIR` သည် `/workspace` ဖြစ်ရမည်။

---

## Exercise 2 — `devel_vs_runtime`

**လိုအပ်ချက်။** သင်ခန်းစာတွင် ဖော်ပြသည့် base image လေးမျိုးကို အရွယ်အစား၊
tooling နှင့် အသုံးပြုရမည့် နေရာ အလိုက် ဇယားဖြင့် နှိုင်းယှဉ်ပြရမည်။ `devel` မှ
`runtime` သို့ ပြောင်းလျှင် မည်မျှ သက်သာသည်၊ မည်သည့် အရာ ဆုံးရှုံးသည်ကို
တွက်ချက်ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. Base image တစ်ခုစီ၏ အမည်၊ အခန်းကဏ္ဍ၊ အသုံးပြုရမည့် နေရာ၊ အရွယ်အစားနှင့်
   compiler ပါ/မပါ ကို data အဖြစ် သတ်မှတ်ပါ။
2. အရွယ်အစား ဇယားကို column လိုက် print လုပ်ပါ။
3. `devel` နှင့် `runtime` ၏ ကွာခြားချက်ကို MB နှင့် GB ဖြင့် တွက်ပါ။
4. အရွယ်အစားသည် ခန့်မှန်းတန်ဖိုး ဖြစ်ကြောင်း နှင့် တိကျသည့် တန်ဖိုးကို
   `docker images` ဖြင့် တိုင်းရမည် ဖြစ်ကြောင်း မှတ်ချက်ရေးပါ။

**အောင်မြင်မှု စစ်နည်း။** ဇယားတွင် image ၄ ခု ပါရမည်။ ကွာခြားချက်သည် 2560 MB
(2.5 GB ခန့်) ဖြစ်ရမည်။ `devel` တွင် compiler ပါပြီး `runtime` တွင် မပါကြောင်း
စစ်ရမည်။

---

## Exercise 3 — `docker_run_command`

**လိုအပ်ချက်။** GPU flag၊ volume mount သုံးခုနှင့် port mapping ပါသော
`docker run` command line ကို spec (dictionary) မှ တည်ဆောက်ရမည်။ ထိုနောက်
GPU မရှိသည့် စက်အတွက် `--gpus all` ဖယ်ထားသည့် ဗားရှင်းကို ထုတ်ပြရမည်။

**လုပ်ရမည့် အဆင့်။**

1. Spec တွင် `image`၊ `gpus`၊ `interactive`၊ `rm`၊ `volumes`၊ `ports` နှင့်
   `command` ကို ထည့်ပါ။ Volume တစ်ခုစီတွင် host နှင့် container path ရှိရမည်။
2. Flag များကို အစဉ်လိုက် ဆက်စပ်၍ command line တစ်လိုင်း တည်ဆောက်ပါ —
   `docker run --rm -it --gpus all -v host:container ... -p host:container image command`။
3. Flag တစ်ခုချင်း၏ လုပ်ဆောင်ချက်ကို ရှင်းပြပါ။
4. `gpus` ကို ဖယ်ထားသည့် spec ဖြင့် ဒုတိယ command ကို ထုတ်ပါ။

**အောင်မြင်မှု စစ်နည်း။** ရလဒ်သည် အောက်ပါ လိုင်းနှင့် ကွက်တိ တူညီရမည်။

```
docker run --rm -it --gpus all -v $(pwd):/workspace -v ~/models:/models -v ~/datasets:/data -p 8888:8888 ai-dev python -c "import torch; print(torch.__version__)"
```

GPU မပါသည့် ဗားရှင်းတွင် `--gpus` မပါရမည်။

---

## Exercise 4 — `parse_compose`

**လိုအပ်ချက်။** Docker Compose ဖိုင်ကို parse လုပ်၍ service စာရင်း၊ service တစ်ခုစီ၏
image သို့မဟုတ် build၊ port၊ volume၊ `depends_on` နှင့် `environment` endpoint ကို
ဖော်ပြရမည်။ ထိုနောက် `depends_on` ကို လိုက်နာသည့် စတင်ရန် အစဉ်လိုက်ကို ထုတ်ရမည်။

**လုပ်ရမည့် အဆင့်။**

1. YAML ၏ လိုအပ်သည့် အပိုင်းကို ဖတ်နိုင်သည့် parser ရေးပါ — indentation ဖြင့်
   mapping နှင့် list ကို ခွဲသည်၊ `- key: value` နှင့် `key: value` နှစ်မျိုးကို
   ကိုင်တွယ်သည်၊ `[a, b]` flow list နှင့် quote လုပ်ထားသည့် scalar ကို ဖတ်သည်။
2. သင်ခန်းစာ၏ compose ဖိုင်နှင့် ဤ repository ၏ compose ဖိုင် နှစ်ခုစလုံးကို parse
   လုပ်ပြီး service တစ်ခုစီ၏ အချက်အလက်ကို print ပါ။
3. `depends_on` ကို topological order အဖြစ် ပြောင်း၍ `A -> B` ပုံစံဖြင့် ပြပါ။
4. Endpoint ကို `environment` မှ ရှာ၍ ပြပါ — ဤ repository တွင်
   `QDRANT_URL=http://qdrant:6333` ဖြစ်သည်။

**အောင်မြင်မှု စစ်နည်း။** သင်ခန်းစာ ဖိုင်တွင် service နှစ်ခု (`ai-dev`၊ `qdrant`) နှင့်
`qdrant/qdrant:v1.12.5` image ပေါ်လာရမည်။ Repository ဖိုင်တွင် `ai-dev` ၏
`depends_on` သည် `qdrant` ဖြစ်ရမည်၊ စတင်ရန် အစဉ်လိုက်သည် `qdrant -> ai-dev` ဖြစ်ရမည်။

---

## Exercise 5 — `container_reachability`

**လိုအပ်ချက်။** AI container သည် vector database ကို service အမည်ဖြင့်
ရောက်နိုင်ကြောင်း စစ်ရမည်။ ရောက်နိုင်သည့် အခြေအနေ သုံးမျိုးကို ခွဲခြားပြရမည် —
service name ဖြင့်၊ host ၏ published port ဖြင့်၊ container အတွင်းမှ `localhost` ဖြင့်။

**လုပ်ရမည့် အဆင့်။**

1. Parse လုပ်ထားသည့် compose dict မှ client service နှင့် target service ကို ရွေးပါ။
2. Target service ရှိ/မရှိ၊ service နှစ်ခုသည် default network တွင် ပါ/မပါ၊ target ၏
   container port သည် လိုအပ်သည့် port နှင့် ကိုက်/မကိုက် ကို စစ်ပါ။
3. ဖြေရှင်းရမည့် URL ကို `http://<service>:<port><path>` ပုံစံဖြင့် တည်ဆောက်ပါ။
4. မရှိသည့် service အမည်ဖြင့် စစ်ကြည့်ပြီး ကျရှုံးသည့် အခြေအနေကို ပြပါ။

**အောင်မြင်မှု စစ်နည်း။** `http://qdrant:6333/collections` အတွက် ရလဒ်သည်
"ရောက်နိုင်သည်" ဖြစ်ရမည်။ မရှိသည့် service အတွက် "မရောက်နိုင်ပါ" ဖြစ်ရမည်။
Container အတွင်းမှ `localhost:6333` သည် မရောက်နိုင်ကြောင်း ရှင်းပြရမည်။

---

## Exercise 6 — `image_report`

**လိုအပ်ချက်။** Dockerfile မှ image တစ်ခု၏ အစီရင်ခံစာ ထုတ်ရမည် — base image၊
platform၊ instruction နှင့် layer အရေအတွက်၊ `WORKDIR`၊ `EXPOSE`၊ `VOLUME`၊ `CMD`၊
တင်ထားသည့် package များ (pin လုပ်ထားသည့် အုပ်စုနှင့် မလုပ်ထားသည့် အုပ်စု)။

**လုပ်ရမည့် အဆင့်။**

1. Parse လုပ်ထားသည့် instruction စာရင်းမှ `WORKDIR`၊ `EXPOSE`၊ `VOLUME`၊ `CMD` ကို
   ရယူပါ။
2. `RUN` instruction များထဲမှ `pip install` လိုင်းများကို ရှာ၍ flag မဟုတ်သည့်
   token များကို package အဖြစ် ခွဲထုတ်ပါ (`==` ပါသည့် အရာကို pin လုပ်ထားသည်
   အုပ်စုတွင် ထည့်ပါ)။
3. Layer အမျိုးအစား အလိုက် အရေအတွက်ကို စုစည်းပြပါ။
4. Base layer အရွယ်အစားနှင့် `devel` မှ `runtime` သို့ ပြောင်းလျှင် သက်သာမည့်
   ပမာဏကို ဖော်ပြပါ။ Image အပြည့်၏ အရွယ်အစားကို သင်ခန်းစာတွင် မဖော်ပြထားသဖြင့်
   တန်ဖိုးတစ်ခုကို မတီးဘဲ `docker images ai-dev` ဖြင့် တိုင်းရန် ညွှန်ပါ။

**အောင်မြင်မှု စစ်နည်း။** အစီရင်ခံစာတွင် layer ၁၂ ခု၊ `EXPOSE 8888`၊
`VOLUME /workspace, /models`၊ pin လုပ်ထားသည့် package အဖြစ်
`torch==2.6.0+cu124`၊ `torchvision==0.21.0+cu124`၊ `torchaudio==2.6.0+cu124`
ပေါ်လာရမည်။ `transformers` နှင့် `safetensors` သည် pin မလုပ်ထားသည့် အုပ်စုတွင်
ပါရမည်။

---

## Run လုပ်ခြင်း

```bash
python3 modules/07_docker_for_ai/lab.py
```

Exit code သည် 0 ဖြစ်ရမည်၊ နောက်ဆုံးလိုင်းတွင်
`[PASS] All 6/6 exercises passed successfully.` ပေါ်ရမည်။
