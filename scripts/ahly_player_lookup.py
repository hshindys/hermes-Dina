#!/usr/bin/env python3
"""Nadi Al-Ahly Player Lookup.
Usage: ahly_player_lookup.py <PLAYER_NAME>   (English, Arabic, or number like #10)
Reads frontmatter (name, name_en, number, position, nationality) from player markdown files.
"""
import sys, os, glob, re

VAULT = "D:/document/Nadi Al-Ahly"
PLAYERS_DIR = os.path.join(VAULT, "Players")

def parse_frontmatter(content):
    """Extract YAML frontmatter from a markdown file's content."""
    fm = {}
    if not content.startswith("---"):
        return fm
    parts = content.split("---")
    if len(parts) < 3:
        return fm
    fm_text = parts[1]
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("-"):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm

def find_player(query):
    """Find a player file by name, number, or english name."""
    query_lower = query.lower().strip()
    
    # Remove leading # if user typed #10
    q_clean = query_lower.lstrip("#").strip()
    
    for fpath in sorted(glob.glob(os.path.join(PLAYERS_DIR, "*.md"))):
        basename = os.path.basename(fpath)
        if basename.endswith(".excalidraw") or "ميزات" in basename:
            continue
        
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        fm = parse_frontmatter(content)
        
        # Build searchable strings from frontmatter
        name_ar = fm.get("name", "").lower()
        name_en = fm.get("name_en", "").lower()
        number = fm.get("number", "")
        
        # Match checks
        if q_clean in name_ar or q_clean in name_en:
            return fpath, fm
        if q_clean == number:
            return fpath, fm
        # Partial number match (e.g., "10" matches "#10")
        if q_clean.replace(".", "") in number or number in q_clean:
            return fpath, fm
        # Check if query is a substring of the filename (e.g., "sharif" in "10-mohamed-sharif")
        fname_no_ext = os.path.splitext(basename)[0].lower()
        if q_clean in fname_no_ext or fname_no_ext in q_clean:
            return fpath, fm
    
    return None, None

def build_player_card(fpath, fm):
    """Build a nice player card from frontmatter."""
    if not fpath:
        return ""
    
    basename = os.path.basename(fpath)
    name = fm.get("name", basename)
    name_en = fm.get("name_en", "")
    number = fm.get("number", "")
    position = fm.get("position", "")
    nationality = fm.get("nationality", "")
    joined = fm.get("joined", "")
    role = fm.get("role", "")
    
    L = []
    L.append(f"⚽ {name}")
    if name_en:
        L.append(f"({name_en})")
    L.append(f"#{number}" if number else "")
    L.append(f"Position: {position}" if position else "")
    L.append(f"Nationality: {nationality}" if nationality else "")
    L.append(f"Joined: {joined}" if joined else "")
    if role:
        L.append(f"Role: {role}")
    L.append("")
    
    # Read first few lines of content (skip frontmatter)
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Find the first ## or ### heading after frontmatter
    content_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("---") and i > 0:
            content_start = i + 1
            break
    
    for line in lines[content_start:content_start+15]:
        stripped = line.strip()
        if stripped and not stripped.startswith("---") and not stripped.startswith("type:"):
            # Remove leading ## 
            heading = stripped.lstrip("#").strip()
            if heading:
                L.append(heading)
        if len([x for x in L if x]) > 20:
            break
    
    return "\n".join([x for x in L if x])

def build_message(query):
    player_file, fm = find_player(query)
    L = ["🦅 Nadi Al-Ahly — Player Lookup", f"Query: {query}", "-------------"]
    
    if player_file and fm:
        L.append(build_player_card(player_file, fm))
    else:
        L.append("❌ Player not found. Check the spelling (English or Arabic).")
        L.append("")
        L.append("💡 Try:")
        L.append('   • "ahly look up Mohamed Sherif"')
        L.append('   • "ahly look up #10"')
        L.append('   • "ahly look up تريزيجيه"')
        L.append('   • "ahly look up 7"')
    
    return "\n".join(L)

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Mohamed Sherif"
    print(build_message(query))
