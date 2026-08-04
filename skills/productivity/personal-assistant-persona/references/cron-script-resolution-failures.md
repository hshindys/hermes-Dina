# Cron Job Script-Resolution Failures — Diagnostic Reference

Captured during the 2026-07-30 cron fix session (Hatem's Dina vault, Windows host).
Four cron jobs failed with distinct root causes. Each pattern below includes the exact error transcript and the fix applied.

## Pattern 1: Script Not in `scripts/` Directory

**Job:** Daily Spiritual Routine Builder (`6eb8a800d5e1`)
**Error:** `Script not found: C:\Users\hshin\AppData\Local\hermes\scripts\daily_routine.py`
**Root cause:** `daily_routine.py` lived at `~/.hermes/scripts/` (user home), not `~/AppData/Local/hermes/scripts/` (Hermes home). The cron system resolves all `--script` paths relative to Hermes's `scripts/` directory.
**Fix:** Copied the file from `~/.hermes/scripts/daily_routine.py` to `~/AppData/Local/hermes/scripts/daily_routine.py`.

## Pattern 2: Shell Binary Not Found on Windows (`npx` is `.cmd`)

**Job:** MCP Bridge Health Check (`7509c13a4422`)
**Error:** `FileNotFoundError: [WinError 2] The system cannot find the file specified` from `subprocess.run(["npx", "-y", "obsidian-mcp", VAULT])`
**Root cause:** On Windows, `npx` is `npx.cmd` — a batch file, not a binary. `subprocess.run(["npx", ...])` uses `CreateProcessW` which does not resolve `.cmd`/`.bat` extensions the way a shell would. The working Python (`python.exe`) was found because `.exe` is in `PATHEXT`, but `.cmd` is not resolved by the raw `CreateProcessW` call.
**Fix:** Rewrote `verify_mcp.py` to call `cmd.exe /c npx -y obsidian-mcp D:/document/Dina` on Windows (`sys.platform == "win32"`). On POSIX, it still calls `npx` directly.

## Pattern 3: Arguments Baked Into Script Name

**Job:** Al-Ahly Standings (`8e2b6b947518`)
**Error:** `Script not found: C:\Users\hshin\AppData\Local\hermes\scripts\ahly_standings.py all`
**Root cause:** The `--script` argument was `ahly_standings.py all` — the cron system treats the entire string as a filename. It does NOT split on spaces to separate script name from arguments.
**Fix:** Changed `script` to `ahly_standings.py` (the script already defaults to `all` when no CLI arg is given — see `sys.argv[1] if len(sys.argv) > 1 else "all"`). Added `workdir` pointing to the Hermes home directory.

## Pattern 4: Shell Command in `script` Field

**Job:** Jellyfin library scan (`aeef21cc2f6a`)
**Error:** `Script not found: C:\Users\hshin\AppData\Local\hermes\scripts\cd \c\Users\hshin\AppData\Local\hermes\skills\jellyfin-control && JF_URL=http:\localhost:8096 ...`
**Root cause:** A full shell command (`cd /path && JF_URL=... node cli.js scan`) was stored in the `script` field. The cron system treats the entire string as a filename to resolve, not a shell command to execute.
**Fix:** Created a wrapper shell script `scripts/jellyfin_scan.sh` containing the command logic, and pointed the cron job's `script` at `jellyfin_scan.sh` with a `workdir` set to `C:\Users\hshin\AppData\Local\hermes`.

## Verification Checklist
After fixing a broken cron job:
1. Run the script manually: `python C:/Users/hshin/AppData/Local/hermes/scripts/<name>.py` or `bash scripts/<name>.sh` from `C:\Users\hshin\AppData\Local\hermes`.
2. Confirm the output is correct (check for stdout content and exit code 0).
3. Wait for the next scheduled run, or check `hermes cron list` to confirm `last_status` flips from `error` to `ok`.

## Key Path Reference
- Hermes scripts directory: `C:\Users\hshin\AppData\Local\hermes\scripts\` — this is the ONLY directory the cron system searches for `--script` files.
- Hermes config: `C:\Users\hshin\AppData\Local\hermes\config.yaml`
- User home (NOT Hermes home): `C:\Users\hshin\` — do not confuse with Hermes home above.
- Legacy user scripts (pre-migration): `C:\Users\hshin\.hermes\scripts\` — check here if a script is missing from Hermes's scripts dir.