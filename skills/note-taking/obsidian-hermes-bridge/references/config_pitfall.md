# Pitfall: `hermes config set` stringifies nested values

## Symptom
After running:
```
hermes config set mcp_servers.obsidian '{"command":"npx",...}'
```
the value is stored as a **quoted YAML string**, not a nested mapping:
```yaml
mcp_servers:
  obsidian: '{"command": "npx", "args": [...]}'
```
This breaks MCP discovery at startup (Hermes can't parse a string as a server config).

## Why
`hermes config set <key> <value>` stores `<value>` as a literal scalar, not parsed
YAML. Nested dicts can't be passed this way.

## Fix (the one safe exception to "never hand-edit config.yaml")
Edit config.yaml programmatically with a Python yaml round-trip — never by hand-editing
indentation. From the terminal (bash/PS via git-bash):
```bash
cd "$LOCALAPPDATA/hermes"   # or $APPDATA/hermes on some setups
python - <<'PY'
import yaml
p = "config.yaml"
cfg = yaml.safe_load(open(p, encoding="utf-8"))
cfg["mcp_servers"] = {
    "obsidian": {
        "command": "npx",
        "args": ["-y", "obsidian-mcp", "D:/document/Dina"],
        "timeout": 120,
        "connect_timeout": 60,
    }
}
yaml.safe_dump(cfg, open(p, "w", encoding="utf-8"),
               allow_unicode=True, sort_keys=False, default_flow_style=False)
PY
```
Then validate and restart Hermes:
```bash
python -c "import yaml; yaml.safe_load(open('config.yaml',encoding='utf-8')); print('OK')"
```

## Note
The general rule "never hand-edit config.yaml" still holds; this programmatic
yaml.safe_dump fix is the sanctioned way to repair a stringified MCP entry that
`hermes config set` produced.
