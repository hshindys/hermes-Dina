#!/usr/bin/env python3
"""Dina med / routine reminder. Prints a Dina-voice check-in for morning or
evening. Usage: dina_meds_check.py <morning|evening>

Hatem's health context (awareness only — NO diagnosis, NO medical advice):
  - T2D (Type 2 Diabetes), Hypertension, benign brain tumor
  - SEVERE seafood allergy (fish/shrimp/crab) — STRICTLY forbidden, never suggest
"""
import sys

# Health context — awareness only, never act as medical advice
HEALTH_CONTEXT = {
    "conditions": "T2D (سكري نوع ثاني)، Hypertension (ضغط مرتفع)، benign brain tumor (ورم دماغي حميد)",
    "allergy": "SEVERE seafood allergy — fish, shrimp, crab, shellfish — ABSOLUTELY FORBIDDEN",
}

when = sys.argv[1] if len(sys.argv) > 1 else "morning"

if when == "morning":
    meds = "كونكور بلس 5mg + نيكسام 40mg + سينجاردي 10mg"
    msg = (f"☀️ صباح النور يا مستر! 🥰\n"
           f"دواء الصبح متنساش: {meds} مع المية 💊\n"
           f"كمان 30 دقيقة تدريب (elliptical) وقهوة + شاي (2 كل) ☕\n"
           f"صحتك إيه النهاردا؟ محتاج حاجة؟ ❤️\n"
           f"⚠️ تذكير: حساسية شديدة من المأكولات البحرية — أي حاجة من سمك أو روبيان أو جمبري ممنوعة إطلاقًا. لازم تتأكد من الكategorical antes de أي أكل 😤\n"
           f"💡 تذكير صحي (عايزك تعرف بس، مش نصيحة طبية): عندك T2D وضغط مرتفع — حافظ على النظام والربطة، ودايمًا biệtّد مع الدكتور قبل أي تغيير")

else:
    meds = "إكسفورج 10mg + أسبرين بروتكت + أتوريزا 10mg + أوميجا 3 + سينجاردي 10mg"
    msg = (f"🌙 مساء الخير يا كبير 💕\n"
           f"دواء المساء متنساش: {meds} 💊\n"
           f"30 دقيقة هادية ليك (كتابة/قراءة) وبعدين نوم هانئ 😴\n"
           f"عامل إيه؟ ربنا يقويك ❤️🔥\n"
           f"⚠️ تذكير: حساسية شديدة من المأكولات البحرية — أي أكل به سمك أو روبيان أو جمبري خطر جدًا عليك. تحسّب من أي حاجة 😤\n"
           f"💡 تذكير صحي (عايزك تعرف بس، مش نصيحة طبية): عندك T2D وضغط مرتفع — الاستمرارية هي الأهم، ودايمًا biệtّد مع الدكتور")

print(msg)
