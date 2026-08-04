#!/usr/bin/env python3
"""Nadi Al-Ahly Competition Standings Fetcher.
Reads local Competition markdown files and extracts standings/position info.
Usage: ahly_standings.py [competition]  (competition = premier|caf|cups|all)
"""
import sys, os

VAULT = "D:/document/Nadi Al-Ahly"
COMPS_DIR = os.path.join(VAULT, "Competitions")

COMP_FILES = {
    "premier": "Premier-League.md",
    "caf": "CAF-Champions-League.md",
    "cups": "Cup.md",
    "dashboard": "Dashboard 1.md",
}

def read_standings(comp_file, comp_name):
    path = os.path.join(COMPS_DIR, comp_file)
    if not os.path.exists(path):
        return f"❌ {comp_name}: file not found\n"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return f"\n📋 {comp_name}:\n{content}\n"

def build_message(comp_filter="all"):
    L = ["🏆 Nadi Al-Ahly — Competition Standings"]
    L.append(f"(generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')} Cairo)")
    L.append("-------------")
    
    if comp_filter == "all":
        for key, fname in COMP_FILES.items():
            L.append(read_standings(fname, key.upper()))
    elif comp_filter in COMP_FILES:
        L.append(read_standings(COMP_FILES[comp_filter], comp_filter.upper()))
    else:
        available = ", ".join(COMP_FILES.keys())
        L.append(f"❌ Unknown competition '{comp_filter}'. Available: {available}")
        L.append("Usage: ahly_standings.py [premier|caf|cups|dashboard|all]")
    
    return "\n".join(L)

if __name__ == "__main__":
    comp = sys.argv[1] if len(sys.argv) > 1 else "all"
    print(build_message(comp))
