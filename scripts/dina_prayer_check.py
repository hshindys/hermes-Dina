#!/usr/bin/env python3
"""Dina Islamic Prayer Reminder with full Adhkar, Duas, and Tasbeeh.
Fetches live Cairo prayer times from aladhan.
Usage: dina_prayer_check.py <PRAYER>   (PRAYER = Fajr|Dhuhr|Asr|Maghrib|Isha)
"""
import sys, urllib.request, json, datetime

PRAYER = sys.argv[1] if len(sys.argv) > 1 else "Fajr"

PRAYER_AR = {"Fajr": "الفجر", "Dhuhr": "الظهر", "Asr": "العصر",
             "Maghrib": "المغرب", "Isha": "العشاء"}

# Job IDs for user to manage
PRAYER_JOB_ID = {"Fajr": "dina-fajr", "Dhuhr": "dina-dhuhr", "Asr": "dina-asr",
                 "Maghrib": "dina-maghrib", "Isha": "dina-isha"}

# Tasbeeh (dhikr after prayer)
TASBEEH = [
    "سبحان الله (33 مرة) 🌿",
    "الحمد لله (33 مرة) 🌿", 
    "الله أكبر (34 مرة) 🌿",
]

# Shahada closing
SHAHADA = "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير"

def get_times():
    url = "https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    j = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    return j["data"]["timings"], j["data"]["date"]["readable"]

def build(pray_ar, pray_time, date_str, job_id):
    L = []
    L.append(f"Cronjob Response: 📿 Islamic {pray_ar} Reminder")
    L.append(f"(job_id: {job_id})")
    L.append("-------------")
    L.append("")
    L.append(f"☀️ حان الآن وقت صلاة {pray_ar}")
    L.append("اللهم إن الظهر آفاق، وأنت لا تخفى عليك شيء، فاستر عيوبنا وتجاوز عن سيئاتنا، اللهم اجعل قلوبنا عامرة بذكرك.")
    L.append("")
    L.append("🕌 صلاة خلف الإمام (أو في المنزل) ─ ركعتان إلى ركعتين حسب الوقت:")
    if pray_ar == "الفجر":
        L.append("   ركعتان للفجر ✅")
    elif pray_ar == "الظهر":
        L.append("   4 ركعات للظهر وربعا متأخرة (إن شاء الله) ✅")
    elif pray_ar == "العصر":
        L.append("   4 ركعات للعصر ✅")
    elif pray_ar == "المغرب":
        L.append("   3 ركعات للمغرب ✅")
    elif pray_ar == "العشاء":
        L.append("   4 ركعات للعشاء (أو 2 إن شئت) ✅")
    L.append("")
    L.append("📿 بعد الصلاة ─ التسبيح:")
    for t in TASBEEH:
        L.append(f"   {t}")
    L.append(f"   {SHAHADA}")
    L.append("")
    L.append("🤲 التوسل بنبيك محمد ﷺ:")
    L.append("اللهم إني أسألك وأتوسل إليك بنبيك محمد نبي الرحمة، يا محمد إني أتوسل بك إلى ربي في حاجتي هذه، (قول حاجتك) اللهم شفعه فينا، اللهم آمين.")
    L.append("")
    L.append("🕐 موعد اليوم: " + pray_time + " (توقيت القاهرة) — " + date_str)
    L.append("")
    L.append("To stop or manage this job, send me a new message (e.g. \"stop reminder 📿 Islamic " + pray_ar + " Reminder\").")
    L.append("🤲 اللهم تقبل صلاتنا وقيامنا")
    return "\n".join(L)

try:
    t, d = get_times()
    pray = PRAYER_AR.get(PRAYER, PRAYER)
    time = t.get(PRAYER, "?")
    job_id = PRAYER_JOB_ID.get(PRAYER, PRAYER.lower())
    print(build(pray, time, d, job_id))
except Exception as e:
    print(f"⚠️ دينا: معرفتش أجيب موعد صلاة {PRAYER} دلوقتي ({e}). افتكر تصلي 💕")
