# Debugging: "interrupted by a user correction" on messaging platforms

## Path resolution
- HERMES_HOME: Linux/macOS `~/.hermes`; Windows `C:\Users\<user>\AppData\Local\hermes`
  (read from `$HERMES_HOME` env if set; this machine resolves to the Windows path).
- Config: `$HERMES_HOME/config.yaml`
- Gateway logs: `$HERMES_HOME/logs/gateway.log`
- Gateway live state: `$HERMES_HOME/gateway_state.json`
- Sessions/request dumps: `$HERMES_HOME/sessions/`

## Command recipes (bash/MSYS on Windows; use absolute paths)
```bash
HERMES_HOME="$(powershell -Command 'echo $env:LOCALAPPDATA')/hermes"  # Windows
# OR on Linux/macOS:
# HERMES_HOME="$HOME/.hermes"

# 1) Confirm the configured mode
grep -n "busy_input_mode" "$HERMES_HOME/config.yaml"

# 2) Prove duplicate delivery — same text at 2+ timestamps, possibly cross-platform
grep -inE "inbound message" "$HERMES_HOME/logs/gateway.log" | tail -40

# 3) Explain the duplicate — network reconnects during a long-poll gap
grep -inE "polling restarted|polling reconnect failed|degraded|Discovering Telegram" \
  "$HERMES_HOME/logs/gateway.log" | tail -20

# 4) Gateway alive + platform connected?
cat "$HERMES_HOME/gateway_state.json" | head -c 350
# After a restart the state file may lag the new PID; confirm the live PID:
#   ps -p <pid> -o pid,cmd=   (Windows: tasklist | grep <pid>)
# and check the log tail for: "Connected to Telegram (polling mode)"
tail -8 "$HERMES_HOME/logs/gateway.log"
```

## Code call chain (for deeper debugging of the gateway source)
- Config knob: `gateway/run.py` `_load_busy_input_mode()` → reads
  env `HERMES_GATEWAY_BUSY_INPUT_MODE` or `display.busy_input_mode`
  (default `"interrupt"`). `interrupt`/`queue`/`steer` are the three values.
- Inbound busy branch: `gateway/run.py` ~line 8503 onward
  (`# Normal busy case (agent actively running a task)`):
  - internal synthetic events (`event.internal`) are deliberately NOT
    interrupt/steer (fall through to queue) — see ~line 8519.
  - `effective_mode == "interrupt"` + TEXT message + running agent →
    `running_agent.redirect(text)` at ~line 8614.
  - `steer` mode → `running_agent.steer(steer_text)` at ~line 8596.
  - `interrupt` is demoted to `queue` when the agent has active subagents
    (`#30170`) or context compression is in flight (`#56391`).
- Redirect impl: `run_agent.py` `AIAgent.redirect()` (~line 3171) sets
  `_interrupt_requested`, aborts the active model request, and stages the
  correction text.
- Scaffold emit: `agent/conversation_loop.py` `_apply_active_turn_redirect()`
  (~line 117) builds the `[This response was interrupted by a user correction.]`
  checkpoint (and `Visible response before the interruption:` if text was on
  screen). It is provider-replay machinery, not user/agent prose; carried in
  `api_content` sidecar, `content` kept clean on normal displays.

## Real-world example (this machine, 2026-08-03)
Telegram log showed the SAME Arabic task text delivered three times:
- 10:11:14 telegram  → starts the turn (session busy)
- 10:14:07 telegram  → duplicate, arrives while busy → read as correction
- 10:14:48 discord   → third echo via linked platform
Network blips at 11:35 (`polling degraded`/`reconnect failed`) confirmed the
redelivery mechanism. Root cause: `busy_input_mode: interrupt` in config.yaml.
Fix applied: `hermes config set display.busy_input_mode queue` +
`hermes gateway restart`; gateway restarted (PID rotated), Telegram reconnected,
startup-queued inbound message drained cleanly.

## Verification after fix
- `grep -n "busy_input_mode" config.yaml` → `  busy_input_mode: queue`
- `gateway_state.json` → `gateway_state: "running"`, `platforms.telegram.state: "connected"`
- `tail` of `gateway.log` → `Connected to Telegram (polling mode)`
- Send a task on Telegram: answer completes with no "interrupted by a user correction" line.
