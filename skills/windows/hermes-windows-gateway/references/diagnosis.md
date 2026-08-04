# Hermes Gateway Auto-Start Diagnosis & Fix (Windows)

## Symptom
"After I restart my computer the Hermes gateway is not working automatically."
The gateway is reachable only after I manually run something / log in.

## Step 1 — confirm current state
```bash
hermes gateway status
# expect: "Scheduled Task registered: Hermes_Gateway" + maybe "Gateway process running (PID: ...)"
schtasks /query /tn \Hermes_Gateway /v /fo LIST
schtasks /query /tn \Hermes_Gateway /xml
```
Look for:
- `<Triggers>` — only `<LogonTrigger>` present? Then no boot trigger.
- `<LogonType>InteractiveToken</LogonType>` + "Logon Mode: Interactive only".
- The action runs a `.vbs` that uses `sh.Run "...", 0, False` (fire-and-forget).

## Step 2 — check logs for unclean deaths
```bash
grep -iE "lifecycle_ledger|exited UNCLEANLY|exited cleanly|Gateway running with" \
  "$LOCALAPPDATA/hermes/logs/agent.log"
```
A pattern of `exited UNCLEANLY (no exit path ran — SIGKILL / OOM / VM death)` with
short lifetimes means the gateway crashes on boot and nothing restarts it (because
the VBS already returned 0 — see root cause #2 in SKILL.md).

## Step 3 — RULE OUT scale_to_zero (common misdiagnosis)
`hermes config get gateway.scale_to_zero` shows `idle_timeout_minutes: 5`. This does
NOT idle-kill the gateway on a normal install. Scale-to-zero only arms when:
- the env flag `HERMES_SCALE_TO_ZERO` is truthy (check `grep SCALE_TO_ZERO ~/.hermes/.env`),
  AND
- messaging is relay-only/absent.
Direct Telegram/Discord/Slack connections DISARM it. Confirm via source:
```bash
cd "$LOCALAPPDATA/hermes/hermes-agent"
python -c "from gateway.scale_to_zero import scale_to_zero_enabled; print(scale_to_zero_enabled())"
# False => scale_to_zero is OFF for you; do NOT touch this setting.
```
Setting `idle_timeout_minutes: 0` is also a no-op — the parser reverts <=0 to 5.

## Step 4 — Apply the fix
Preferred: `python scripts/harden_gateway_autostart.py`
Manual equivalent:
1. Patch the VBS: change the last arg of `sh.Run` from `False` to `True`.
2. Rebuild the task XML with BootTrigger + LogonTrigger + HighestAvailable.
   - Back up first: `schtasks /query /tn \Hermes_Gateway /xml > backup.xml`
   - Write the XML as **UTF-16** (schtasks requires byte-encoding == declaration).
   - `schtasks /create /tn \Hermes_Gateway /xml Hermes_Gateway.new.xml /f`
   See templates/Hermes_Gateway.vbs and the XML block in scripts/harden_gateway_autostart.py.

## Step 5 — verify
```bash
hermes gateway stop
schtasks /run /tn \Hermes_Gateway
sleep 45
hermes gateway status          # fresh PID + "Gateway running with N platform(s)"
```
For a true reboot test, reboot the machine (not just log off) and check again.
