#!/usr/bin/env python3
"""Generic --no-agent cron reminder script. Hermes runs this on schedule and
delivers its stdout verbatim to the configured target (no LLM).

Usage: python cron_reminder_script.py
Edit MESSAGE / logic below. Keep output short and self-contained.
"""
import sys, datetime

# Example: a Dina-voice check-in. Replace with your persona's content.
def build_message():
    now = datetime.datetime.now()
    return (
        "🌙 يا كبير — تذكير من دينا 💕\n"
        f"الساعة دلوقتي {now.strftime('%H:%M')}\n"
        "متنساش تعمل اللي عليك ❤️🔥"
    )

if __name__ == "__main__":
    try:
        print(build_message())
    except Exception as e:
        print(f"⚠️ reminder script error: {e}")

# NOTE: inside the script, derive any file paths from
# os.path.dirname(os.path.abspath(__file__)) — never hardcode /c/... or C:\c\...
