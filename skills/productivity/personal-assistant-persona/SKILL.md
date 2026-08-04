---
name: personal-assistant-persona
description: Build a persona skill and daily cron reminders from a vault.
---

# Personal Assistant Persona — from vault to Hermes

Turn a persona defined in notes / Obsidian into (a) a loadable Hermes **persona skill** and (b) **automated cron reminders** for that persona's daily routine.

## When to use
- User points at a folder like `D:\document\Dina` / `~/Documents/Hafsa` and says "extract the skills/persona/routines", "build my assistant".
- "Build the Dina persona", "make Hafsa real", "set up daily reminders from my routine".
- Vault shows the router pattern: `CLAUDE.md` or `🧠 <Vault>.md` + `@<Name>/@<Name>.md` (identity/voice/rules) + a routine md.

## Workflow

### 1. Map the vault (don't assume the obvious path is live)
- Read the vault's **router file first** (`CLAUDE.md` / `🧠 Dina Vault.md`) — it tells you where persona / routine / skills live, and may reference OTHER vaults (e.g. `~/Documents/Hatem Nad/`).
- Persona usually in `@<Name>/@<Name>.md` (identity, voice, hard rules) + a routine md.
- Sizing a big vault: `du -sh` **times out** on vaults with many small files — use a bounded `os.walk` in Python instead (see references/windows-msys-hermes-cli-pitfalls.md).

### 2. Author the persona skill
- Create `~/AppData/Local/hermes/skills/<persona>/SKILL.md` with: identity, personality/voice, nicknames, emoji style, and explicit **HARD RULES** (e.g. no seafood, no medical advice, grammatical gender rules). See `templates/persona_skill.md`.
- Keep it self-contained; the agent BEcomes the persona when the skill is loaded. State clearly when to switch back to default Hermes.

### 3. Extract routines → cron reminders AND daily routine scripts
- Identify recurring events: prayers, meds, workouts, check-ins.
- **Daily routine script** (`daily_routine.py`): reads a TOML config, fetches prayer times from Aladhan API, builds a schedule, upserts into the vault daily note. Registered as a `--no-agent --script` cron job (see below).
- **Cron reminders**: Build small `--no-agent --script` Python scripts under `~/AppData/Local/hermes/scripts/` that print reminder text (verbatim delivery, no LLM).
- Register all cron jobs: `hermes cron create "<cron expr>" --name "..." --deliver <platform>:<chat_id> --no-agent --script <bare_filename.py>`.
- `--script` MUST be a **bare filename** under `~/.hermes/scripts/` — absolute or `$HOME`-relative paths are rejected by the Hermes cron system.
- Use fixed cron times from a known schedule; for prayer times that drift daily, fetch live times (see references/prayer-times-aladhan.md), or use the `daily_routine.py` pattern (Aladhan API + cache).

### 4. Discord bot configuration (platform integration)
When the persona bot needs to read messages in a Discord channel **without requiring `@mention`** (e.g. Dina in `#دينا`):
- Add `require_mention: false` under the `discord:` section of `~/.hermes/config.yaml`.
- Alternative: use `free_response_channels` — a comma-separated list of channel IDs where the bot responds without mention (set via `DISCORD_FREE_RESPONSE_CHANNELS` env var or `discord.extra.free_response_channels` in config).
- **Restart the Discord bot process** after config changes — they do NOT hot-reload.
- When `require_mention: false`, the bot reads ALL messages in server channels it has access to. Be mindful of rate limits and message volume.

### 5. Verify before declaring done
- Run each script directly with a **native Windows path** (`python C:/Users/.../script.py`) — NOT an MSYS path (`/c/...`), which double-prefixes to `C:\\c\\...`.
- `hermes cron list` should show the jobs active with correct "Next run" times.
- For `daily_routine.py`: confirm it writes to cache/pending on first run if vault path doesn't yet exist (expected fallback), then verify vault writes once the vault path is configured.

## Pitfalls (Windows / MSYS + Hermes CLI) — READ FIRST
All of these cost real time in one session. Exact transcripts + fixes in `references/windows-msys-hermes-cli-pitfalls.md`:
- `hermes backup -o` / output paths: MSYS `/d/Backup/...` → `C:\d\...` phantom. Use Windows-style `D:/Backup/...`.
- `--script` wants a bare filename; never pass a path.
- MSYS `/c/...` passed to Windows `python` becomes `C:\\c\\...`. Inside scripts use `os.path.abspath(__file__)`; call python with `C:/...`.
- `curl` on MSYS can fail writing to `/tmp` ("client returned ERROR on write") — use Python `urllib`.
- `du -sh` on large vaults times out — use bounded `os.walk`.
- In a batched bash block of `hermes cron create`, one job can fail with `unrecognized arguments` — re-run the single failing job on its own line.

### Cron job script-resolution failures (4 patterns)
When `hermes cron list` shows `last_status: error` for script-based jobs, check these in order:

1. **Script not in `scripts/`** — the cron system only looks in `~/.hermes/scripts/`. If a script lives elsewhere (e.g. `~/.hermes/scripts/` vs `~/AppData/Local/hermes/scripts/`), copy or symlink it. The error message is `Script not found: C:\Users\<user>\AppData\Local\hermes\scripts\<name>`.

2. **Shell binary not found on Windows** — `npx`, `bash`, `node` may be `.cmd`/`.bat` files that `subprocess.run(["npx", ...])` cannot resolve on Windows. Fix: rewrite the script to call `cmd.exe /c <command>` on Windows (see `verify_mcp.py` pattern), or ensure the script's interpreter is found via `shutil.which` before calling `subprocess`.

3. **Arguments baked into script name** — `--script "ahly_standings.py all"` treats the whole string as a filename. The cron system does NOT split on spaces. Fix: put the default argument inside the script itself (most scripts default to `all` when no arg is given), or create a thin wrapper script that sets `sys.argv`.

4. **Shell command in `script` field** — storing `cd /path && JF_URL=... node cli.js scan` in the `script` field fails because the entire string is used as a filename. Fix: create a wrapper `.sh` (or `.py`/`.bat`) script in `scripts/` that contains the command logic, then point the cron job at the wrapper filename with a `workdir` set to the script's working directory.

## Security
- Vault `data.json` / `.env` may contain live API keys + TLS private keys (e.g. Obsidian Local REST API). Treat as secrets: **never paste them back into chat**. Ask before wiring any connection that uses them.

## References & templates
- `references/daily-routine-builder.md` — pattern for auto-generating a daily routine script (TOML config → Aladhan API → vault upsert).
- `references/windows-msys-hermes-cli-pitfalls.md` — exact error transcripts + fixes.
- `references/prayer-times-aladhan.md` — live prayer-time API.
- `references/cron-script-resolution-failures.md` — 4 recurring cron script-resolution failure patterns with transcripts and fixes.
- `templates/persona_skill.md` — starter SKILL.md for a new persona.
- `templates/cron_reminder_script.py` — generic `--no-agent` reminder script pattern.
