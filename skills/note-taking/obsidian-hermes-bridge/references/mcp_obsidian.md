# obsidian-mcp — package, tools, gotchas

## Package
- npm: `obsidian-mcp` (v1.0.6 at time of writing).
- It is a **filesystem-based** MCP server: it reads/writes the vault's markdown
  directly. The Obsidian app does NOT need to be running (unlike obsidian-local-rest-api).
- Launch style: `npx -y obsidian-mcp <vault_path>` where `<vault_path>` is a
  positional arg that MUST exist (the server validates it at startup and errors
  `Vault directory does not exist: ...` if missing). Forward slashes work on Windows.

## Hermes registration (config.yaml)
```yaml
mcp_servers:
  obsidian:
    command: "npx"
    args: ["-y", "obsidian-mcp", "D:/document/Dina"]
    timeout: 120
    connect_timeout: 60
```
MCP connects at Hermes **startup** — restart Hermes after registering. Tools appear
prefixed `mcp_obsidian_*`.

## Tools (11, confirmed live)
create-note, list-available-vaults, edit-note, search-vault, move-note,
create-directory, delete-note, add-tags, remove-tags, rename-tag, read-note.

## GOTCHAS
1. **`vault` parameter** — most tools require `vault` = the lowercase basename of
   the vault directory. Get it from `list-available-vaults` (returns e.g. `dina`).
   Passing the path or wrong name → `Unknown vault: ...`.
2. **Schema-enforced args** — wrong/unrecognized keys are rejected with
   `-32602 Invalid arguments`. Known schemas:
   - search-vault: required `[vault, query]`; optional `[path, caseSensitive, searchType]`
   - read-note: required `[vault, filename]`; optional `[folder]`
   - create-note: required `[vault, filename, content]`; optional `[folder]`
   - list-available-vaults: no args
3. **aladhan API for prayer times** returns HTTP 302. Use Python `urllib` (follows
   redirect); bare `curl` may return empty/302. Endpoint:
   `https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5`
   → `json["data"]["timings"]` and `json["data"]["date"]["readable"]`.
