---
name: obsidian-hermes-bridge
version: 1.0.0
description: Connect an Obsidian vault to Hermes as live knowledge base.
---

# Obsidian ↔ Hermes Bridge

## When to use
- User points at an Obsidian vault and says "install everything", "set up my vault",
  "read my personality / notes and hook them into Hermes", or "turn my routines into cron".
- You need Hermes to query/read/write the user's notes from any conversation.

## Three artifact classes — DO NOT conflate
A vault usually mixes three things; only one is directly Hermes-installable:

1. **Hermes skills** — files named `SKILL.md` (frontmatter `name`/`description`).
   Install by copying into `<hermes_home>/skills/<name>/SKILL.md`. Fix any stale
   paths inside (e.g. `~/Documents/Hafsa` → the real vault path).
2. **Obsidian plugins** — folders under `.obsidian/plugins/`. These are NOT
   Hermes-installable; they only run inside the Obsidian app. Do not copy them into
   Hermes skills. (Optionally, bridge the vault's *content* via MCP — see below.)
3. **External skill repos** — cloned under a research folder (e.g.
   `AI-Skills-Research/`). These are `npx skills add <repo>` installs, not local
   Hermes skills. Don't copy them wholesale.

Also watch for **empty folders** masquerading as skills (e.g. `taste-skill/` with
0 files) — skip them; note them to the user.

## Procedure
### 0. Check what's already installed
Before making any changes, check existing state:
- `grep "mcp_servers" <hermes_home>/config.yaml` — is obsidian-mcp already registered?
- `cronjob action=list` — are vault cron jobs already present?
- `ls <hermes_home>/skills/` — are vault-wiki or persona-system already installed?
If already configured, verify live and skip redundant steps.

### 1. Read persona → memory (not a skill)
Find the identity file (often `@<name>/@<name>.md`, `CLAUDE.md`, or `* Vault.md`).
Read it, then `memory` the durable facts: who the user is, hard rules (e.g. "no
medical advice", "no seafood", "no feminine pronouns for X"), timezone, key
relationships, daily meds/routine. Keep memory compact (≤2.2k chars total).

**Note:** vault-wiki and persona-system skills referenced in CLAUDE.md may be
profile-scoped (e.g. `~/.hermes/profiles/<name>/skills/`). They may not exist
in the current Hermes instance. Check with `ls <hermes_home>/skills/` before
assuming they need installation.

### 2. Install real Hermes skills
Find every `SKILL.md` in the vault. Copy each to `<hermes_home>/skills/<name>/`.
Patch internal paths to the real vault path. Verify the frontmatter is valid.

### 3. Bridge the vault via MCP (the real "plugin" payoff)
Register the `obsidian-mcp` server so Hermes can read/write the vault from any
chat. See `references/mcp_obsidian.md` for the package, launch args, tool list,
and the `vault` name gotcha. **Pitfall:** `hermes config set mcp_servers.X` saves
the value as a quoted STRING and breaks startup — see `references/config_pitfall.md`
for the fix (write nested YAML via yaml.safe_dump). After editing config, **restart
Hermes** (MCP connects at startup). Verify with `scripts/verify_mcp.py`.

**Pitfall:** `verify_mcp.py` has a hardcoded node path `C:\Program Files\nodejs\npx.cmd`.
This won't exist on systems where node is installed elsewhere (e.g. via nvm or
WindowsApps). Use `which npx` or `node -e "console.log(process.execPath)"` to find
the actual path, or update the script's `NPX` variable before running.

### 4. Recreate routines as Hermes cron jobs
Map the vault's routine files (`cron/`, `*-schedule.md`, prayer/meds logs) into
`cronjob` entries. **Check existing cronjobs first** — `cronjob action=list` —
the vault's prior system may already be installed (e.g. prayer med scripts
already in `scripts/`). Prefer one agent-driven job (persona-voiced) over many
`no_agent` scripts when the message should feel personal. For accurate prayer
times, fetch live from `https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5`
(use Python `urllib`, which follows the 302 that bare `curl` mishandles). Deliver
to the user's home channel (already in config.platforms).

## Verification
- Skill installed: `ls <hermes_home>/skills/<name>/SKILL.md`.
- MCP live: run `scripts/verify_mcp.py <vault_path>` → expects 11 tools + a
  successful `search-vault`/`read-note` round trip.
  **Note:** `verify_mcp.py` hardcodes `C:\Program Files\nodejs\npx.cmd`.
  Update the `NPX` variable if node/npx live elsewhere (common on
  Windows with nvm or WindowsApps Python).
- Cron scheduled: `cronjob action=list` shows the new jobs with `state: scheduled`.
- Old routines already present? `cronjob list` + run one (`python <script>.py`)
  BEFORE assuming you must recreate them — the vault's prior system may already be installed.

## Pitfalls (summary)
- `hermes config set` can't write nested dicts → value gets stringified → broken config.
- Obsidian plugins ≠ Hermes skills (different runtimes).
- `obsidian-mcp` tool calls need `vault` = lowercase basename; args are schema-enforced.
- Don't hand-edit config.yaml for the user as a rule — EXCEPT to fix a stringified
  mcp entry, where the safe programmatic fix is `yaml.safe_dump` (see config_pitfall.md).
- aladhan returns HTTP 302; Python `urllib` follows it, bare `curl` may not — use urllib in scripts.

## References
- `references/mcp_obsidian.md` — obsidian-mcp package, tools, gotchas.
- `references/config_pitfall.md` — the `hermes config set` string pitfall + fix.
- `scripts/verify_mcp.py` — re-runnable MCP liveness probe.
