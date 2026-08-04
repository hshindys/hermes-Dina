---
name: hermes-gateway-messaging
description: "Fix Hermes Telegram/Discord/Slack messaging failures: (1) '[This response was interrupted by a user correction.]' from busy-input interrupt mode on duplicate delivery, and (2) provider/model content-moderation false-positives (e.g. Hunyuan 'تم رفض الطلب لوجود محتوى غير مناسب') that block normal tasks."
version: 1.0.0
author: Hermes curator
license: MIT
platforms: [linux, macos, windows]
---

# Hermes Gateway Messaging — interrupt / correction / busy-input issues

## When to load this skill
- User reports answers on Telegram/Discord/Slack come back as `[This response was interrupted by a user correction.]` or get cut off when they send a task.
- A message sent while the agent is "thinking" disappears, restarts the turn, or is folded into the running turn as a correction.
- Symptoms appear only on messaging platforms (telegram/discord/slack), not in the CLI or desktop app.
- User reports a task on Telegram/Discord/Slack returns a hard rejection like "تم رفض الطلب لوجود محتوى غير مناسب" / "inappropriate content" / "content policy" / "request blocked" — the agent refuses/aborts BEFORE producing any answer, and the refusal text is in the USER'S language or a stock provider phrase (not a friendly Hermes sentence). This is a **provider/model safety-filter false-positive**, not the busy-input interrupt above.
- A normal, harmless task (e.g. "search YouTube…", "say hi") is refused while other tasks work — points to the MODEL's moderation, not Hermes config.

## Symptom → root cause (most common)
`[This response was interrupted by a user correction.]` is NOT a bug in the task. It is Hermes's **busy-input interrupt** scaffold. With `display.busy_input_mode: interrupt`, ANY inbound message that arrives while a turn is still running is treated as a mid-task correction: the gateway calls `agent.redirect()`, which aborts the in-flight model request and prepends the scaffold text.

The usual trigger is **duplicate delivery**: the same user message lands twice (or a third time on another platform). The first delivery starts the turn (session becomes "busy"); the later duplicate arrives while busy → gateway reads it as a correction → the running answer is killed and the scaffold appears.

Why duplicates happen: Telegram uses long-poll (`getUpdates`). On a network blip the gateway reconnects (logs show `[Telegram] Telegram polling restarted after network error`), and if a message arrived during the gap it can be redelivered. Telegram also shares sessions across linked platforms (a message to the Discord mirror can echo to Telegram), producing apparent duplicates.

## Diagnosis (verify before changing anything)
1. Confirm the mode in config:
   `grep -n "busy_input_mode" "$HERMES_HOME/config.yaml"`
   (HERMES_HOME is usually `~/.hermes` on Linux/macOS, `C:\Users\<user>\AppData\Local\hermes` on Windows.)
2. Prove duplicate delivery from the gateway log:
   `grep -inE "inbound message" "$HERMES_HOME/logs/gateway.log" | tail -40`
   Look for the SAME message text appearing at two+ timestamps within a few minutes, especially across platforms (telegram + discord).
3. Check connection/reconnect chatter that explains the dup:
   `grep -inE "polling restarted|polling reconnect failed|degraded" "$HERMES_HOME/logs/gateway.log" | tail -20`
4. Confirm gateway is actually up and which platform is connected:
   read `"$HERMES_HOME/gateway_state.json"` (`gateway_state: running`, `platforms.telegram.state: connected`). Note: after a restart the state file may briefly lag the new PID — check `ps` for the live PID and the tail of `gateway.log` for `Connected to Telegram (polling mode)`.

See `references/debugging-interrupt-correction.md` for the full command recipes, exact file paths, and the code call chain (config → `gateway/run.py` busy branch → `run_agent.py redirect()` → `agent/conversation_loop.py` scaffold). For the provider content-moderation false-positive (Symptom #2), see `references/debugging-content-moderation.md`.

## The fix
Switch busy-input mode from `interrupt` to `queue` so late/duplicate messages wait for the current turn instead of aborting it, then restart the gateway:

```
hermes config set display.busy_input_mode queue
hermes gateway restart
```

`hermes config set` is the ONLY supported way to edit config — never hand-edit `config.yaml` (a stray indent corrupts it and can break the live gateway). After restart, verify: config line shows `busy_input_mode: queue`, gateway_state `running`, and `Connected to Telegram (polling mode)` in the log.

Behavior after the fix:
- Normal tasks run to completion — no more "interrupted by a user correction" line.
- A message sent while the agent is busy is queued and answered when the turn finishes (no cut-off).
- `/stop` (and `/new`) still force-cancels a running turn — it bypasses busy_input_mode.

## Symptom #2 — provider/model content-moderation false-positive
A task returns a hard refusal ("تم رفض الطلب لوجود محتوى غير مناسب" / "inappropriate content" / "content policy" / "request blocked") with NO assistant answer. This is the MODEL's own safety filter, NOT Hermes.

### How to tell it apart from the interrupt issue
- The interrupt scaffold (`[This response was interrupted by a user correction.]`) is Hermes-internal machinery and only fires on a busy-input duplicate. A flat refusal sentence in the USER'S language (often Arabic for Hunyuan) is the provider's filter.
- **First proof step: grep the Hermes source + locale files for the exact refusal string.** If it is NOT there, Hermes is not generating it — the model is. (The string `تم رفض الطلب…` does not exist anywhere in Hermes's `agent/`, `gateway/`, `hermes_cli/`, or `locales/` — only an unrelated `title_rejected` line. So it comes from the model endpoint.)
- Check the agent/gateway logs for the model actually in use: `grep -iE "model=qwen|model=tencent|provider=nous" "$HERMES_HOME/logs/agent.log" | tail`. Successful calls (different tasks answering fine) confirm the connection is healthy — so the block is content-policy, not auth/network.

### Why it happens
Free hosted models with aggressive moderation (notably `tencent/hy3:free` / Hunyuan) emit that exact Arabic sentence when their safety filter trips. The filter FALSE-POSITIVES heavily on Arabic text and on certain benign topics (e.g. "search YouTube for…"), so ordinary tasks get refused even though nothing is inappropriate.

### Diagnosis checklist (verify before switching models)
1. Confirm the refusal string is absent from Hermes source (see above) → it's upstream.
2. Identify the active model: `grep -nE "^  default:|provider:|base_url:" "$HERMES_HOME/config.yaml"`.
3. Confirm other tasks work (ruling out network/auth): `grep -iE "API call #" "$HERMES_HOME/logs/agent.log" | tail`.
4. If you try to reproduce directly with a script: use Hermes's own User-Agent `hermes-cli/<version>` (from `hermes_cli/__version__`) and the auth.json invoke JWT. A bare `Python-urllib` request to the Nous inference URL returns `error code: 1010` (Cloudflare Browser Integrity Check) — that is a SCRIPT ARTIFACT, not the real agent path, and must NOT be mistaken for the moderation block. The agent itself sends the correct UA and works fine.

### The fix
Switch the default model to one with a lighter/English-oriented safety filter. For a free Nous model that handles Arabic well, `qwen/qwen3-32b:free` is a good default; `meta-llama/llama-3.3-70b-instruct:free` or `google/gemini-2.5-flash:free` are alternatives. Paid Nous models avoid the false blocks entirely.

```bash
hermes config set model.default qwen/qwen3-32b:free
hermes gateway restart
```
Verify: `gateway_state.json` → `running` + `telegram: connected`; `grep -iE "model=qwen" "$HERMES_HOME/logs/agent.log"` shows the new client. Then send a previously-blocked task — it should now complete.

> Note: this model fix is INDEPENDENT of the busy-input `queue` fix above. Both can be needed in the same session.

See `references/debugging-content-moderation.md` for the repro recipes, the Cloudflare-1010 UA pitfall detail, and the known-trigger model list.

## Pitfalls / edge cases
- **Mode values:** `interrupt` (default, aggressive), `queue` (safe, waits), `steer` (injects mid-run via `agent.steer()`). For a personal assistant that gets duplicate/echoed messages, `queue` is the right default.
