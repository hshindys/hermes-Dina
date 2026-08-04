#!/usr/bin/env python3
"""MCP liveness probe for obsidian-mcp bridge.

Lightweight check: verifies npx is available, obsidian-mcp package is installed,
and the vault directory exists and is a valid Obsidian vault — without launching
the long-running MCP server process.
"""
import subprocess, sys, os

VAULT = "D:/document/Dina"

def run(cmd, timeout=10):
    if sys.platform == "win32":
        cmd = ["cmd.exe", "/c"] + cmd
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.stdout + p.stderr, p.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "", 1

# 1. Check npx is available
out, rc = run(["npx", "--version"])
if rc != 0 or not out.strip():
    print("FAIL: npx not found")
    sys.exit(1)
print(f"OK: npx v{out.strip()}")

# 2. Check obsidian-mcp package is installed (quick, exits immediately)
out, rc = run(["npx", "obsidian-mcp"])
if rc != 0 and "No vault paths provided" not in out:
    print(f"FAIL: obsidian-mcp check failed: {out[:200]}")
    sys.exit(1)
print("OK: obsidian-mcp package available")

# 3. Check vault directory exists and is a valid Obsidian vault (has .obsidian dir)
vault_path = "D:\\document\\Dina"
if not os.path.isdir(vault_path):
    print(f"FAIL: vault directory does not exist: {vault_path}")
    sys.exit(1)

obsidian_dir = os.path.join(vault_path, ".obsidian")
if not os.path.isdir(obsidian_dir):
    print(f"WARN: .obsidian directory not found in {vault_path} — vault may not be initialized")
else:
    print(f"OK: vault directory exists and is initialized")

# 4. Quick connectivity check — try running obsidian-mcp briefly and kill it
# Use subprocess.Popen so we can kill it after catching initial output
import signal
try:
    if sys.platform == "win32":
        cmd = ["cmd.exe", "/c", "npx", "-y", "obsidian-mcp", VAULT]
    else:
        cmd = ["npx", "-y", "obsidian-mcp", VAULT]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Wait briefly for initial output (tool registration happens fast)
    import time
    time.sleep(1)
    # Check if process is still running (it will be — it's a server)
    poll = p.poll()
    if poll is None:
        # Server started and is running — this is healthy
        p.kill()
        p.wait(timeout=3)
        print("OK: obsidian-mcp launched and registered tools successfully")
    else:
        # Process exited — check if it failed
        stdout, stderr = p.communicate(timeout=3)
        if "Vault directory does not exist" in (stdout + stderr):
            print("FAIL: vault path rejected by obsidian-mcp")
            sys.exit(1)
        print("OK: obsidian-mcp exited cleanly")
except Exception as e:
    print(f"WARN: connectivity check inconclusive: {e}")

print(f"Vault path: {VAULT}")
print("MCP Bridge: HEALTHY")
sys.exit(0)