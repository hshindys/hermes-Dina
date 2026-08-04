---
name: cron-job-debugging
description: Debug Hermes cronjob failures on Windows timeouts
tags: [debugging, cron, troubleshooting, windows]
---

# Cron Job Debugging — Hermes

## When to Use
Use when a Hermes cron job reports provider timeout, fallback chain exhaustion, script failure, or unexpected exit codes. This is the go-to workflow for diagnosing scheduled script failures in Hermes on Windows.

## Root Cause Categories

### 1. Script Blocks on Long-Running Process (Most Common)
MCP bridge scripts launch npx obsidian-mcp as a stdio server that never exits. Python subprocess.run(timeout=N) should kill the child and raise TimeoutExpired, but on Windows with cmd.exe /c wrappers the behavior is unreliable. The Windows timeout command kills the outer process but not grandchild processes. capture_output=True causes pipes to buffer indefinitely if the child never closes stdout/stderr.

**Fix:** Use subprocess.Popen with a sleep + p.kill() instead of subprocess.run with timeout. Or avoid launching the server entirely — do a lightweight pre-check.

### 2. PATH/Environment Mismatch
Cron scripts run in a minimal environment. npx, node, or other tools may not be on PATH from the cron workdir even though they work in an interactive terminal.

**Fix:** Use absolute paths in scripts (C:/Program Files/nodejs/npx), or cmd.exe /c wrappers on Windows for .cmd/.bat files.

### 3. Vault Path or Config Issue
If the script depends on a vault path or config file, verify it exists from the cron workdir context (not just the session working directory).

## Diagnosis Workflow

1. Read the cron output file in ~/AppData/Local/hermes/cron/output/<job_id>/
2. Check if any .md file shows Script timed out or non-zero exit code
3. Read the script source to identify blocking calls
4. Test the script manually with the same workdir the cron job uses
5. Apply the fix and re-run to confirm clean exit within seconds

## Fix: Lightweight MCP Bridge Check
Do not launch the full MCP server in a health probe. Instead:
1. Check npx --version works
2. Run npx obsidian-mcp with no vault args — exits immediately with usage info
3. Verify the vault directory exists and has .obsidian/
4. Optionally: launch server briefly with Popen + sleep + kill for connectivity check

## Example: Fixed verify_mcp.py Pattern (see references/verify_mcp.py)
Use subprocess.Popen with a brief sleep and p.kill() for any process that starts a server, or skip server launch entirely and rely on pre-checks. The script should exit in under 10 seconds and return code 0 when healthy.

### Detailed Fix: verify_mcp.py Reference
See `references/verify_mcp.py` for the full rewritten script with:
1. Lightweight pre-checks (npx version, obsidian-mcp no-args, vault existence)
2. Optional Popen+kill connectivity check
3. Proper handling of Windows subprocess timeout behavior

### Detailed Fix: verify_mcp.py Reference
See `references/verify_mcp.py` for the full rewritten script with:
1. Lightweight pre-checks (npx version, obsidian-mcp no-args, vault existence)
2. Optional Popen+kill connectivity check
3. Proper handling of Windows subprocess timeout behavior