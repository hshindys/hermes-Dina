# Debugging: provider/model content-moderation false-positive (messaging platforms)

## Symptom
A task on Telegram/Discord/Slack returns a hard refusal with NO assistant answer:
"تم رفض الطلب لوجود محتوى غير مناسب" / "inappropriate content" / "content policy" /
"request blocked". The refusal is in the USER's language or a stock provider phrase.

This is the MODEL's own safety filter, NOT Hermes config (and NOT the busy-input
interrupt scaffold). Treat it as a different class from `references/debugging-interrupt-correction.md`.

## Step 1 — prove Hermes is not the source
Grep the codebase + locales for the exact refusal string. If it is absent, the model
is generating it.
```bash
cd "$HERMES_HOME/hermes-agent"   # or the cloned hermes-agent source
grep -rln "محتوى غير مناسب\|inappropriate content\|content policy" \
  agent/ gateway/ hermes_cli/ locales/ --include=*.py --include=*.yaml 2>/dev/null
# (On Windows MSYS use forward-slash paths; -rln works under git-bash.)
```
The Arabic refusal `تم رفض الطلب لوجود محتوى غير مناسب` is NOT present anywhere in
Hermes (only an unrelated `title_rejected` locale line). => It comes from the model endpoint.

## Step 2 — identify the active model
```bash
grep -nE "^  default:|provider:|base_url:" "$HERMES_HOME/config.yaml"
```
Common offender: `tencent/hy3:free` (Tencent Hunyuan). Its hosted filter emits that
exact Arabic sentence and FALSE-POSITIVES on Arabic text and benign topics.

## Step 3 — confirm connection is healthy (rule out auth/network)
```bash
grep -iE "API call #|model=qwen|model=tencent|provider=nous" "$HERMES_HOME/logs/agent.log" | tail
```
If OTHER tasks answer fine (successful API calls), the block is content-policy, not
auth/network. Do NOT chase credentials.

## Step 4 (optional) — reproduce via the real endpoint
If you must reproduce directly with a script, you will hit a Cloudflare pitfall:
- Bare `urllib.request` with the default `Python-urllib/*` User-Agent to
  `https://inference-api.nousresearch.com/v1/chat/completions` returns
  `HTTP 403 error code: 1010` — that is Cloudflare's Browser Integrity Check
  rejecting the UA, NOT the moderation block.
- Fix: send Hermes's own UA `hermes-cli/<version>` (from `hermes_cli/__version__`)
  and an invoke JWT read from `$HERMES_HOME/auth.json`
  (`providers -> nous -> ... -> invoke_jwt / access_token`).
- Even then, a 1010 in a hand-rolled script is unreliable evidence. The definitive
  signal is the live `agent.log` API-call lines and the user's reported refusal text.

Minimal correct-shape probe (illustrative, not authoritative):
```python
import json, urllib.request
d = json.load(open(HERMES_HOME + "/auth.json"))
nous = d["providers"]["nous"]
# walk nous for an invoke_jwt / access_token string (len > 20)
tok = <first long jwt-ish string found>
ua = "hermes-cli/3.1.0"   # match HERMES_VERSION
hdr = {"Authorization": "Bearer " + tok, "Content-Type": "application/json",
       "User-Agent": ua}
req = urllib.request.Request(
    "https://inference-api.nousresearch.com/v1/chat/completions",
    data=json.dumps({"model":"tencent/hy3:free",
                     "messages":[{"role":"user","content":"<the blocked text>"}],
                     "max_tokens":50}).encode(), headers=hdr)
# 403 "inappropriate content" in the body == model filter; 403 "error code: 1010" == UA/Cloudflare
```

## The fix — switch the default model
```bash
hermes config set model.default qwen/qwen3-32b:free
hermes gateway restart
```
- `qwen/qwen3-32b:free` — good Arabic support, far lighter moderation false-positives.
- Alternatives (free via Nous): `meta-llama/llama-3.3-70b-instruct:free`,
  `google/gemini-2.5-flash:free`.
- Paid Nous models avoid the false blocks entirely (recommended if the user okays cost).

## Verification
- `gateway_state.json` → `gateway_state: "running"`, `platforms.telegram.state: "connected"`.
- `grep -iE "model=qwen" "$HERMES_HOME/logs/agent.log"` shows the new client created.
- Send a previously-blocked task → it completes with no refusal.

## Independence note
This model fix is orthogonal to the busy-input `queue` fix
(see `references/debugging-interrupt-correction.md`). Both can apply in one session.

## Real-world example (this machine, 2026-08-03)
- Model was `tencent/hy3:free`. User's Arabic task ("ممكن تعمل بحث على اليوتيوب…")
  returned "تم رفض الطلب لوجود محتوى غير مناسب".
- Grep proved the string is absent from Hermes source → Hunyuan filter.
- Other tasks answered fine (agent.log full of successful `hy3:free` API calls) → not auth/network.
- Fix: `hermes config set model.default qwen/qwen3-32b:free` + `hermes gateway restart`.
  Gateway restarted, Telegram reconnected, new client on `qwen/qwen3-32b:free`.
