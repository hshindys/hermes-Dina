# showtime.py — Cairo Time + Weather + Session Status

## Overview
`showtime.py` is a unified status script that displays the current time in Cairo (GMT+3), weather from Open-Meteo, and daily session status — all in one Arabic-friendly terminal output.

## Location
`~/.hermes/scripts/showtime.py`

## Usage
```bash
python ~/.hermes/scripts/showtime.py
```

## Output Format
```
╔══════════════════════════════════╗
║  صباح الخير يا حاتم              ║
║                                    ║
║  📅 السبت, 1 أغسطس 2026          ║
║  🕐 09:19:04                      ║
║  🌍 Cairo (GMT+3)                ║
║  📍 الجيزة، مصر                  ║
║  🌤️ الطقس: ☀️ سماء صافية, 27.4°م  ║
║  💬 الجلسة: مستمرة (2 تفاعل)     ║
╚══════════════════════════════════╝
```

## Key Design Decisions
1. **Weather via Open-Meteo** — free, no API key needed. Uses `urllib.request` (stdlib) to avoid extra dependencies.
2. **Session tracking** reads `~/.hermes/sessions/YYYY-MM-DD.json` — the same file written by `session_manager.py`.
3. **Arabic day names** — `weekday()` returns 0=Mon..6=Sun, mapped to Arabic day names in correct order.
4. **No external deps** — uses only stdlib (`datetime`, `json`, `urllib.request`, `pathlib`, `zoneinfo`).

## Pitfall: weekday() indexing
Python's `weekday()` returns 0=Monday, 6=Sunday. The Arabic day array MUST match this order:
```python
days_ar = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
```
A common mistake is starting with السبت (Saturday) which would shift all days by one.

## Pitfall: Windows path in subprocess
When running `showtime.py` from git-bash/MSYS, use `python` from the Hermes venv:
```bash
/c/Users/hshin/AppData/Local/hermes/hermes-agent/venv/Scripts/python showtime.py
```
Not `/usr/bin/python` which may not exist or point to a different Python.

## Integration with cron
The script can be called from a cron job to deliver a daily status message to Telegram/Discord.
