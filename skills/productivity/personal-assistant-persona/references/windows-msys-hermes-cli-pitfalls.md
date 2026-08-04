# Windows / MSYS + Hermes CLI Pitfalls (exact transcripts & fixes)

Captured while building the Dina persona + 7 cron reminders on a Windows host
where the `terminal` tool runs bash (git-bash/MSYS). Each cost real debugging
time. The host HOME is `C:\Users\hshin`; Hermes home is
`C:\Users\hshin\AppData\Local\hermes`.

## 1. `hermes backup -o` path got mangled into a phantom drive
- Symptom: passed `-o /d/Backup/hermes-backup-<ts>.zip`, the tool reported
  success writing to `C:\d\Backup\...` (a nonexistent path). `ls` on
  `/d/Backup/...` showed nothing; the file was actually at `/c/d/Backup/...`.
- Cause: MSYS rewrote the POSIX-style `/d/...` into `C:\d\...`.
- Fix: pass a real Windows path with forward slashes: `-o D:/Backup/name.zip`.
- Cleanup: `rm -f /c/d/Backup/<file>; rmdir /c/d/Backup` to remove the phantom.

## 2. `hermes cron create --script` rejects any path
- Symptom: `--script "$HOME/AppData/Local/hermes/scripts/x.py"` →
  "Script path must be relative to ~/.hermes/scripts/. Got absolute or
  home-relative path".
- Fix: pass ONLY the bare filename, e.g. `--script dina_prayer_Fajr.py`. The
  file must live in `~/.hermes/scripts/`. To parametrize (e.g. which prayer),
  make a thin wrapper in that dir that sets `sys.argv` and `runpy.run_path`.

## 3. MSYS `/c/...` path passed to Windows `python` double-prefixes
- Symptom: `python /c/Users/hshin/.../script.py` →
  "can't open file 'C:\\c\\Users\\hshin\\...'".
- Fix: call with a native path: `python C:/Users/hshin/.../script.py`.
  Inside scripts, always derive paths from `os.path.abspath(__file__)` /
  `os.path.dirname(...)`, never hardcode a `/c/...` literal.

## 4. MSYS `curl` fails writing to /tmp
- Symptom: `curl -sSL ... -o /tmp/p.json` → "curl: (23) client returned ERROR
  on write of 1312 bytes" (HTTP 200 but size 0).
- Fix: use Python `urllib.request` instead of curl for API fetches on this host.

## 5. `du -sh` on a large vault times out
- Symptom: `du -sh /c/Users/hshin/AppData/Local/hermes` returned exit 124
  (timeout) — the tree has ~10k small files (mostly venv).
- Fix: bounded `os.walk` in Python to estimate per-directory sizes with a
  deadline, e.g. sum `os.path.getsize` and break after N seconds.

## 6. Batched `hermes cron create` — one job drops silently
- Symptom: a heredoc/`set -e` block creating 7 jobs; 6 succeeded, 1 failed
  with "hermes: error: unrecognized arguments: telegram:779043832" (a shell
  quoting glitch on that one line). `hermes cron list` only showed the 6.
- Fix: re-run the single failed job on its own command line. Always confirm
  with `hermes cron list` afterward and count the jobs.
