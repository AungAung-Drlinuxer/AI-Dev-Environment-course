#!/usr/bin/env python3
"""Module 04 - APIs & Keys: offline, deterministic lab.

Run:
    python3 modules/04_apis_and_keys/lab.py

Standard library only. No network, no SDK, no GPU. The API call of
exercise 6 is simulated against a fabricated response shape that matches
the documented Anthropic /v1/messages response (content, usage, stop_reason).

Security note: every credential literal in this file is an obvious
placeholder. The lab never prints a full secret; the helpers below mask it
down to a short prefix and a short suffix.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared fixtures - all values are obvious placeholders, never real keys.
# ---------------------------------------------------------------------------

PLACEHOLDER_KEY = "sk-ant-PLACEHOLDER-0000"
PLACEHOLDER_OPENAI_KEY = "sk-PLACEHOLDER-0000"

ENV_FILE_TEXT = """# Module 04 fixture .env (placeholder values only)
ANTHROPIC_API_KEY=sk-ant-PLACEHOLDER-0000
OPENAI_API_KEY=sk-PLACEHOLDER-0000
# The model id can be overridden per shell.
LLM_MODEL="claude-sonnet-5"
MAX_TOKENS=256
"""

DEFAULT_MODEL = "claude-sonnet-5"
ENDPOINT = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
PROMPT = "What is a neural network in one sentence?"

# Documented response shape of POST /v1/messages.
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


# ---------------------------------------------------------------------------
# Helpers reused across exercises
# ---------------------------------------------------------------------------

def parse_env_text(text):
    """Parse .env-style text into a dict.

    Rules (same shape every dotenv loader follows):
      * blank lines and lines starting with '#' are skipped
      * KEY=VALUE split on the first '='
      * optional surrounding single or double quotes are stripped
    Returns {key: value}.
    """
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


def mask_secret(secret, keep_prefix=7, keep_suffix=4):
    """Return a display-safe preview of a secret.

    Only the first `keep_prefix` characters and the last `keep_suffix`
    characters survive; everything between them is replaced by '...'.
    A value too short to mask safely is fully hidden.
    """
    if not secret:
        return "(missing)"
    if len(secret) <= keep_prefix + keep_suffix:
        return "...(hidden)"
    return secret[:keep_prefix] + "..." + secret[-keep_suffix:]


def build_messages_payload(model, max_tokens, prompt):
    """Build the JSON body of a /v1/messages request."""
    return {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }


def build_messages_headers(api_key):
    """Build the HTTP headers of a /v1/messages request."""
    return {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
    }


def parse_response(response):
    """Extract text, token usage and stop_reason from a response dict."""
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


def classify_api_error(status_code, retry_after_seconds=None):
    """Map an HTTP status code to the action a client must take.

    The action is one of:
      * "stop"           - retrying the same request cannot succeed
      * "backoff-retry"  - transient; wait then retry with backoff
    """
    if status_code == 401:
        return {
            "status": 401,
            "kind": "authentication_error",
            "action": "stop",
            "reason": (
                "The API key is missing, malformed or revoked. Retrying with "
                "the same key fails again; fix or rotate the key first."
            ),
        }
    if status_code == 403:
        return {
            "status": 403,
            "kind": "permission_error",
            "action": "stop",
            "reason": (
                "The key is valid but the account or organization is not "
                "allowed to use this model or feature. Change the account or "
                "the model; do not retry."
            ),
        }
    if status_code == 429:
        detail = "  Wait, then retry with exponential backoff."
        if retry_after_seconds is not None:
            detail = (
                "  Wait at least %s second(s) per the Retry-After header, "
                "then retry with exponential backoff." % retry_after_seconds
            )
        return {
            "status": 429,
            "kind": "rate_limit_error",
            "action": "backoff-retry",
            "reason": "Too many requests for this key." + detail,
        }
    if 500 <= status_code <= 599:
        return {
            "status": status_code,
            "kind": "server_error",
            "action": "backoff-retry",
            "reason": (
                "The provider is overloaded or has an internal fault. The "
                "request may succeed later; retry with backoff and a cap."
            ),
        }
    if status_code == 400:
        return {
            "status": 400,
            "kind": "invalid_request_error",
            "action": "stop",
            "reason": (
                "The request body is malformed, for example a missing "
                "max_tokens or bad message roles. Fix the payload."
            ),
        }
    if status_code == 404:
        return {
            "status": 404,
            "kind": "not_found_error",
            "action": "stop",
            "reason": (
                "The endpoint or model id does not exist. Check the URL and "
                "the model id for the account."
            ),
        }
    return {
        "status": status_code,
        "kind": "unknown_error",
        "action": "stop",
        "reason": "Unrecognised status; read the response body before retrying.",
    }


# ---------------------------------------------------------------------------
# Exercise 1 - load_dotenv
# ---------------------------------------------------------------------------

def exercise_1():
    """Parse a .env file and report key names without revealing values."""
    print("Exercise 1 - parse .env and list key names only")

    path = Path(tempfile.gettempdir()) / "module04_fixture.env"
    path.write_text(ENV_FILE_TEXT, encoding="utf-8")

    env = parse_env_text(path.read_text(encoding="utf-8"))

    print("  fixture file      : %s" % path)
    print("  keys found        : %d" % len(env))
    for key in sorted(env):
        print("    - %-20s value length=%d (value not printed)"
              % (key, len(env[key])))

    assert sorted(env) == [
        "ANTHROPIC_API_KEY",
        "LLM_MODEL",
        "MAX_TOKENS",
        "OPENAI_API_KEY",
    ]
    # A comment line must never become a key.
    assert not any(key.startswith("#") for key in env)
    # Quoted values lose their quotes.
    assert env["LLM_MODEL"] == "claude-sonnet-5"
    assert env["ANTHROPIC_API_KEY"] == PLACEHOLDER_KEY
    print("  comment lines and surrounding quotes handled correctly")
    print("[OK] exercise_1 - .env parsed, key names listed without values")
    return env


# ---------------------------------------------------------------------------
# Exercise 2 - mask_secret
# ---------------------------------------------------------------------------

def exercise_2():
    """Show only a short prefix and suffix of a secret."""
    print("Exercise 2 - mask a secret for display")

    masked = mask_secret(PLACEHOLDER_KEY)
    print("  raw value hidden  : yes (never printed)")
    print("  masked preview    : %s" % masked)
    print("  visible characters: %d of %d" % (11, len(PLACEHOLDER_KEY)))

    assert masked == "sk-ant-...0000"
    # The middle of the secret must not survive masking.
    assert "PLACEHOLDER" not in masked
    assert mask_secret("") == "(missing)"
    assert mask_secret("short") == "...(hidden)"
    print("  empty and short inputs are fully hidden")
    print("[OK] exercise_2 - secret masked to a short prefix and suffix")
    return masked


# ---------------------------------------------------------------------------
# Exercise 3 - build_messages_payload
# ---------------------------------------------------------------------------

def exercise_3():
    """Build the Anthropic messages payload as a plain dict."""
    print("Exercise 3 - build the /v1/messages payload")

    payload = build_messages_payload(DEFAULT_MODEL, 256, PROMPT)
    headers = build_messages_headers(PLACEHOLDER_KEY)

    print("  endpoint          : %s" % ENDPOINT)
    print("  header names      : %s" % sorted(headers))
    print("  payload:")
    print(json.dumps(payload, indent=4, ensure_ascii=False))

    assert set(payload) == {"model", "max_tokens", "messages"}
    assert payload["model"] == "claude-sonnet-5"
    assert payload["max_tokens"] == 256
    assert payload["messages"][0]["role"] == "user"
    assert payload["messages"][0]["content"] == PROMPT
    assert headers["anthropic-version"] == "2023-06-01"
    assert headers["x-api-key"] == PLACEHOLDER_KEY
    print("  payload and headers match the documented request shape")
    print("[OK] exercise_3 - messages payload built as a dict")
    return payload


# ---------------------------------------------------------------------------
# Exercise 4 - parse_response
# ---------------------------------------------------------------------------

def exercise_4():
    """Extract text and token usage from the documented response shape."""
    print("Exercise 4 - parse the response shape")

    parsed = parse_response(FABRICATED_RESPONSE)

    print("  top-level fields  : %s"
          % sorted(FABRICATED_RESPONSE))
    print("  content blocks    : %d" % len(FABRICATED_RESPONSE["content"]))
    print("  text              : %s" % parsed["text"])
    print("  stop_reason       : %s" % parsed["stop_reason"])
    print("  tokens            : %d in, %d out, %d total"
          % (parsed["input_tokens"], parsed["output_tokens"],
             parsed["total_tokens"]))

    assert parsed["input_tokens"] == 12
    assert parsed["output_tokens"] == 28
    assert parsed["total_tokens"] == 40
    assert parsed["stop_reason"] == "end_turn"
    assert parsed["text"].startswith("A neural network is a stack")

    # The same field names appear in the raw JSON and on the SDK object.
    raw = json.loads(json.dumps(FABRICATED_RESPONSE))
    assert raw["content"][0]["text"] == parsed["text"]
    assert raw["usage"]["input_tokens"] == parsed["input_tokens"]
    print("  raw JSON and SDK attribute names agree (content/usage/stop_reason)")
    print("[OK] exercise_4 - response text and token usage extracted")
    return parsed


# ---------------------------------------------------------------------------
# Exercise 5 - classify_api_error
# ---------------------------------------------------------------------------

def exercise_5():
    """Classify 401 / 403 / 429 / 5xx into an action."""
    print("Exercise 5 - classify API errors into an action")

    cases = [
        (401, None),
        (403, None),
        (429, 30),
        (500, None),
        (529, None),
        (400, None),
        (404, None),
    ]

    decisions = {}
    for status, retry_after in cases:
        decision = classify_api_error(status, retry_after)
        decisions[status] = decision
        print("  HTTP %-4s -> %-20s action=%s"
              % (decision["status"], decision["kind"], decision["action"]))

    print("  HTTP 429 detail   : %s" % decisions[429]["reason"])

    assert decisions[401]["action"] == "stop"
    assert decisions[403]["action"] == "stop"
    assert decisions[429]["action"] == "backoff-retry"
    assert decisions[500]["action"] == "backoff-retry"
    assert decisions[529]["action"] == "backoff-retry"
    assert decisions[400]["action"] == "stop"
    assert decisions[404]["action"] == "stop"
    assert "Retry-After" in decisions[429]["reason"]
    print("  stop vs backoff-retry split is correct")
    print("[OK] exercise_5 - 401/403/429/5xx mapped to an action")
    return decisions


# ---------------------------------------------------------------------------
# Exercise 6 - api_call_report
# ---------------------------------------------------------------------------

def exercise_6():
    """Simulate one whole API call offline and print a report."""
    print("Exercise 6 - end-to-end offline API call report")

    env = parse_env_text(ENV_FILE_TEXT)
    api_key = env["ANTHROPIC_API_KEY"]
    model = env.get("LLM_MODEL", DEFAULT_MODEL)
    max_tokens = int(env.get("MAX_TOKENS", "256"))

    print("  mode              : OFFLINE (no network request is made)")
    print("  model             : %s" % model)
    print("  endpoint          : %s" % ENDPOINT)
    print("  key preview       : %s" % mask_secret(api_key))
    print("  max_tokens        : %d" % max_tokens)

    payload = build_messages_payload(model, max_tokens, PROMPT)
    headers = build_messages_headers(api_key)
    request_ok = (
        set(payload) == {"model", "max_tokens", "messages"}
        and headers["anthropic-version"] == ANTHROPIC_VERSION
        and headers["x-api-key"] == api_key
    )
    print("  request valid     : %s" % ("yes" if request_ok else "no"))

    parsed = parse_response(FABRICATED_RESPONSE)
    print("  response text     : %s" % parsed["text"])
    print("  tokens            : %d in, %d out"
          % (parsed["input_tokens"], parsed["output_tokens"]))
    print("  stop_reason       : %s" % parsed["stop_reason"])

    # Three failure scenarios the same client code must survive.
    scenarios = [
        classify_api_error(401),
        classify_api_error(429, 30),
        classify_api_error(500),
    ]
    stop_count = 0
    retry_count = 0
    for decision in scenarios:
        print("  scenario HTTP %-4s -> action=%s"
              % (decision["status"], decision["action"]))
        if decision["action"] == "stop":
            stop_count += 1
        else:
            retry_count += 1

    verdict = "REQUEST AND RESPONSE OK" if request_ok else "REQUEST INVALID"
    print("  verdict           : %s" % verdict)

    assert request_ok
    assert parsed["total_tokens"] == 40
    assert stop_count == 1 and retry_count == 2
    assert api_key == PLACEHOLDER_KEY  # placeholder fixture, never a real key
    print("  report complete: 1 success path, %d stop, %d backoff-retry"
          % (stop_count, retry_count))
    print("[OK] exercise_6 - offline API call simulated and reported")
    return {
        "model": model,
        "masked_key": mask_secret(api_key),
        "tokens": parsed["total_tokens"],
        "verdict": verdict,
    }


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("Module 04 - APIs & Keys (offline lab)")
    print("=" * 72)
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    print()
    print("[PASS] All 6/6 exercises passed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
