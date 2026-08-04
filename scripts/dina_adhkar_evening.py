#!/usr/bin/env python3
"""Dina Evening/Maghrib Adhkar Reminder (after Maghrib or Isha prayer).
Delivers full evening adhkar + Quran reading reminder + daily evaluation prompt.
Usage: dina_adhkar_evening.py
"""
import urllib.request, json

def get_date():
    url = "https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
    j = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    return j["data"]["date"]["readable"]

def build():
    d = get_date()
    L = []
    L.append("Cronjob Response: 🌙 Evening Adhkar (Maghrib/Isha)")
    L.append("(job_id: dina-adhkar-evening)")
    L.append("-------------")
    L.append("")
    L.append("🌙 مساء الخير يا مستر حاتم! 🤍")
    L.append("حان وقت أذكار المساء بعد صلاة المغرب 🕌")
    L.append("")
    L.append("📖 أذكار المساء (من السنة):")
    L.append("")
    L.append("1️⃣ أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه — 100 مرة 🌿")
    L.append("2️⃣ سبحان الله وبحمده — 100 مرة 🌿")
    L.append("3️⃣ سبحان الله العظيم — 100 مرة 🌿")
    L.append("")
    L.append("📖 الحفظ (القرآن):")
    L.append("   • لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير — 10 مرات")
    L.append("   • بسم الله الذي لا يضر مع اسمه شيء في الأرض ولا في السماء وهو السميع العليم — 3 مرات")
    L.append("   • آية الكرسي (البقرة: 255) — مرة واحدة 🛡️")
    L.append("   • سورة الإخلاص — 3 مرات")
    L.append("   • سورة الفلق — 3 مرات")
    L.append("   • سورة الناس — 3 مرات")
    L.append("")
    L.append("🌙 قبل النوم:")
    L.append("   • بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا (عند النوم)")
    L.append("   • أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ...")
    L.append("   • نَحْنُ وَكَمِلْنَا اسْمُكَ نَسْأَلُكَ رِضَاكَ وَالْمَغْنَمَةَ عَلَى مَا قَدَّمْتَ")
    L.append("")
    L.append("📖 ورد قرآن: اقرأ 3 صفحات قبل النوم 🤍")
    L.append("📅 تقييم اليوم: ماذا أنجزت اليوم؟ ماذا نحسّن؟")
    L.append("")
    L.append("🕐 اليوم: " + d + " (توقيت القاهرة)")
    L.append("")
    L.append("To stop or manage this job, send me a new message (e.g. \"stop reminder 🌙 Evening Adhkar\").")
    L.append("🤲 اللهم بلّغنا رمضان وأعنّا فيه على الصيام والقيام")
    return "\n".join(L)

try:
    print(build())
except Exception as e:
    print(f"⚠️ دينا: معرفتش أجيب التاريخ دلوقتي ({e}). برّوك ربنا 🤍")
