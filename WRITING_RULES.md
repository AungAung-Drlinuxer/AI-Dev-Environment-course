# Course Writing Rules — AI Development Environment

ဤဖိုင်သည် ဤ course ၏ အရေးအသား စည်းမျဉ်း ဖြစ်သည်။ chapter တိုင်း မရေးမီ ဤဖိုင်ကို ဖတ်ရမည်။

## ၁. ဘာသာစကား နှင့် register

- စာသည် **မြန်မာဘာသာ** ဖြစ်သည်။ Code၊ command၊ flag၊ file path၊ identifier၊ version အားလုံးကို English အတိုင်း ထားရမည်။
- Technical term များကို English အတိုင်း ထားရမည် — gateway, provider, endpoint, virtual environment, container,
  image, layer, volume, dataset, split, batch, token, dtype, shape, checkpoint, lockfile, runtime, driver, VRAM။
  မြန်မာလို တိုက်ရိုက် ဘာသာပြန်၍ technical အဓိပ္ပာယ် ပျက်စီးစေခြင်းကို ခွင့်မပြုပါ။
- **Formal written register** ကို သုံးရမည် — `သည်` / `ပါသည်` / `ရမည်` / `ဖြစ်သည်`။ Genitive တွင် `၏` ကို သုံးရမည်။
- မသုံးရ — `ပါတယ်`၊ `ပါဘူး`၊ `ရမယ်`၊ `ဖြစ်တယ်`၊ `တဲ့`၊ `နဲ့`၊ `ဖို့`၊ `ရဲ့`၊ `နော်`၊ `ပေါ့`၊ `လို့`၊ `ဆိုတာ`၊ `ဒီ` (ဤနေရာတွင် ပြသည့်အနေဖြင့်)။
  လိုအပ်သည့်နေရာတွင် `ဤ` / `ထို` ကို သုံးရမည်။
- ဂဏန်း ၄ နှင့် ၉ ကို သီးခြားအသုံးပြုသည့်အခါ "၄ ခု" ကဲ့သို့ space ဖြင့် ရေးရမည်။
- Emoji၊ အခြားဘာသာစကား အက္ခရာ (တရုတ်၊ ဂျပန်၊ ကိုရီးယား၊ Devanagari)၊ ideographic/fullwidth punctuation
  (`、`၊ `。`၊ `，`) ကို လုံးဝ မသုံးရ။ မြန်မာ ပုဒ်ကြောင်း `။` နှင့် `၊` ကို သုံးရမည်။

## ၂. Chapter တစ်ခု၏ တည်ဆောက်ပုံ

problem → core concept → technique comparison（table） → practical configuration（command + လုပ်ဆောင်ချက်） →
operational cautions → self-check（မေးခွန်း ၃–၅ ခု + အတိုချုပ် အဖြေ）။
Heading များကို ထပ်တူ မဖြစ်စေရ — "ဘာလဲ / ဘာကြောင့်လဲ / ဘယ်လိုလဲ" သုံးခုကို subsection တိုင်း ထပ်ခြင်း မပြုရ။

- အခန်းတိုင်း အရှည် — အနည်းဆုံး **၅၀၀၀ လုံး (characters)**၊ အမြင့်ဆုံး ကန့်သတ်ချက် မရှိ။ (byte မဟုတ်၊ character ဖြင့် တိုင်းသည်။)
- ဖတ်သူသည် ဤ course ကို ပထမဆုံး လုပ်သည့် engineer ဖြစ်သည် — command တိုင်း၏ လုပ်ဆောင်ချက်ကို တစ်လိုင်းစီ ရှင်းပြရမည်။
- work instruction ပုံစံ — "ဤ command သည် X ကို လုပ်သည်၊ ရလဒ်သည် Y ဖြစ်သည်၊ မအောင်မြင်ပါက Z ကို စစ်ပါ။"

## ၃. Figure များ

- Module တိုင်းတွင် **Mermaid** figure ၂ ခုမှ ၄ ခုအထိ (`flowchart TD/LR` သို့မဟုတ် `sequenceDiagram`) ထည့်ရမည်။
  အခြား diagram အမျိုးအစား မသုံးရ။ node အရေအတွက် ~၁၅ ခုအထိ။ label များကို quote လုပ်ရမည်။
- Figure တိုင်းကို "Figure N — <ခေါင်းစဉ်>" ဖြင့် နံပါတ်တပ်၍ caption တပ်ရမည်၊ နှင့် figure ပြီးတိုင်း
  **ပုံရှင်းလင်းချက် (Figure N)** ဟူသော အဆင့်လိုက် ရှင်းလင်းချက်（၃–၆ လိုင်း）ကို ပေးရမည်။
- Third-party image များ embed လုပ်ခြင်း မပြုရ — figure အားလုံးသည် ဤ course ကိုယ်တိုင် ရေးသည်။

## ၄. File တစ်ခုစီ၏ တာဝန်

- `README.md` — module ၏ ရည်ရွယ်ချက်၊ လိုအပ်ချက်（prerequisite）၊ subtopic စာရင်း၊ exercise တစ်လိုင်းချင်း၊ ဖိုင်စာရင်း။
- `explanation.md` — အဓိက သင်ခန်းစာ။ ဤစည်းမျဉ်း အားလုံးကို လိုက်နာရမည်။
- `exercise.md` — exercise ၆ ခု၊ `## Exercise N — <ခေါင်းစဉ်>` format。 တစ်ခုစီတွင် လိုအပ်ချက်၊ လုပ်ရမည့်အဆင့်၊ အောင်မြင်မှုကို စစ်သည့် နည်းလမ်း ပါရမည်။
- `solution.md` — exercise ၆ ခုစီ၏ အဖြေ။ Code ကို တကယ် run ၍ ရလဒ်ကို ကူးထည့်ရမည်။ Hand-computed value မရေးရ။
- `lab.py` — exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ပြီး `assert` ဖြင့် စစ်သည်။ Standard library သာ။

## ၅. Technical accuracy

- Version၊ command၊ flag၊ package အမည်တိုင်းကို **source（`MODULE_SPEC.md` ရှိ source လမ်းကြောင်း）နှင့် တိုက်ဆိုင်စစ်ရမည်**။
- Source တွင် မပါသော version နှင့် benchmark ကို မတီးရ။ မှန်ကန်ကြောင်း မစစ်နိုင်ပါက "version အလိုက် ပြန်စစ်ရန် လိုသည်" ဟု ရေးရမည်။
- `README.md` တွင် ဤစာသား ပါရမည် — "command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။"
- Source ၏ fact ကို ဖော်ပြသည့်အခါ source ၏ အနေအထားအတိုင်း ဖော်ပြရမည် — ပိုကောင်းအောင် ပြင်ခြင်း မပြုရ။
  ပြင်လိုက်ပါက `## Technical review notes` တွင် အကြောင်းပြချက်နှင့်တကွ မှတ်ရမည်။

## ၆. Beginner walkthrough register（ဤ register အတွက် ခြွင်းချက်）

`modules/<module>/walkthroughs/NN_<exercise_slug>.md` ဖိုင်များသည် အထက်ပါ "အခြေခံသဘောတရား မရှင်းပြရ" အစဉ်အလာမှ
**ကင်းလွတ်သည်**။ ထိုဖိုင်များတွင် Python အခြေခံ（dictionary၊ tuple၊ dataclass၊ comprehension၊ generator၊ `sorted`，
`with`，`try/except`）ကို အစမှ ရှင်းပြရမည်။ ထို register အတွက် snippet တိုင်း run နိုင်ရမည်၊ documented output တိုင်း
တကယ် run ရလဒ် ဖြစ်ရမည်၊ နှင့် အဆုံးတွင် run နိုင်သည့် assembled script တစ်ခု ပါရမည်။

## ၇. Lab စည်းမျဉ်း

- Standard library သာ — third-party import မရ။ Network၊ Docker၊ GPU၊ dataset download မလိုရ။
- Deterministic — `random` မသုံးရ (`random.Random(seed)` ကဲ့သို့ seeded generator ကို ခွင့်ပြုသည်)။ Set ကို print လုပ်ပါက `sorted()` ဖြင့်။
- `python3 modules/<folder>/lab.py` → exit 0။ exercise တိုင်း ပြီးစီးသည့်အခါ `[OK] exercise_N — <အတိုချုပ်>` ဟူသော လိုင်းကို print ရမည် (runner သည် ဤလိုင်းကို ရေတွက်သည်)၊ နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.`
- Exercise တိုင်း၏ output ကို လူဖတ်နိုင်သော လိုင်းများဖြင့် ပြရမည် — assert သာ မဟုတ်ရ။
