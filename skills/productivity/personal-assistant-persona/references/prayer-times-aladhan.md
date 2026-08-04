# Live prayer times — aladhan API

For prayer/med reminders that stay correct as times drift (~1-2 min/day),
fetch times per-run instead of hardcoding.

Endpoint (Cairo, Egypt, ISNA method=5):
  https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5

Python (use urllib on Windows/MSYS — curl -o /tmp fails here):
```python
import urllib.request, json
url = "https://api.aladhan.com/v1/timingsByCity?city=Cairo&country=Egypt&method=5"
req = urllib.request.Request(url, headers={"User-Agent": "curl/8"})
j = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
t = j["data"]["timings"]          # Fajr, Dhuhr, Asr, Maghrib, Isha
date = j["data"]["date"]["readable"]
print(t["Maghrib"], date)
```
Sample (28 Jul 2026): Fajr 04:32 | Dhuhr 13:01 | Asr 16:38 |
Maghrib 19:51 | Isha 21:19.

Note: if you hardcode cron times from one day's values, they drift. For exact
daily times, use a single morning dispatcher job that fetches the day's times
and re-schedules the 5 reminders (schtasks / Hermes cron update). Otherwise
accept the slow drift and re-run the setup monthly.
