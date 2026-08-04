---
name: hermes-windows-gateway
description: "Harden Hermes gateway for Windows reboot auto-start."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
---

# Hermes Gateway Persistence on Windows

On Windows the "gateway auto-start" is a **Scheduled Task** named `\Hermes_Gateway`
(there is no systemd/launchd on Windows). The default install is fragile and the
gateway often does NOT survive a reboot. This skill hardens it.

## Quick diagnosis

```bash
hermes gateway status                      # running? PID + Scheduled Task state
schtasks /query /tn \Hermes_Gateway /xml   # inspect triggers / principal / actions
```

A healthy, reboot-surviving task has BOTH a `<BootTrigger>` and a `<LogonTrigger>`,
a `Principal` with `<RunLevel>HighestAvailable</RunLevel>`, and `<RestartOnFailure>`
(default 999 retries / PT1M).

## Why the gateway "isn't working after restart"

Two real root causes (verify before "fixing"):

1. **LogonTrigger only.** The default task fires only on *interactive logon*
   (`<LogonType>InteractiveToken</LogonType>`). A reboot that lands on the lock
   screen, or uses Fast Startup / hibernate, never triggers it. There is no
   `<BootTrigger>`, so the gateway stays dead until the next interactive logon.
2. **Fire-and-forget launcher.** The task action runs a VBS that calls
   `sh.Run "... gateway run", 0, False` (Wait=False). The VBS exits 0 immediately,
   so to Task Scheduler the task *succeeded*. Its RestartOnFailure therefore watches
   the VBS, not the gateway — when the gateway crashes on boot (logs show
   `exited UNCLEANLY — no exit path ran — SIGKILL / OOM / VM death`), nothing
   restarts it until the next logon.

## The fix (password-free, reversible)

1. Edit the VBS launcher to WAIT for the gateway so RestartOnFailure actually
   guards the gateway process:

   ```vbs
   sh.Run "C:\Users\...\hermes-agent\venv\Scripts\python.exe -m hermes_cli.main gateway run", 0, True
   ```

2. Re-register the task with a BootTrigger + LogonTrigger and HighestAvailable,
   keeping RestartOnFailure. A ready, idempotent script that does both (and reads
   the existing task to preserve your SID/paths) is in `scripts/harden_gateway_autostart.py`.
   See `references/diagnosis.md` for the manual steps and `templates/Hermes_Gateway.vbs`.

## Pitfalls / do NOT do this

- **Do NOT "fix" `scale_to_zero`.** `gateway.scale_to_zero.idle_timeout_minutes: 5`
  looks like it would shut the gateway down on idle, but it does NOT. Scale-to-zero
  only *arms* when the `HERMES_SCALE_TO_ZERO` env flag is set AND messaging is
  relay-only/absent. Direct platform connections (Telegram/Discord/Slack) **disarm**
  it. Setting `idle_timeout_minutes: 0` is also a no-op (the parser reverts ≤0 back
  to 5). Verify with source: `gateway/scale_to_zero.py::scale_to_zero_enabled()`
  returns False when the env flag is unset. If the gateway "dies on idle," look at
  crashes/unclean exits, not scale_to_zero.
- **schtasks XML encoding.** When re-registering from a hand-written XML, `schtasks`
  requires the file's actual byte encoding to match the `<?xml ... encoding="..."?>`
  declaration. The existing Hermes task is **UTF-16**; declare `encoding="UTF-16"`
  AND write the file as UTF-16 (e.g. `open(path,'w',encoding='utf-16')`). A UTF-8
  file with a UTF-16 declaration fails: `ERROR: The task XML is malformed.
  (1,40)::ERROR: unable to switch the encoding`.
- **Python raw strings for the XML.** The task URI is `\Hermes_Gateway` — a literal
  `\U` inside a normal Python triple-quoted string raises
  `unicode error ... truncated \UXXXXXXXX escape`. Use a **raw** string (`r'''...'''`)
  when generating the XML in Python, or strip the declaration before ET.fromstring
  (parsing a `str` that contains an encoding declaration raises).
- **Back up first.** `schtasks /query /tn \Hermes_Gateway /xml > Hermes_Gateway.backup.xml`
  before re-registering.

## Verify

```bash
hermes gateway stop
schtasks /run /tn \\Hermes_Gateway
sleep 45
hermes gateway status      # expect a fresh PID and "Gateway running with N platform(s)"
```

## Windows-specific git pitfall: "dubious ownership" (git 2.40+)

On Windows (and WSL), git 2.40+ enforces the **`safe.directory`** ownership check. Any
git operation that runs inside a folder on a filesystem that does not record POSIX
ownership — common for `C:\Users\<you>\AppData\Local\hermes` and its subfolders, or WSL
mounts — fails with:

```
fatal: detected dubious ownership in repository at 'D:/document/رواية-كرون'
'document/رواية-كرون' is on a file system that does not record ownership
To add an exception for this directory, call:
    git config --global --add safe.directory 'D:/document/رواية-كرون'
```

This surfaces inside tools that shell out to git: `obsidian-git`, backup scripts,
`hermes` CLI git operations, etc. — not just interactive git. It is the most common
cause of "git operations silently fail inside Hermes on Windows".

**Fix — one of:**
```bash
# Per-directory (idempotent, safe to repeat):
git config --global --add safe.directory 'D:/document/رواية-كرون'

# Trust everything under a prefix (broader):
git config --global --add safe.directory 'C:/Users/<you>/AppData/Local/hermes/*'

# Or disable the check entirely (less safe):
git config --global --add safe.directory '*'
```

**Tip:** If `rm -rf` of a backup target that already sits inside a git repo fails with
`PermissionError: Access is denied` on a `.git/objects/...` file, the repo is likely
open in another process (an active `hermes` session or Obsidian). Either close those
first, or build the backup in a fresh empty directory outside any existing git tree
(cleanest: a non-Appdata drive path).

## Files in this skill
- `scripts/harden_gateway_autostart.py` — idempotent re-registration + VBS patch (preferred path).
- `templates/Hermes_Gateway.vbs` — corrected VBS (Wait=True), for reference only.
- `references/diagnosis.md` — manual step-by-step + the scale_to_zero deep-dive.
