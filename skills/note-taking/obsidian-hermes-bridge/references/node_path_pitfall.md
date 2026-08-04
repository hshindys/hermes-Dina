# Node/npx Path Pitfall for verify_mcp.py

## Symptom
`verify_mcp.py` hardcodes `NPX = r"C:\Program Files\nodejs\npx.cmd"`.
On systems where Node is installed elsewhere (nvm, WindowsApps, Scoop,
standalone install), this path doesn't exist and the script fails with
`FileNotFoundError`.

## Fix
Before running, find the actual npx path:
```bash
which npx
# or
node -e "console.log(require('child_process').execSync('where npx').toString().trim())"
```
Then edit `verify_mcp.py` and change the `NPX` variable to the real path.

## Common Windows locations
- Standard: `C:\Program Files\nodejs\npx.cmd`
- WindowsApps (Microsoft Store Node): `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\npx`
  (but this is a stub that redirects to `npx.cmd — often fails in heredocs)
- nvm-windows: `C:\Users\<user>\AppData\Roaming\nvm\v<ver>\npx`
- Scoop: `~\scoop\apps\nodejs\current\npx.cmd`

## Also affects
Any script that invokes `npx` or `node` directly. Prefer `uv run` or
the Hermes venv Python (`~/AppData/Local/hermes/hermes-agent/venv/bin/python`)
for Python-based probes when available.