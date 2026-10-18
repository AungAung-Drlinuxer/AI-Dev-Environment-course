# Module 04 — Solutions

ဤဖိုင်ရှိ output အားလုံးသည် `python3 modules/04_apis_and_keys/lab.py` ကို တကယ် run ၍ ရသည့် ရလဒ် ဖြစ်သည်။
Hand-computed တန်ဖိုး မပါဝင်ပါ။

> **Security စည်းမျဉ်း။** ဤ module ၏ output တွင် ပေါ်သည့် key သည် `sk-ant-PLACEHOLDER-0000` ကဲ့သို့
> ထင်ရှားသည့် placeholder သာ ဖြစ်သည်။ တကယ့် key ကို ဤဖိုင်၊ `lab.py` သို့မဟုတ် print ရလဒ် မည်သည့်နေရာတွင်မျှ
> မဖော်ပြရ။ Masked preview တွင်လည်း ပြသင့်သည့် prefix နှင့် နောက်ဆုံး အက္ခရာ ၄ လုံးသာ ပေါ်သည်။

## Exercise 1 — load_dotenv

`.env` ပုံစံ ဖိုင်ကို parse လုပ်ပြီး key အမည်စာရင်းသာ ထုတ်သည်။ Value သည် အရှည် (length) အဖြစ်သာ ပေါ်သည်။

```python
import tempfile
from pathlib import Path

ENV_FILE_TEXT = """# Module 04 fixture .env (placeholder values only)
ANTHROPIC_API_KEY=sk-ant-PLACEHOLDER-0000
OPENAI_API_KEY=sk-PLACEHOLDER-0000
# The model id can be overridden per shell.
LLM_MODEL="claude-sonnet-5"
MAX_TOKENS=256
"""


def parse_env_text(text):
    result = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if not key:
            continue
        result[key] = value
    return result


path = Path(tempfile.gettempdir()) / "module04_fixture.env"
path.write_text(ENV_FILE_TEXT, encoding="utf-8")
env = parse_env_text(path.read_text(encoding="utf-8"))
for key in sorted(env):
    print("    - %-20s value length=%d (value not printed)" % (key, len(env[key])))
```

**တကယ့် output**

```text
Exercise 1 - parse .env and list key names only
  fixture file      : /home/aungaung/.hermes/profiles/ai-engineer/cache/scratch/module04_fixture.env
  keys found        : 4
    - ANTHROPIC_API_KEY    value length=23 (value not printed)
    - LLM_MODEL            value length=15 (value not printed)
    - MAX_TOKENS           value length=3 (value not printed)
    - OPENAI_API_KEY       value length=19 (value not printed)
  comment lines and surrounding quotes handled correctly
[OK] exercise_1 - .env parsed, key names listed without values
```

ပထမ comment line သည် key မဖြစ်ခဲ့ပါ။ `LLM_MODEL` ၏ value သည် double quote ဖယ်ပြီးနောက်
`claude-sonnet-5` (၁၅ လုံး) ဖြစ်သည်။ Key တန်ဖိုး တစ်လုံးမျှ print မဖြစ်ခဲ့ပါ။

## Exercise 2 — mask_secret

```python
def mask_secret(secret, keep_prefix=7, keep_suffix=4):
    if not secret:
        return "(missing)"
    if len(secret) <= keep_prefix + keep_suffix:
        return "...(hidden)"
    return secret[:keep_prefix] + "..." + secret[-keep_suffix:]
```

**တကယ့် output**

```text
Exercise 2 - mask a secret for display
  raw value hidden  : yes (never printed)
  masked preview    : sk-ant-...0000
  visible characters: 11 of 23
  empty and short inputs are fully hidden
[OK] exercise_2 - secret masked to a short prefix and suffix
```

Placeholder key သည် ၂၃ လုံး ရှိသည်။ Mask ပြီးနောက် `sk-ant-...` (၇ လုံး) နှင့် `0000` (၄ လုံး) —
စုစုပေါင်း ၁၁ လုံးသာ ပေါ်သည်။ အလယ်ပိုင်း ၁၂ လုံး (တကယ့် key ဖြစ်လျှင် အရေးကြီးသည့် အပိုင်း) သည်
လုံးဝ ပေါ်မလာပါ။ တကယ့် key ဖြစ်လျှင် output သည် `sk-ant-...AB12` ကဲ့သို့ ပေါ်မည် — ကုဒ်ထဲတွင်
မည်သည့်အခါမျှ ပြည့်စုံသည့် တန်ဖိုး မပေါ်ရ။

## Exercise 3 — build_messages_payload

```python
ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
PROMPT = "What is a neural network in one sentence?"


def build_messages_payload(model, max_tokens, prompt):
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }


def build_messages_headers(api_key):
    return {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }
```

**တကယ့် output**

```text
Exercise 3 - build the /v1/messages payload
  endpoint          : https://api.anthropic.com/v1/messages
  header names      : ['Content-Type', 'anthropic-version', 'x-api-key']
  payload:
{
    "model": "claude-sonnet-5",
    "max_tokens": 256,
    "messages": [
        {
            "role": "user",
            "content": "What is a neural network in one sentence?"
        }
    ]
}
  payload and headers match the documented request shape
[OK] exercise_3 - messages payload built as a dict
```

Payload ၏ key ၃ ခုနှင့် header ၃ ခုသည် source ၏ request shape အတိုင်း ဖြစ်သည်။ `anthropic-version` ၏
တန်ဖိုးသည် `2023-06-01` ဖြစ်ပြီး version အလိုက် ပြန်စစ်ရန် လိုသည်။

## Exercise 4 — parse_response

```python
FABRICATED_RESPONSE = {
    "id": "msg_0000000000000000000000",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-5",
    "content": [
        {
            "type": "text",
            "text": (
                "A neural network is a stack of differentiable functions "
                "that learns patterns by adjusting weights against a loss "
                "signal."
            ),
        }
    ],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {"input_tokens": 12, "output_tokens": 28},
}


def parse_response(response):
    blocks = response.get("content") or []
    text = ""
    for block in blocks:
        if block.get("type") == "text":
            text = block.get("text", "")
            break
    usage = response.get("usage") or {}
    return {
        "text": text,
        "input_tokens": int(usage.get("input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
        "total_tokens": int(usage.get("input_tokens", 0))
        + int(usage.get("output_tokens", 0)),
        "stop_reason": response.get("stop_reason"),
    }
```

**တကယ့် output**

```text
Exercise 4 - parse the response shape
  top-level fields  : ['content', 'id', 'model', 'role', 'stop_reason', 'stop_sequence', 'type', 'usage']
  content blocks    : 1
  text              : A neural network is a stack of differentiable functions that learns patterns by adjusting weights against a loss signal.
  stop_reason       : end_turn
  tokens            : 12 in, 28 out, 40 total
  raw JSON and SDK attribute names agree (content/usage/stop_reason)
[OK] exercise_4 - response text and token usage extracted
```

`result["content"][0]["text"]` (raw HTTP) နှင့် `response.content[0].text` (SDK) သည် တူညီသည့်
တန်ဖိုးကို ဖတ်ကြောင်း ဤ output က ပြသည်။ Token စုစုပေါင်းသည် 12 + 28 = 40 ဖြစ်သည်။

## Exercise 5 — classify_api_error

```python
def classify_api_error(status_code, retry_after_seconds=None):
    if status_code == 401:
        return {"status": 401, "kind": "authentication_error", "action": "stop",
                "reason": "The API key is missing, malformed or revoked. ..."}
    if status_code == 403:
        return {"status": 403, "kind": "permission_error", "action": "stop",
                "reason": "The key is valid but the account or organization is not allowed ..."}
    if status_code == 429:
        return {"status": 429, "kind": "rate_limit_error", "action": "backoff-retry",
                "reason": "Too many requests for this key.  Wait at least 30 second(s) per "
                          "the Retry-After header, then retry with exponential backoff."}
    if 500 <= status_code <= 599:
        return {"status": status_code, "kind": "server_error", "action": "backoff-retry",
                "reason": "The provider is overloaded or has an internal fault. ..."}
    # 400, 404 နှင့် အခြား status များ → stop
```

**တကယ့် output**

```text
Exercise 5 - classify API errors into an action
  HTTP 401  -> authentication_error action=stop
  HTTP 403  -> permission_error     action=stop
  HTTP 429  -> rate_limit_error     action=backoff-retry
  HTTP 500  -> server_error         action=backoff-retry
  HTTP 529  -> server_error         action=backoff-retry
  HTTP 400  -> invalid_request_error action=stop
  HTTP 404  -> not_found_error      action=stop
  HTTP 429 detail   : Too many requests for this key.  Wait at least 30 second(s) per the Retry-After header, then retry with exponential backoff.
  stop vs backoff-retry split is correct
[OK] exercise_5 - 401/403/429/5xx mapped to an action
```

401 နှင့် 403 သည် `stop` ဖြစ်သည် — key ကို မပြင်ဘဲ retry လုပ်လျှင် အလားတူ error ပြန်လာမည်။ 429 နှင့်
5xx သည် `backoff-retry` ဖြစ်သည် — စောင့်လျှင် အောင်မြင်နိုင်သည်။

## Exercise 6 — api_call_report

```python
env = parse_env_text(ENV_FILE_TEXT)
api_key = env["ANTHROPIC_API_KEY"]
model = env.get("LLM_MODEL", "claude-sonnet-5")
max_tokens = int(env.get("MAX_TOKENS", "256"))

print("  key preview       : %s" % mask_secret(api_key))
payload = build_messages_payload(model, max_tokens, PROMPT)
headers = build_messages_headers(api_key)
parsed = parse_response(FABRICATED_RESPONSE)
scenarios = [classify_api_error(401), classify_api_error(429, 30), classify_api_error(500)]
```

Network ကို လုံးဝ မခေါ်ပါ။ `FABRICATED_RESPONSE` သည် documented `/v1/messages` response shape ကို
ကိုယ်စားပြုသည်။

**တကယ့် output**

```text
Exercise 6 - end-to-end offline API call report
  mode              : OFFLINE (no network request is made)
  model             : claude-sonnet-5
  endpoint          : https://api.anthropic.com/v1/messages
  key preview       : sk-ant-...0000
  max_tokens        : 256
  request valid     : yes
  response text     : A neural network is a stack of differentiable functions that learns patterns by adjusting weights against a loss signal.
  tokens            : 12 in, 28 out
  stop_reason       : end_turn
  scenario HTTP 401  -> action=stop
  scenario HTTP 429  -> action=backoff-retry
  scenario HTTP 500  -> action=backoff-retry
  verdict           : REQUEST AND RESPONSE OK
  report complete: 1 success path, 1 stop, 2 backoff-retry
[OK] exercise_6 - offline API call simulated and reported
```

Key preview သည် `sk-ant-...0000` ဖြစ်သည် — ပြည့်စုံသည့် တန်ဖိုး မပေါ်ပါ။ အခြေအနေ ၃ ခုတွင် stop
၁ ခု (401)၊ backoff-retry ၂ ခု (429၊ 500) ရသည်။

## Run စစ်ခြင်း ရလဒ်

```text
$ python3 modules/04_apis_and_keys/lab.py
...
[OK] exercise_1 - .env parsed, key names listed without values
[OK] exercise_2 - secret masked to a short prefix and suffix
[OK] exercise_3 - messages payload built as a dict
[OK] exercise_4 - response text and token usage extracted
[OK] exercise_5 - 401/403/429/5xx mapped to an action
[OK] exercise_6 - offline API call simulated and reported

[PASS] All 6/6 exercises passed successfully.
$ echo "exit code: $?"
exit code: 0
```

`[OK] exercise_N` လိုင်း ၆ ခု ပေါ်သည်။ Exit code သည် 0 ဖြစ်သည်။ Network၊ API key နှင့်
third-party package မလိုအပ်ပါ။
