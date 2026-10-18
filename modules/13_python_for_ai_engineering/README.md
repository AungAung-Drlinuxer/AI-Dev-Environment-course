# Module 13 — Python for AI Engineering

> ဤ phase ၏ နောက်ဆုံး module ဖြစ်သည်။ သင်္ချာ နှင့် model သင်ခန်းစာများ မစမီ Python idiom အနည်းငယ်ကို ကျွမ်းကျင်ထားရမည်။

**Type:** Build · **Language:** Python · **Time:** ~120 min · **Source lesson:** `phases/00-setup-and-tooling/13-python-for-ai-engineering`

## ရည်ရွယ်ချက်

ဤ module ပြီးဆုံးသည့်အခါ ဖတ်ရှုသူသည် အောက်ပါ အရာများကို လုပ်နိုင်ရမည် —

- course code အများစု သုံးသည့် idiom များကို ဖတ်နိုင်၊ ရေးနိုင်ခြင်း — unpacking၊ f-string၊ comprehension၊ dataclass၊ generator၊ `with`၊ type hint
- **error မတက်ဘဲ ရလဒ် မှားစေသည့်** အမှား သုံးမျိုးကို ရှာဖွေနိုင်ခြင်း — share လုပ်ထားသည့် list၊ mutable default argument၊ ကုန်သွားသည့် generator
- standard library သာ ဖြင့် CSV loader၊ seed ပါသည့် split နှင့် mini-batch generator တည်ဆောက်ခြင်း
- pure Python ဖြင့် dot product၊ mean နှင့် standard deviation ရေးပြီး အချိန် နှင့် memory ကို တိုင်းတာခြင်း
- ဂဏန်းအပေါ် pure Python loop သည် ဘာကြောင့် နှေးသည်ကို ရှင်းပြပြီး NumPy broadcasting က ထို loop ကို compiled code ထဲ မည်သို့ ရွှေ့သည်ကို ရှင်းလင်းခြင်း

## လိုအပ်ချက် (Prerequisites)

- Module 01 (Dev Environment) — Python 3.11+ နှင့် terminal အခြေခံ
- Module 06 (Python Environments) — virtual environment ဖန်တီးခြင်း
- Python အခြေခံ — variable၊ function၊ list၊ dict၊ `for` loop
- ဤ module ၏ lab ကို run ရန် **network မလိုပါ**၊ **package တစ်ခုမျှ install လုပ်ရန် မလိုပါ**။ Lab သည် Python standard library သာ သုံးသည်။
- Lab ရှိ `dataclass`၊ `random.Random(seed)`၊ `itertools.islice`၊ `tracemalloc` တို့ကို မဖတ်ဖူးသေးပါက အဆင်ပါသည် — `solution.md` တွင် တစ်လိုင်းချင်း ရှင်းပြထားသည်။

## Subtopic စာရင်း (source ၏ အစဉ်အတိုင်း)

1. What the course code uses
2. Names refer to objects
3. A list holds pointers, an array holds numbers
4. A list holds every item, a generator holds one
5. The Idioms You Need — 1. Values, collections, and unpacking
6. The Idioms You Need — 2. Comprehensions
7. The Idioms You Need — 3. Functions, arguments, and closures
8. The Idioms You Need — 4. Classes and dataclasses
9. The Idioms You Need — 5. Iterators and generators
10. The Idioms You Need — 6. Context managers and exceptions
11. The Idioms You Need — 7. Type hints, modules, and the main guard
12. The Idioms You Need — 8. Files, JSON, CSV, and sorting
13. The Idioms You Need — 9. Counting, grouping, and iterator tools
14. The Idioms You Need — 10. Why loops over numbers are slow
15. Step 1: A record type and a dataset loader
16. Step 2: A seeded train and test split
17. Step 3: A mini-batch generator
18. Step 4: Vector math and a standardizer
19. Step 5: A complete run
20. Step 6: Measure speed and memory
21. The standard library versions
22. The same math with compiled arrays
23. Broadcasting
24. Further Reading

## Exercise စာရင်း

| # | Exercise | တစ်လိုင်း အနှစ်ချုပ် |
|---|---|---|
| 1 | `Record` နှင့် `load_records` | `@dataclass(frozen=True)` ဖြင့် `Record` သတ်မှတ်ပြီး ကိုယ်တိုင်ရေးသည့် CSV ကို record စာရင်း အဖြစ် ပြန်ဖတ်ခြင်း |
| 2 | `train_test_split` | `random.Random(seed)` ဖြင့် 80/20 train-test split ခွဲပြီး အရွယ်အစား၊ overlap နှင့် ပြန်လုပ်နိုင်မှုကို စစ်ခြင်း |
| 3 | `minibatch` | `itertools.islice` ဖြင့် mini-batch generator ရေးပြီး epoch တိုင်း generator အသစ် ဖန်တီးခြင်း |
| 4 | `vecmath` | dot product၊ mean၊ standard deviation နှင့် closure ဖြစ်သည့် standardizer ကို pure Python ဖြင့် ရေးခြင်း |
| 5 | `silent_bugs` | shared list၊ mutable default argument နှင့် ကုန်သွားသည့် generator သုံးမျိုးကို သရုပ်ပြပြီး ဖြေရှင်းခြင်း |
| 6 | `run_demo` | dot product variant သုံးမျိုးကို တိုင်းတာပြီး list နှင့် generator ၏ peak memory ကို နှိုင်းယှဉ်ခြင်း |

## ဖိုင်စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise နှင့် ဖိုင် စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ — ပြဿနာ၊ သဘောတရား၊ နှိုင်းယှဉ်ချက် ဇယား၊ လက်တွေ့ build ၊ သတိထားရန် အချက်၊ ကိုယ်တိုင်စစ်မေးခွန်း |
| `exercise.md` | လက်တွေ့ လုပ်ရမည့် exercise ၆ ခု (လိုအပ်ချက်၊ အဆင့်၊ အောင်မြင်မှု စစ်နည်း) |
| `solution.md` | exercise ၆ ခု၏ အဖြေ — တကယ် run ၍ ရသည့် output နှင့်တကွ |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ထားသည့် offline lab |

## Lab ကို run စစ်ခြင်း

```bash
python3 modules/13_python_for_ai_engineering/lab.py
```

ဤ command သည် exercise ၆ ခုကို အစဉ်လိုက် run ပြီး exercise တိုင်း၏ ရလဒ်ကို လူဖတ်နိုင်သော လိုင်းများဖြင့် print သည်။
အောင်မြင်ပါက နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ကို ပြပြီး exit code `0` ဖြင့် ပြီးဆုံးသည်။

Lab သည် data ကို မိမိကိုယ်တိုင် ရေးသည် — temporary directory တစ်ခုထဲသို့ CSV ဖိုင် တစ်ခု ရေးပြီး၊ ဖတ်ပြီး၊ ပြီးဆုံးသည့်အခါ ဖျက်ပစ်သည်။
ထို့ကြောင့် network မရှိသည့် စာသင်ခန်း သို့မဟုတ် offline machine တွင် လည်း run နိုင်သည်။
Output သည် run တိုင်းတွင် တူညီသည် — အချိန် (wall-clock) ကို တိုင်းတာ သော်လည်း ဂဏန်းကို မပြပါ။

## Cautions

- command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
- `math.sumprod` နှင့် `itertools.batched` သည် Python 3.12 သို့မဟုတ် အထက် လိုသည်။ Course သည် Python 3.11 ကို support လုပ်သောကြောင့် `main.py` သည် ကိုယ်ပိုင် `dot` နှင့် `batches` ကို ရေးထားသည်။
- `zip(..., strict=True)` သည် Python 3.10 သို့မဟုတ် အထက် လိုသည်။
- NumPy ကို install လုပ်ခြင်း (`uv pip install numpy`) သည် ဤ module ၏ lab အတွက် **မလိုပါ**။ Source ၏ ဥပမာအတွက်သာ ဖြစ်သည်။
