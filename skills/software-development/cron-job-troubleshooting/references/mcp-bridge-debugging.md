# MCP Bridge Debugging — obsidian-mcp Health Check Fix

## Problem
The `MCP Bridge Health Check` cron job (job_id: `7509c13a4422`) was failing with "provider timeout" because `verify_mcp.py` launched `obsidian-mcp` as a long-running stdio server and called `subprocess.run()` with `capture_output=True`. The server never exits (it blocks on stdio), so `subprocess.run()` hangs until the outer timeout kills it — or worse, the fallback chain exhausts.

## Root Cause
`obsidian-mcp` is a stdio server: it starts, registers tools, then blocks waiting for JSON-RPC messages. `subprocess.run()` waits for the process to exit, which never happens.

## Fix Applied to `~/.hermes/scripts/verify_mcp.py`

The script was rewritten to:
1. Check `npx --version` (quick, exits)
2. Check `obsidian-mcp` package is available (runs `npx obsidian-mcp` with no args — exits immediately with usage text)
3. Validate vault directory exists and has `.obsidian` folder
4. Launch obsidian-mcp via `subprocess.Popen`, wait 1 second for tool registration output, then `p.kill()` cleanly

## Verification
```bash
timeout 10 python ~/.hermes/scripts/verify_mcp.py
# Expected output:
# OK: npx v11.16.0
# OK: obsidian-mcp package available
# OK: vault directory exists and is initialized
# OK: obsidian-mcp launched and registered tools successfully
# Vault path: D:/document/Dina
# MCP Bridge: HEALTHY
```

## Key Insight
On Windows, `npx` is a `.cmd`/`.bat` file that requires `cmd.exe /c` to be found properly. The `subprocess.run` call must use `["cmd.exe", "/c", "npx", ...]` on Windows. The Python venv's `python` binary is at `~/AppData/Local/hermes/hermes-agent/venv/Scripts/python`, not the system `python`.