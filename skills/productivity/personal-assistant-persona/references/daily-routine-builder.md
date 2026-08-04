# Daily Routine Builder — Pattern Reference

Session-captured pattern for building a self-contained daily-routine script
that reads a TOML config, fetches prayer times from the Aladhan API, builds a
schedule, and upserts it into the vault's daily note.

## When to use
- User has a `routine.toml` (or similar) with schedule + location + vault path.
- User wants the daily spiritual/work schedule written automatically into their
  Obsidian daily note each day.
- User needs a script that can run as a Hermes cron job (`--no-agent --script`).

## Setup

### 1. Config file: `~/.hermes/config/routine.toml`

Sections needed:
```toml
[location]
city = "Giza"
country = "Egypt"
latitude = 30.0131
longitude = 31.2089
timezone = "Africa/Cairo"
calculation_method = 5   # 5 = Egyptian General Authority of Survey

[vault]
path = "C:/Users/<user>/Documents/<vault-folder>"
daily_note_pattern = "Daily/{date}.md"
section_header = "## الروتين الروحي"

[schedule]
quran_minutes_after_fajr = 0
quran_duration_minutes = 30
asma_minutes_after_fajr = 35
writing_minutes_after_asr = 0
writing_duration_minutes = 45
family_call_minutes_after_maghrib = 15
sleep_time = "23:00"

[cache]
dir = "C:/Users/<user>/.hermes/cache"
```

### 2. Script: `~/.hermes/scripts/daily_routine.py`

Place the script in `~/.hermes/scripts/` (not in a subdirectory). The script:

- Reads `routine.toml` via `tomllib` (fallback `tomli` for pre-3.11).
- Fetches prayer times from `https://api.aladhan.com/v1/timings/<dd-mm-YYYY>`.
- Caches result as `<cache_dir>/prayer_times_<YYYY-MM-DD>.json`.
- Falls back to stale cache if API call fails and no internet.
- Builds a sorted schedule: Fajr → Quran → Asma → Dhuhr → Asr → Writing → Maghrib → Family Call → Isha → Sleep.
- Picks a random dua (Arabic) for the day.
- Picks the day's Asma al-Husna by day-of-year index.
- Upserts the block into `<vault_path>/Daily/<YYYY-MM-DD>.md` under the
  section header. If vault path doesn't exist, saves to `<cache_dir>/pending/`
  as a fallback.
- Uses `logging` module for structured output (timestamps, INFO/WARNING/ERROR).
- Uses `hhmm(timing)[:5].strip()` to strip timezone suffixes like `(EEST)`.

### 3. Cron job (daily, 5 AM Cairo time)

```
hermes cron create "0 5 * * *" \
  --name "Daily Spiritual Routine Builder" \
  --no-agent \
  --script daily_routine.py
```

Note: `--script` requires a bare filename only (no path). The file must be in
`~/.hermes/scripts/`. See `personal-assistant-persona` skill's pitfalls section
(on Windows MSYS) for path gotchas.

## Dependencies

```
pip install requests tomli   # tomli only needed for Python < 3.11
```

On Windows, `tzdata` may also be needed if the stdlib `zoneinfo` cannot find
the timezone database: `pip install tzdata`.

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `zoneinfo` fails at import | Missing tzdata on Windows | `pip install tzdata` |
| `tomllib` not found | Python < 3.11 | `pip install tomli` |
| `Script path must be relative` | Absolute path passed to `--script` | Use bare filename only |
| Prayer times have `(EEST)` suffix | Aladhan API includes timezone label | `hhmm()` strips it — do NOT skip this |
| Vault not found, script exits | `vault.path` missing or typo | Verify path in config; script saves to `pending/` instead of failing |
| Duplicate routine in note | Script re-run same day | Check `section_header` in content before writing (idempotent guard) |

## File locations (Windows host)

| File | Path |
|------|------|
| Script | `C:/Users/<user>/.hermes/scripts/daily_routine.py` |
| Config | `C:/Users/<user>/.hermes/config/routine.toml` |
| Cache dir | `C:/Users/<user>/.hermes/cache/` |
| Fallback (pending) | `C:/Users/<user>/.hermes/cache/pending/` |
| Vault (target) | Configurable in `routine.toml` → `[vault].path` |
