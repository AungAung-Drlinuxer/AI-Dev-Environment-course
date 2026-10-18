# Module 04 — APIs & Keys

## ရည်ရွယ်ချက် (Goal)

API key များကို **ကုဒ်နှင့် သီးခြား** လုံခြုံစွာ သိမ်းဆည်းသည့် အလေ့အကျင့်ကို တည်ဆောက်ပြီး LLM API ကို
SDK ဖြင့်လည်းကောင်း၊ SDK မသုံးဘဲ raw HTTP ဖြင့်လည်းကောင်း ခေါ်နိုင်ရမည်။ ခေါ်ဆိုမှု မအောင်မြင်သည့်အခါ
status code မှ လုပ်ဆောင်ရမည့် အပြုအမူ (ရပ်ရန် သို့မဟုတ် backoff-retry) ကို ဆုံးဖြတ်နိုင်ရမည်။

## လိုအပ်ချက် (Prerequisites)

- Phase 0, Lesson 01 (dev environment) ပြီးစီးထားခြင်း
- Python 3.11+ နှင့် Node.js 20+ (TypeScript ပိုင်းအတွက်)
- `.env` ဖိုင်၊ `.gitignore` နှင့် environment variable အခြေခံ နားလည်ခြင်း
- **ဤ module ၏ lab.py အတွက် network၊ API key သို့မဟုတ် third-party package မလိုအပ်ပါ** — lab သည်
  offline နှင့် deterministic ဖြစ်သည်။ API call ကို documented response shape အတိုင်း တုပထားသည်။

## Subtopic စာရင်း (Source ၏ အစဉ်အတိုင်း)

1. Step 1 — Store API keys safely (environment variable နှင့် `.env`)
2. Step 2 — First API call (Python)
3. Step 3 — First API call (TypeScript)
4. Step 4 — Raw HTTP (no SDK)

## Exercise စာရင်း

| # | Exercise | တစ်လိုင်း အနှစ်ချုပ် |
|---|---|---|
| 1 | load_dotenv | `.env` ဖိုင်ကို parse လုပ်ပြီး value များကို မပြဘဲ key အမည်စာရင်း ထုတ်ခြင်း |
| 2 | mask_secret | key ကို ပြသင့်သည့် အနည်းဆုံး အပိုင်းသာ ပြသော masked preview ထုတ်ခြင်း |
| 3 | build_messages_payload | Anthropic messages payload ကို dict အဖြစ် တည်ဆောက်ခြင်း |
| 4 | parse_response | documented response shape မှ text နှင့် token usage ကို ထုတ်ခြင်း |
| 5 | classify_api_error | 401 / 403 / 429 / 5xx ကို stop သို့မဟုတ် backoff-retry အဖြစ် ခွဲခြားခြင်း |
| 6 | api_call_report | offline ဖြင့် ခေါ်ဆိုမှု တစ်ခုလုံးကို တုပြီး အစီရင်ခံစာ ထုတ်ခြင်း |

## ဖိုင်စာရင်း

| ဖိုင် | တာဝန် |
|---|---|
| `README.md` | ဤဖိုင် — ရည်ရွယ်ချက်၊ လိုအပ်ချက်၊ subtopic၊ exercise စာရင်း |
| `explanation.md` | အဓိက သင်ခန်းစာ (Figure ၄ ခုနှင့် self-check ပါဝင်သည်) |
| `exercise.md` | exercise ၆ ခု — လိုအပ်ချက်၊ လုပ်ရမည့်အဆင့်၊ အောင်မြင်မှု စစ်နည်း |
| `solution.md` | အဖြေ ၆ ခု (တကယ် run ရလဒ်နှင့်တကွ) |
| `lab.py` | exercise ၆ ခုကို `def exercise_N()` အဖြစ် implement လုပ်ပြီး `assert` ဖြင့် စစ်သည့် ကုဒ် |

## Lab ကို run ခြင်း

```bash
python3 modules/04_apis_and_keys/lab.py
```

အောင်မြင်လျှင် နောက်ဆုံးလိုင်းတွင် `[PASS] All 6/6 exercises passed successfully.` ပေါ်ပြီး exit code သည် 0 ဖြစ်သည်။

## Cautions

- command များသည် version အလိုက် ပြောင်းလဲနိုင်သည်၊ run မီ မိမိ version အတွက် official documentation ကို စစ်ပါ။
- မော်ဒယ် id နှင့် API version header တန်ဖိုးများသည်လည်း version အလိုက် ပြောင်းလဲနိုင်သည်။
- API key ကို ဤ repository တွင် လုံးဝ မသိမ်းရ။ `.env` သည် `.gitignore` တွင် ပါပြီး ဖြစ်သည်။
- အမှားအမှန် နှိုင်းယှဉ်ရန် ရေးထားသည့် key တိုင်းသည် `sk-ant-...` ကဲ့သို့ **ထင်ရှားသည့် placeholder** သာ
  ဖြစ်သည်။ တကယ့် key ကို ဤ module ၏ ဖိုင် မည်သည့်နေရာတွင်မျှ မဖော်ပြရ။
