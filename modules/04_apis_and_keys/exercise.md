# Module 04 — Exercises

Exercise ၆ ခုလုံးကို `modules/04_apis_and_keys/lab.py` တွင် `def exercise_1()` … `def exercise_6()` အဖြစ်
implement လုပ်ထားသည်။ ဤဖိုင်တွင် လိုအပ်ချက်၊ လုပ်ရမည့် အဆင့်နှင့် အောင်မြင်မှု စစ်သည့် နည်းလမ်းကို ဖော်ပြသည်။

Security စည်းမျဉ်း — exercise တိုင်းတွင် key အနေဖြင့် သုံးရမည့် တန်ဖိုးသည် **ထင်ရှားသည့် placeholder**
(ဥပမာ `sk-ant-PLACEHOLDER-0000`) သာ ဖြစ်ရသည်။ တကယ့် key ကို ဤဖိုင်များတွင်လည်းကောင်း၊ print ရလဒ်တွင်လည်းကောင်း
မဖော်ပြရ။

## Exercise 1 — load_dotenv

**လိုအပ်ချက်။** `.env` ပုံစံ ဖိုင်တစ်ခုကို parse လုပ်သည့် function တစ်ခု ရေးရမည်။ ရလဒ်သည်
`{key: value}` dict ဖြစ်ရမည်။ Blank line နှင့် `#` ဖြင့် စသည့် comment line များကို ကျော်ရမည်။ Value တွင်
single သို့မဟုတ် double quote ပါလျှင် ဖယ်ရမည်။ Key အမည်စာရင်းကို print ရမည်၊ value ကို print **မရ** —
value ၏ အရှည် (length) ကိုသာ ပြရမည်။

**အဆင့်များ။**

1. `.env` ဖိုင်အထောက်အထား တစ်ခု တည်ဆောက်ပါ။ ၎င်းတွင် `ANTHROPIC_API_KEY`၊ `OPENAI_API_KEY`၊
   `LLM_MODEL` နှင့် `MAX_TOKENS` ပါရမည်။ Value အားလုံးသည် placeholder ဖြစ်ရမည်။
2. ဖိုင်ကို ဖတ်ပြီး line တိုင်းကို `=` ပထမဆုံး တွေ့သည့်နေရာတွင် ခွဲပါ။ `=` မပါသည့် line ကို ကျော်ပါ။
3. Quote ဖယ်ပါ။ `sorted()` ဖြင့် key အမည်များကို print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** ရလဒ် key စာရင်းသည် `ANTHROPIC_API_KEY`, `LLM_MODEL`, `MAX_TOKENS`,
`OPENAI_API_KEY` ဖြစ်ရမည်။ Comment line သည် key ဖြစ်လာခြင်း မရှိရ။ `LLM_MODEL` ၏ တန်ဖိုးသည် quote
မပါဘဲ `claude-sonnet-5` ဖြစ်ရမည်။ stdout တွင် key မည်သည့်လုံးမျှ မပေါ်ရ။

## Exercise 2 — mask_secret

**လိုအပ်ချက်။** Secret တစ်ခုကို log တွင် ပြရန် လိုအပ်သည့်အခါ ပြသင့်သည့် အနည်းဆုံး အပိုင်းသာ ပြသည့်
`mask_secret(secret, keep_prefix=7, keep_suffix=4)` function ရေးရမည်။ အလယ်ပိုင်းကို `...` ဖြင့် အစားထိုးရမည်။
တိုလွန်းသည့် value ကို လုံးဝ ဖုံးရမည်။

**အဆင့်များ။**

1. `secret[:keep_prefix] + "..." + secret[-keep_suffix:]` ကို တည်ဆောက်ပါ။
2. `len(secret) <= keep_prefix + keep_suffix` ဖြစ်လျှင် `...(hidden)` ပြန်ပါ။
3. Secret ဗလာ ဖြစ်လျှင် `(missing)` ပြန်ပါ။
4. Placeholder key တစ်ခုကို mask လုပ်ပြီး ရလဒ်ကို print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** `sk-ant-PLACEHOLDER-0000` ကို mask လုပ်လျှင် `sk-ant-...0000` ရမည်။
ရလဒ်တွင် `PLACEHOLDER` ဟူသော စကားလုံး မပါရ။ ဗလာ value အတွက် `(missing)`၊ တိုသည့် value အတွက်
`...(hidden)` ရမည်။

## Exercise 3 — build_messages_payload

**လိုအပ်ချက်။** Anthropic `/v1/messages` request ကို ကိုယ်စားပြုသည့် dict တစ်ခုကို
`build_messages_payload(model, max_tokens, prompt)` ဖြင့် တည်ဆောက်ရမည်။ Header များကိုလည်း
`build_messages_headers(api_key)` ဖြင့် တည်ဆောက်ရမည်။

**အဆင့်များ။**

1. Body တွင် `model`၊ `max_tokens` နှင့် `messages` သုံးခု ထည့်ပါ။ `messages` သည်
   `[{"role": "user", "content": prompt}]` ဖြစ်ရမည်။
2. Header တွင် `Content-Type`၊ `x-api-key` နှင့် `anthropic-version` ထည့်ပါ။ Version တန်ဖိုးသည်
   `2023-06-01` ဖြစ်ရမည်။
3. Model အတွက် default သည် `os.environ.get("LLM_MODEL", "claude-sonnet-5")` ဖြစ်ရမည်။
4. Payload ကို `json.dumps(payload, indent=4)` ဖြင့် print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** `set(payload)` သည် `{"model", "max_tokens", "messages"}` ဖြစ်ရမည်။
`messages[0]["role"] == "user"` ဖြစ်ရမည်။ Header တွင် key သုံးခု ရှိရမည်။

## Exercise 4 — parse_response

**လိုအပ်ချက်။** Documented response shape မှ text၊ token usage နှင့် `stop_reason` ကို ထုတ်သည့်
`parse_response(response)` function ရေးရမည်။

**အဆင့်များ။**

1. `content` စာရင်းကို ဖတ်ပြီး `type == "text"` ဖြစ်သည့် ပထမ block ၏ `text` ကို ယူပါ။
2. `usage` မှ `input_tokens` နှင့် `output_tokens` ကို ယူပြီး စုစုပေါင်းကို တွက်ပါ။
3. `stop_reason` ကို ယူပါ။
4. ရလဒ်ကို print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** Fabricated response (`input_tokens=12`၊ `output_tokens=28`) အတွက်
စုစုပေါင်းသည် 40 ဖြစ်ရမည်။ `stop_reason` သည် `end_turn` ဖြစ်ရမည်။ Raw JSON နှင့် SDK attribute
အမည်များ (`content`၊ `usage`၊ `stop_reason`) တူညီကြောင်း ပြရမည်။

## Exercise 5 — classify_api_error

**လိုအပ်ချက်။** HTTP status code ကို လုပ်ဆောင်ရမည့် အပြုအမူ (`stop` သို့မဟုတ် `backoff-retry`) အဖြစ်
ခွဲခြားသည့် `classify_api_error(status_code, retry_after_seconds=None)` function ရေးရမည်။
401 နှင့် 403 သည် `stop`၊ 429 နှင့် 5xx သည် `backoff-retry` ဖြစ်ရမည်။

**အဆင့်များ။**

1. 401 → `authentication_error`၊ 403 → `permission_error` ဟု သတ်မှတ်ပါ။ နှစ်ခုလုံး `stop` ဖြစ်သည်။
2. 429 → `rate_limit_error`၊ `backoff-retry`။ `retry_after_seconds` ပေးထားလျှင် `Retry-After` ဟူသော
   စကားလုံးကို reason တွင် ထည့်ပါ။
3. 500–599 → `server_error`၊ `backoff-retry`။
4. 400 နှင့် 404 ကို `stop` အဖြစ် ခွဲပါ။ အခြား status အတွက် `unknown_error` ပြန်ပါ။
5. Status တိုင်းအတွက် အဖြေကို ဇယားလိုက် print ပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** 401၊ 403၊ 400၊ 404 သည် `stop` ဖြစ်ရမည်။ 429၊ 500၊ 529 သည်
`backoff-retry` ဖြစ်ရမည်။

## Exercise 6 — api_call_report

**လိုအပ်ချက်။** Offline ဖြင့် API call တစ်ခုလုံးကို တုပြီး အစီရင်ခံစာ တစ်ခု print ရမည်။ နောက်ခံ
အဆင့်များအားလုံး (`.env` ဖတ်ခြင်း၊ key mask လုပ်ခြင်း၊ payload တည်ဆောက်ခြင်း၊ response parse လုပ်ခြင်း၊
error ခွဲခြားခြင်း) ကို ပြန်သုံးရမည်။ Network ကို လုံးဝ မခေါ်ရ။

**အဆင့်များ။**

1. `.env` မှ model နှင့် `max_tokens` ကို ဖတ်ပါ။ Key ကို mask လုပ်ပြီး print ပါ။
2. Payload နှင့် header တည်ဆောက်ပြီး request မှန်/မမှန် ဆုံးဖြတ်ပါ။
3. Fabricated response ကို parse လုပ်ပြီး text နှင့် token ကို print ပါ။
4. မအောင်မြင်သည့် အခြေအနေ ၃ ခု (401၊ 429၊ 500) ကို ခွဲခြားပြီး stop နှင့် backoff-retry အရေအတွက်ကို
   print ပါ။
5. အစီရင်ခံစာ အဆုံးတွင် စစ်ဆေးချက် အားလုံး အောင်မြင်ကြောင်း ပြပါ။

**အောင်မြင်မှု စစ်ဆေးခြင်း။** `mode` သည် `OFFLINE` ဖြစ်ရမည်။ Key preview သည် masked ဖြစ်ရမည်။
Token စုစုပေါင်းသည် 40 ဖြစ်ရမည်။ အခြေအနေ ၃ ခုတွင် stop ၁ ခု၊ backoff-retry ၂ ခု ရမည်။

## အားလုံးကို run စစ်ခြင်း

```bash
python3 modules/04_apis_and_keys/lab.py
echo "exit code: $?"
```

`[OK] exercise_N` လိုင်း ၆ ခုနှင့် နောက်ဆုံးလိုင်းတွင်
`[PASS] All 6/6 exercises passed successfully.` ပေါ်ရမည်။ Exit code သည် 0 ဖြစ်ရမည်။
