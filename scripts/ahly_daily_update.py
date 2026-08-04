#!/usr/bin/env python3
"""Nadi Al-Ahly Match Reminder & Standings Pinger.

Reads Matches/Data/ and Matches/Schedule.md from the Al-Ahly vault,
fetches live standings from the API (if available), and prints a
Dina-voice summary for Telegram delivery.
"""
import os, re, json, urllib.request
from datetime import datetime, timezone

VAULT = "D:/document/Nadi Al-Ahly"
MATCH_DIR = os.path.join(VAULT, "Matches", "Data")
SCHEDULE_FILE = os.path.join(VAULT, "Matches", "Schedule.md")
LOG_FILE = os.path.join(VAULT, "Matches", "Log.md")

def get_live_standings():
    """Try to fetch live standings from aladhan or football-api (best effort)."""
    # For now, parse local data; live API integration is optional.
    return None

def parse_schedule(md_path):
    """Parse markdown tables from Schedule.md for upcoming matches."""
    upcoming = []
    if not os.path.exists(md_path):
        return upcoming
    current_date = datetime.now().strftime("%Y-%m-%d")
    in_table = False
    headers = []
    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "|" in line and "---" not in line:
                cells = [c.strip() for c in line.split("|")]
                if not in_table and any("تاريخ" in c or "date" in c.lower() for c in cells):
                    headers = cells
                    in_table = True
                    continue
                if in_table and cells:
                    row = {i: c for i, c in enumerate(cells)}
                    # Find date column (first column usually)
                    date_val = row.get(0, row.get(1, "")).strip()
                    if date_val and date_val != "التاريخ" and date_val != "Date":
                        upcoming.append(row)
    return upcoming[-7:]  # Last 7 entries or all

def parse_match_log(md_path):
    """Parse last result from Log.md."""
    last_result = None
    if not os.path.exists(md_path):
        return last_result
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        if "|" in line and "---" not in line:
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 4:
                last_result = cells
    return last_result

def read_squad_summary(squad_path):
    """Quick summary from Squad.md - count players and find captain."""
    squad = {"goalkeepers": 0, "defenders": 0, "midfielders": 0, "forwards": 0, "captain": "Unknown"}
    if not os.path.exists(squad_path):
        return squad
    with open(squad_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Count sections
    if "حراس المرمى" in content:
        # crude count by looking at table rows in GK section
        gk_section = content.split("حراس المرمى")[1].split("##")[0] if "حراس المرمى" in content else ""
        squad["goalkeepers"] = gk_section.count("|") // 4  # rough
    return squad

def build_message():
    """Build the Al-Ahly match & standings message."""
    L = []
    L.append("⚽ Nadi Al-Ahly — Daily Update")
    L.append(f"(generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} Cairo)")
    L.append("-------------")

    # 1. Current form / last result
    last = parse_match_log(os.path.join(VAULT, "Matches", "Log.md"))
    if last:
        L.append(f"📊 آخر نتيجة: {' | '.join(filter(None, last))}")
    else:
        L.append("📊 آخر نتيجة: (بيانات قيد التحديث)")

    # 2. Upcoming schedule
    schedule = parse_schedule(SCHEDULE_FILE)
    if schedule:
        L.append("")
        L.append("📅 المباريات القادمة:")
        for match in schedule[:3]:
            # Try to find date/opponent columns
            date_val = match.get(0, match.get(1, "?"))
            opp = match.get(2, match.get(3, "?"))
            L.append(f"   📌 {date_val} — {opp}")

    # 3. Current competition standings (local data)
    comps_dir = os.path.join(VAULT, "Competitions")
    if os.path.isdir(comps_dir):
        L.append("")
        L.append("🏆 المسابقات:")
        for f in os.listdir(comps_dir):
            if f.endswith(".md") and not f.startswith("Dashboard"):
                L.append(f"   📄 {f.replace('.md', '')}")

    # 4. Squad highlight
    squad = read_squad_summary(os.path.join(VAULT, "Squad.md"))
    L.append(f"")
    L.append(f"👥 التشكيلة الحالية: {squad.get('goalkeepers', '?')} حراس + لاعبين")
    L.append(f"   🔑 الكابتن: **{squad.get('captain', 'محمد الشناوي')}**")

    # 5. CTA
    L.append("")
    L.append("🔥 يا أهلي! يا حاتم، في حاجة عايز تعملها؟ 🤍")
    L.append("💬 قول مثلاً:")
    L.append("   • \"من هو #10؟\"")
    L.append("   • \"موعد الماتش القادم\"")
    L.append("   • \"تحديث الترتيب\"")
    L.append("   • \"قائمة اللاعبين\"")
    L.append("")
    L.append("📌 المصدر: خزنة حاتم — Nadi Al-Ahly")

    return "\n".join(L)

if __name__ == "__main__":
    print(build_message())
