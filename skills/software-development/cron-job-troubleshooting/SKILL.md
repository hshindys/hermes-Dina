---
name: cron-job-troubleshooting
description: Fix Hermes cron job failures and MCP bridge issues.
tags: [hermes, cron, troubleshooting, debugging, mcp, scripts]
---

# Cron Job Troubleshooting

Class-level skill for diagnosing and fixing Hermes cron job failures. Covers script hangs, provider timeouts, fallback chain exhaustion, and MCP bridge health checks.

## Common Failure Modes

### 1. Script Hangs (most common)
A cron script launches a long-running process (e.g., an MCP server that blocks on stdio) and never exits. The cron runner waits for the script to finish, hits the timeout, and reports "provider timeout."

**Root cause:** `subprocess.run()` with `capture_output=True` on a process that becomes a long-running server (e.g., `obsidian-mcp`). The pipe never gets EOF because the server does not exit.

**Fix:** Use `subprocess.Popen` instead of `subprocess.run`, wait briefly for initial output, then kill the process. Or restructure the check to avoid launching the server at all.

### 2. Fallback Chain Exhausted
The cron job has no fallback when the primary script fails. The error message says "Fallback chain was exhausted or unavailable."

**Fix:** Ensure the script has a clear exit path (exit 0 on success, exit 1 on failure). Add a timeout wrapper around the script execution.

### 3. Command Not Found in Cron Environment
Cron jobs run in a minimal environment — `PATH` may not include `npx`, `python`, or other tools.

**Fix:** Use absolute paths or wrap commands in `cmd.exe /c` on Windows. Test with `which <command>` in the cron workdir.

### 4. Windows Path Mangling
MSYS/bash on Windows can double-rewrite paths (e.g., `/d/Backup` becomes `C:\d\Backup`).

**Fix:** Always use native Windows paths (`C:/Users/...` or `D:/document/...`) in scripts, never POSIX-style paths that start with `/d/` or `/c/`.

## Workflow
1. Read the cron job output file in `~/.hermes/cron/output/<job_id>/`
2. Check the script's exit code and stderr
3. Identify the failure mode (hang, not-found, path error, provider timeout)
4. Apply the fix from the relevant reference
5. Re-run the script manually to verify
6. Wait for the next cron tick to confirm the fix persists

## Gateway Process Not Running (Telegram/Discord/Slack bot not responding)
The Hermes gateway process manages all messaging platform connections. If a platform (especially Telegram) stops responding, the gateway may have died.

**Diagnosis:**
- Check if gateway is running: `ps aux | grep "gateway run"`
- Check the lifecycle ledger for crash cause: `cat ~/.hermes/gateway/restart_loop.json`
- Check logs for OOM/crash: `grep "SIGKILL\|OOM\|VM death\|exited UNCLEANLY" ~/.hermes/logs/gateway.log | tail -5`
- Check Telegram connection status: `grep "telegram connected\|telegram disconnected\|Connecting to Telegram" ~/.hermes/logs/gateway.log | tail -10`

**Fix:**
```bash
# Restart the gateway (from Hermes home directory)
hermes gateway run --replace
```

**Pitfall:** On Windows, the gateway can be killed by the OS when memory is low. The lifecycle ledger records `SIGKILL / OOM / VM death` when this happens. Always use `--replace` to clear the stale PID before restarting.

## References
- `references/mcp-bridge-debugging.md` — MCP bridge health check fix (obsidian-mcp stdio server hang)
- `references/session-manager-integration.md` — Session manager + weather integration pattern
- `references/showtime-skill.md` — showtime.py: Cairo time + weather + session status in one script

## Pitfall: subprocess.run on stdio servers
Never use `subprocess.run()` with `capture_output=True` on a process that becomes a long-running server (e.g., `obsidian-mcp`). The pipe never gets EOF and the call hangs forever. Use `subprocess.Popen` with a brief wait, then kill the process.
