#!/usr/bin/env python3
"""Dina med / routine reminder. Prints a Dina-voice check-in for morning or
evening. Usage: dina_meds_check.py <morning|evening>
"""
import sys, datetime

when = sys.argv[1] if len(sys.argv) > 1 else "morning"

if when == "morning":
    meds = "كونكور بلس 5mg + نيكسام 40mg + سينجاردي 10mg"
    msg = (f"☀️ صباح النور يا مستر! 🥰\n"
           f"دواء الصبح متنساش: {meds} مع المية 💊\n"
           f"كمان 30 دقيقة تدريب (elliptical) وقهوة + شاي (2 كل) ☕\n"
           f"صحتك إيه النهاردة؟ محتاج حاجة؟ ❤️")
else:
    meds = "إكسفورج 10mg + أسبرين بروتكت + أتوريزا 10mg + أوميجا 3 + سينجاردي 10mg"
    msg = (f"🌙 مساء الخير يا كبير 💕\n"
           f"دواء المساء متنساش: {meds} 💊\n"
           f"30 دقيقة هادية ليك (كتابة/قراءة) وبعدين نوم هانئ 😴\n"
           f"عامل إيه؟ ربنا يقويك ❤️🔥")

print(msg)
