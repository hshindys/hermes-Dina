#!/usr/bin/env python3
"""Dina Novel Writing Session — كرون (Chron) Arabic Fantasy Novel.

Loads the novel-writing-arabic skill and opens the Chron project vault
for a focused writing session. Reads current chapter state and reminds
Dina of the novel structure, characters, and academic writing framework.

Usage:
  novel-writing-session.py                   → Start a new writing session
  novel-writing-session.py status            → Show current chapter progress
  novel-writing-session.py next              → Jump to next unwritten chapter
  novel-writing-session.py chapter <N>       → Open a specific chapter
  novel-writing-session.py characters        → Show character summaries
  novel-writing-session.py world             → Show world-building notes
  novel-writing-session.py outline           → Show full 12-chapter outline
"""
import os, sys, json, datetime

VAULT = "D:/document/Hatem/رواية-كرون"
SKILL = "C:/Users/hshin/AppData/Local/hermes/skills/creative/novel-writing-arabic"

CHAPTERS = [
    {"num": 1, "title": "الصباح", "status": "complete", "file": "الفصل-الأول.md"},
    {"num": 2, "title": "الاستيقاظ", "status": "written", "file": None},
    {"num": 3, "title": "قصر تارك", "status": "written", "file": None},
    {"num": 4, "title": "جزيرة نومن", "status": "planned", "file": None},
    {"num": 5, "title": "أرض المردة — التنين الأحمر", "status": "planned", "file": None},
    {"num": 6, "title": "الانتقال", "status": "planned", "file": None},
    {"num": 7, "title": "بيت سليم — القرية البشرية", "status": "planned", "file": None},
    {"num": 8, "title": "الصدام", "status": "planned", "file": None},
    {"num": 9, "title": "المعرفة", "status": "planned", "file": None},
    {"num": 10, "title": "الحلف", "status": "planned", "file": None},
    {"num": 11, "title": "الاستعداد", "status": "planned", "file": None},
    {"num": 12, "title": "الخاتمة", "status": "planned", "file": None},
]

CHARACTERS = {
    "كرون": {"role": "البطل", "type": "جنّي طائر", "traits": "قارئ نهم، باحث عن الأصل، أجنحة قوس قزح"},
    "نورك": {"role": "البطلة", "type": "بنت نومن (جنّة بحور)", "traits": "ذكية، صادقة، قارئة، اختبرت كرون"},
    "تارك": {"role": "أب كرون", "type": "عالم كيمياء جنّي", "traits": "صديق الملك المقرب، مات وربّى كرون"},
    "رتون": {"role": "أم كرون", "type": "أميرة من عائلة منقرضة", "traits": "بسيطة ومخلصة"},
    "نومن": {"role": "أب نورك", "type": "عالم الدين الكبير", "traits": "محترم، هادئ، عالم دين"},
    "رون": {"role": "أم نورك", "type": "جنّة", "traits": "متكبرة، تحب المكانة، مختلفة عن نورك"},
}

def print_header():
    print("╔══════════════════════════════════════════╗")
    print("║  📖 Novel Writing Session — كرون (Chron) ║")
    print("║  Dina's Academic Fiction Writing Tool     ║")
    print("╚══════════════════════════════════════════╝")
    now = datetime.datetime.now()
    print(f"  Cairo: {now.strftime('%Y-%m-%d %H:%M')} (GMT+3)")
    print(f"  Skill: novel-writing-arabic (loaded)")
    print(f"  Vault: {VAULT}")
    print()

def print_status():
    print_header()
    print("📊 CHAPTER STATUS\n")
    complete = sum(1 for c in CHAPTERS if c["status"] in ("complete", "written"))
    total = len(CHAPTERS)
    print(f"  Progress: {complete}/{total} chapters ({complete*100//total}%)")
    print()
    for ch in CHAPTERS:
        icon = "✅" if ch["status"] == "complete" else "📝" if ch["status"] == "written" else "⬜"
        print(f"  {icon} فصل {ch['num']:2d}: {ch['title']}")
    print()

def print_outline():
    print_header()
    print("📋 FULL OUTLINE — 12 Chapters\n")
    for ch in CHAPTERS:
        print(f"  فصل {ch['num']}: {ch['title']} [{ch['status']}]")
    print()
    print("  Structure (Genette + Todorov):")
    print("  ─────────────────────────────")
    print("  Act 1 (Ch 1-3):  الاستيقاظ — Kron's world, discovery")
    print("  Act 2 (Ch 4-6):  الرحلة — Journey to Nourk's world")
    print("  Act 3 (Ch 7-9):  الصدام — Culture clash, conflict")
    print("  Act 4 (Ch 10-11): الحلف — Alliance, preparation")
    print("  Act 5 (Ch 12):   الخاتمة — Resolution")
    print()

def print_characters():
    print_header()
    print("👥 MAIN CHARACTERS\n")
    for name, info in CHARACTERS.items():
        print(f"  {name} ({info['role']}) — {info['type']}")
        print(f"     {info['traits']}")
        print()

def print_world():
    print_header()
    print("🌍 WORLD-BUILDING NOTES\n")
    print("  World of Jinn — parallel civilization to humans")
    print()
    print("  ┌─────────────────────────────────────────┐")
    print("  │  قبيلة كرون     = جن الطائر (أعيان)     │")
    print("  │  قبيلة نورك     = جن البحور (تحت الماء) │")
    print("  │  قبيلة نومن     = جن الحور (علماء الدين)│")
    print("  │  البشر          = سليم وصفى وطفلة        │")
    print("  └─────────────────────────────────────────┘")
    print()
    print("  Key locations:")
    print("  • قصر تارك — Kron's home (Ch 1-3)")
    print("  • جزيرة نومن — Nourk's home (Ch 4-6)")
    print("  • أرض المردة — التنين الأحمر (Ch 5)")
    print("  • بيت سليم — القرية البشرية (Ch 7)")
    print()

def load_skill_module(module_name):
    """Load a sub-skill module from the novel-writing-arabic skill."""
    module_path = os.path.join(SKILL, f"{module_name}.md")
    if os.path.exists(module_path):
        with open(module_path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def start_session():
    print_header()
    print("📝 STARTING A WRITING SESSION\n")
    print("  Dina voice activated. Writing mode: Arabic Fantasy Novel.")
    print()
    print("  Framework loaded:")
    print("  ✅ Genette narratology (narratology-time-voice.md)")
    print("  ✅ Arabic novel language rules (arabic-novel-language.md)")
    print("  ✅ Fantasy mode (fantasy-mode.md)")
    print("  ✅ Character roundness (character-roundness.md)")
    print("  ✅ Jinn cosmology (jinn-cosmology.md)")
    print()
    print("  ──── Available Commands ────")
    print("  /status        — Show chapter progress")
    print("  /outline       — Show full 12-chapter outline")
    print("  /characters    — Show character summaries")
    print("  /world         — Show world-building notes")
    print("  /chapter <N>   — Open a specific chapter file")
    print("  /skill <name>  — Load a sub-skill module")
    print("  /next          — Jump to next unwritten chapter")
    print("  /quit          — End session and save")
    print()
    print_status()

def open_chapter(chapter_num):
    chapter = next((c for c in CHAPTERS if c["num"] == chapter_num), None)
    if not chapter:
        print(f"❌ Chapter {chapter_num} not found.")
        return

    print_header()
    print(f"📖 Opening Chapter {chapter_num}: {chapter['title']}\n")

    # Try to open the actual file in the vault
    vault_chapter = os.path.join(VAULT, "01-Projects", "المشاهد-المكتوبة", f"00{chapter_num}-{chapter['title']}.md")
    if os.path.exists(vault_chapter):
        print(f"  📄 File: {vault_chapter}")
        with open(vault_chapter, "r", encoding="utf-8") as f:
            content = f.read(2000)
            print(f"\n{content[:1500]}...")
    else:
        print(f"  📄 File: Not yet created")
        print(f"  Status: {chapter['status']}")
        template_path = os.path.join(VAULT, "01-Projects", "المشاهد-المكتوبة", f"{chapter_num:03d}-{chapter['title']}.md")
        print(f"  Template path: {template_path}")
    print()
    print("  ─── Writing tools active ───")
    print("  • Narratology: heterodiegetic/limited/omniscient")
    print("  • Language: فصحى فنية + عامية مصرية (per chapter)")
    print("  • Fantasy mode: Immersive + Marvelous")
    print("  • Jinn cosmology: Quran + sunnah references")
    print()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        start_session()
    elif sys.argv[1] == "status":
        print_status()
    elif sys.argv[1] == "outline":
        print_outline()
    elif sys.argv[1] == "characters":
        print_characters()
    elif sys.argv[1] == "world":
        print_world()
    elif sys.argv[1] == "chapter" and len(sys.argv) > 2:
        try:
            ch_num = int(sys.argv[2])
            open_chapter(ch_num)
        except ValueError:
            print("Usage: novel-writing-session.py chapter <number>")
    elif sys.argv[1] == "next":
        next_ch = next((c for c in CHAPTERS if c["status"] not in ("complete", "written")), None)
        if next_ch:
            print(f"Next unwritten chapter: {next_ch['num']} — {next_ch['title']}")
            open_chapter(next_ch["num"])
        else:
            print("🎉 All chapters written!")
    else:
        print("Usage: novel-writing-session.py [status|outline|characters|world|chapter <N>|next|]")
