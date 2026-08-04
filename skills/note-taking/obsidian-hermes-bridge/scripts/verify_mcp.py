#!/usr/bin/env python3
"""Liveness probe for the obsidian-mcp bridge.
Usage: python verify_mcp.py <vault_path>
Prints INIT_OK, TOOL_COUNT, SEARCH_OK, READ_OK. Exits non-zero on failure.
"""
import subprocess, json, sys, time

NPX = r"C:\Program Files\nodejs\npx.cmd"  # adjust if npx lives elsewhere

def main():
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "D:/document/Dina"
    p = subprocess.Popen([NPX, "-y", "obsidian-mcp", vault_path],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, bufsize=1)
    def send(o):
        p.stdin.write(json.dumps(o) + "\n"); p.stdin.flush()
    def read(timeout=30):
        start = time.time()
        while time.time() - start < timeout:
            line = p.stdout.readline()
            if not line: return None
            line = line.strip()
            if not line: continue
            try: return json.loads(line)
            except: continue
        return None
    send({"jsonrpc":"2.0","id":1,"method":"initialize",
          "params":{"protocolVersion":"2024-11-05","capabilities":{},
                    "clientInfo":{"name":"probe","version":"1.0"}}})
    init = read(30)
    ok_init = bool(init and init.get("result"))
    print("INIT_OK:", ok_init)
    send({"jsonrpc":"2.0","method":"notifications/initialized","params":{}})
    send({"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}})
    tl = read(30)
    names = [t["name"] for t in (tl or {}).get("result",{}).get("tools",[])]
    print("TOOL_COUNT:", len(names))
    # get vault name
    send({"jsonrpc":"2.0","id":3,"method":"tools/call",
          "params":{"name":"list-available-vaults","arguments":{}}})
    v = read(30)
    vault = None
    try:
        for c in v["result"]["content"]:
            if c.get("type") == "text":
                vault = [l.strip() for l in c["text"].splitlines() if l.strip()][-1]
    except Exception:
        pass
    print("VAULT_NAME:", vault)
    ok_search = ok_read = False
    if vault:
        send({"jsonrpc":"2.0","id":4,"method":"tools/call",
              "params":{"name":"search-vault","arguments":{"vault":vault,"query":"Dina"}}})
        s = read(30); ok_search = bool(s and s.get("result"))
        send({"jsonrpc":"2.0","id":5,"method":"tools/call",
              "params":{"name":"read-note","arguments":{"vault":vault,"filename":"📌 Index.md"}}})
        r = read(30); ok_read = bool(r and r.get("result"))
    print("SEARCH_OK:", ok_search)
    print("READ_OK:", ok_read)
    p.terminate()
    sys.exit(0 if (ok_init and len(names) >= 5 and ok_search and ok_read) else 1)

if __name__ == "__main__":
    main()
