#!/usr/bin/env python3
"""showtime.py — Display current time, weather, session status, and prayer
times + du'a in Cairo (GMT+3).  Prayer times from AlAdhan (no API key)."""
import datetime
import json
import pathlib
import urllib.request
from zoneinfo import ZoneInfo

CAIRO = ZoneInfo("Africa/Cairo")
now = datetime.datetime.now(CAIRO)

# ── Du'a for each prayer ──
PRAYER_DUAS = {
    "Fajr": (
        "اللهم إني أسألك خير ما في الفجر يا مفتاح الرحمة والمغفرة،\n"
        "وأنت لا تخلف الميعاد فاغفر لنا يا غفارًا. 🌙"
    ),
    "Dhuhr": (
        "اللهم إني أسألك رحمتك التي وسعتْ كل شيء أن تغفرة لنا ولإخواننا\n"
        "المؤمنين، واجعلنا من التوابين المتطهرين. ☀️"
    ),
    "Asr": (
        "اللهم إني أعوذ بك من عذاب القبر وعذاب النار،\n"
        "وأعوذ بك من فتنة الصدر ومن كرب البثر. 🕰️"
    ),
    "Maghrib": (
        "اللهم إنك تسألوا عنكِ شكرًا، فأنا أشكرُك على نعمتك،\n"
        "وأستغفرك من شق نفسي فاغفر لي. 🌆"
    ),
    "Isha": (
        "اللهم إني أعوذ بك من عذاب القبر ومن فتنته،\n"
        "واجعلنا من المتوكلين عليك في كل حال. 🌙"
    ),
}

PRAYER_ORDER = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Maghrib", "Isha"]


def _to_min(t):
    """HH:MM or 'HH:MM ام/مس' → minutes since midnight (24h)."""
    t = t.strip()
    parts = t.split()
    core = parts[0]
    hh, mm = core.split(":")
    h, m = int(hh), int(mm)
    if "م" in (parts[-1].lower() if len(parts) > 1 else ""):
        if h < 12:
            h += 12
    elif "ص" in (parts[-1].lower() if len(parts) > 1 else ""):
        if h == 12:
            h = 0
    return h * 60 + m


def fetch_prayer_times():
    date = now.strftime("%d-%m-%Y")
    url = (
        f"https://api.aladhan.com/v1/timings?city=Cairo&country=Egypt"
        f"&date={date}&method=3"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return data["data"]["timings"]
    except Exception:
        return None


def current_prayer_info(timings):
    """Return (active_prayer_name, mins_to_next, dua) based on `now`."""
    if not timings:
        return ("—", 0, "(مواقيت غير متاحة الآن — API فشلت) ☁️")
    now_min = now.hour * 60 + now.minute
    active = "Isha"
    mins_next = 0
    for i, name in enumerate(PRAYER_ORDER):
        if name == "Sunrise":
            continue
        start = _to_min(timings[name])
        nxt = [n for n in PRAYER_ORDER[i + 1:] if n != "Sunrise"]
        end_name = nxt[0] if nxt else None
        end = _to_min(timings[end_name]) if end_name else 24 * 60 + 59
        if start <= now_min < end:
            active = name
            mins_next = end - now_min
            # show mins until *next* prayer
            break
    dua = PRAYER_DUAS.get(active, "(دعاء غير مسجل)")
    return (active, mins_next, dua)


# ── Greetings ──
hour = now.hour
if 5 <= hour < 12:
    greeting = "صباح الخير يا حاتم"
elif 12 <= hour < 17:
    greeting = "مساء الخير يا حاتم"
elif 17 <= hour < 21:
    greeting = "مساء الخير يا حاتم"
else:
    greeting = "تصبح على خير يا حاتم"

days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
day_name = days_ar[now.weekday()]

months_ar = [
    "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
    "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
]
month_name = months_ar[now.month - 1]
time_str = now.strftime("%H:%M:%S")
date_str = f"{now.day} {month_name} {now.year}"

# ── Weather (Open-Meteo) ──
def fetch_weather(lat=30.0131, lon=31.2089):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read()).get("current_weather", {})
    except Exception:
        return None

def weather_emoji(code):
    if code == 0:
        return "☀️"
    if code in (1, 2, 3):
        return "⛅"
    if code in (45, 48):
        return "🌫️"
    if code in (51, 53, 55):
        return "🌦️"
    if code in (61, 63, 65):
        return "🌧️"
    if code in (71, 73, 75):
        return "🌨️"
    if code == 95:
        return "⛈️"
    if code in (96, 99):
        return "⛈️🌨️"
    return "🌡️"

def describe_weather(code):
    mapping = {
        0: "سماء صافية",
        1: "غائمة جزئيا",
        2: "غائمة جزئيا",
        3: "غائمة",
        45: "ضباب",
        48: "ضباب سحب",
        51: "رذاذ خفيف",
        53: "رذاذ",
        55: "رذاذ كثيف",
        61: "أمطار",
        63: "أمطار",
        65: "أمطار غزيرة",
        71: "ثلوج",
        73: "ثلوج",
        75: "ثلوج غزيرة",
        95: "عاصفة رعدية",
        96: "رعد + برد",
        99: "رعد + برد غزير",
    }
    return mapping.get(code, "غير معروف")

def format_weather(cw):
    if not cw:
        return "غير متاح"
    temp = cw.get("temperature", "?")
    wind = cw.get("windspeed", "?")
    code = cw.get("weathercode", -1)
    is_day = cw.get("is_day", 0)
    emoji = weather_emoji(code)
    desc = describe_weather(code)
    period = "نهاراً" if is_day else "ليلاً"
    return f"{emoji} {desc} | {temp}° م | رياح {wind} كم/س | {period}"

# ── Session status ──
def get_session():
    session_dir = pathlib.Path.home() / ".hermes" / "sessions"
    date_key = now.strftime("%Y-%m-%d")
    session_file = session_dir / f"{date_key}.json"
    if not session_file.exists():
        return None
    try:
        with open(session_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None

def format_session(s):
    if not s:
        return "جديدة — أول تفاعل اليوم"
    turns = s.get("turn_count", 0)
    if s.get("freshly_created"):
        return f"جديدة ({turns}) 🆕"
    return f"مستمرة ({turns} تفاعلات)"

# ── Assemble ──
weather_line = format_weather(fetch_weather())
session_line = format_session(get_session())
timings = fetch_prayer_times()
if timings:
    name, mins, dua = current_prayer_info(timings)
    hh, mm = divmod(mins, 60)
    next_idx = (PRAYER_ORDER.index(name) + 1) % len(PRAYER_ORDER)
    next_prayer = PRAYER_ORDER[next_idx] if PRAYER_ORDER[next_idx] != 'Sunrise' else PRAYER_ORDER[next_idx+1]
    prayer_line = f"🧧 الآن: {name} — {hh}س: {mm}د للـ {next_prayer}"
else:
    prayer_line = "🧧 مواقيت الصلاة: API فشلت"
    dua = "اللهم صلِّ على محمد وعلى آل محمد، كما صلّيت على إبراهيم وعلى آل إبراهيم إنك حميدٌ مجيدٌ. 🌙"

box_w = 36
print()
print("╔" + "═" * (box_w + 2) + "╗")
print(f"║  {greeting:<{box_w}}  ║")
print("║" + " " * (box_w + 2) + "║")
print(f"║  📅 {day_name}، {date_str:<{box_w - 3}}║")
print(f"║  🕐 {time_str:<{box_w - 3}}║")
print(f"║  🌍 القاهرة (GMT+3){' ' * (box_w - 16)}║")
print(f"║  📍 الجيزة، مصر{' ' * (box_w - 12)}║")
print(f"║  🌤️  {weather_line:<{box_w - 3}}║")
print(f"║  💬 جلسة: {session_line:<{box_w - 5}}║")
print(f"║  {prayer_line:<{box_w}}║")
print("╠" + "═" * (box_w + 2) + "╣")
print("║  📿 دعاء الصلاة:" + " " * (box_w - 11) + "║")
print("║" + " " * (box_w + 2) + "║")
# Print du'a line wrapped
for line in dua.split("\n"):
    print(f"║  {line:<{box_w}}  ║")
print("║" + " " * (box_w + 2) + "║")
print("╚" + "═" * (box_w + 2) + "╝")
