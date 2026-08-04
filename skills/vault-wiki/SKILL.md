---
name: vault-wiki
description: Read, search, and write across all Obsidian vaults connected to Hermes. Use whenever the user refers to their vault, second brain, knowledge base, or asks about vault content. Always load when the Dina/Hafsa persona is active and needs to read or update vault notes.
platforms: [linux, macos, windows]
---

# Vault Wiki

Read-write access to all Obsidian vaults connected to Hermes. Uses the obsidian-mcp MCP server (registered in config.yaml).

## Vault Path

The active vault for this instance is **Dina**: `D:/document/Dina`
Vault name (MCP parameter): `dina`

## When to Use
- User asks about vault content, notes, or files
- Creating, editing, or searching notes in any vault
- Cross-vault queries when multiple vaults are registered
- Daily vault health checks

## MCP Tools (11 tools, all prefixed `mcp_obsidian_*`)
| Tool | Args | Use |
|------|------|-----|
| `list-available-vaults` | — | List registered vaults |
| `read-note` | vault, filename, folder? | Read a note |
| `search-vault` | vault, query, path?, caseSensitive?, searchType? | Search vault content |
| `create-note` | vault, filename, content, folder? | Create a new note |
| `edit-note` | vault, filename, old_string, new_string | Targeted edit |
| `move-note` | vault, filename, new_path | Move/rename a note |
| `delete-note` | vault, filename | Delete a note |
| `create-directory` | vault, dirname | Create a folder |
| `add-tags` | vault, filename, tags | Add frontmatter tags |
| `remove-tags` | vault, filename, tags | Remove tags |
| `rename-tag` | vault, old, new | Rename a tag across vault |

## Key Rules
- `vault` param = lowercase basename (e.g. `dina` for `D:/document/Dina`)
- Pass folder path as `folder` arg when needed (e.g. `@دينا`)
- All write operations go through MCP — never edit vault files directly from terminal
- For vault health, check that the vault path exists and vault name resolves

## Vault Structure (Dina)
```
@دينا/          ← Identity (persona, routine, goals, values)
cron/            ← Python scripts for prayers, meds, reminders
AI-Skills-Research/  ← Cloned skill repos (many empty — unpulled)
📌 Index.md     ← Master index
🧠 Dina Vault.md   ← Vault router
04-System/       ← System tools & audits
```

## Search Strategy
1. For filename lookup: `search-vault` with `searchType: "filename"`
2. For content lookup: `search-vault` with `searchType: "content"`
3. Use `read-note` to read any file found
4. For vault-wide stats, use `search-vault` with a broad query and count results

## Writing Notes
- Every new note should have YAML frontmatter with `created`, `updated`, `tags`
- Add the note to `📌 Index.md` if it belongs in the main index
- Use `edit-note` for appending to existing notes (find stable anchor)
