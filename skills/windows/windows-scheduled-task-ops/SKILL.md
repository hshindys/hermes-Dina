---
name: windows-scheduled-task-ops
description: "Auto-start a Windows service via schtasks on reboot."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
---

# Windows Scheduled Task Ops

Reusable technique for launching / auto-starting / keeping-alive a background
process (Python service, gateway, cron runner, any long-lived exe) on Windows via
Task Scheduler (`schtasks`). Captured from a real fix where a Hermes gateway
would not come back after a reboot.

## When to use
- You need a process to start automatically after a Windows reboot (and stay up).
- A scheduled task "succeeds" but the underlying service is dead and never restarts.
- `schtasks /create /xml` fails with a malformed-XML / encoding error.
- `schtasks /create` returns "Access is denied" in git-bash / MSYS.
- You are re-registering or editing an existing task from an XML file.

## The four things that bite (and the fix for each)

### 1. `schtasks /create /xml` demands UTF-16 with a matching declaration
`schtasks` only accepts task XML encoded as **UTF-16 LE with BOM**, and the
`<?xml ... encoding="..."?>` declaration MUST match the actual bytes. Common error:
```
ERROR: The task XML is malformed.
(1,40)::ERROR: unable to switch the encoding
```
This happens if you write a UTF-8 file but declare `encoding="UTF-16"`, or vice
versa. The original Hermes task XML was UTF-16; a hand-written UTF-8 file with a
UTF-16 declaration fails identically.

**Reliable approach:** author the XML as UTF-8 (easy to write), then convert to
UTF-16 with PowerShell — do NOT rely on a Python heredoc here, because the
backslash in the task URI (`\Hermes_Gateway`) triggers a Python `unicodeescape`
error in a normal triple-quoted string:
```powershell
powershell -NoProfile -Command "$c=Get-Content -Raw -Encoding UTF8 'in.xml'; [System.IO.File]::WriteAllText('out.xml',$c,[System.Text.Encoding]::Unicode)"
```
`[System.Text.Encoding]::Unicode` is UTF-16 LE BOM — exactly what `schtasks` wants.

### 2. "Access is denied" under git-bash is a schtasks quirk, not a real perms block
Even for a task that runs as the current user, `schtasks /create` invoked from
git-bash / MSYS can return `Access is denied`. The fix is to run it elevated via
PowerShell (this does NOT require you to actually be an admin — it just routes the
call correctly):
```powershell
powershell -NoProfile -Command "Start-Process schtasks.exe -ArgumentList '/create','/tn','<Name>','/xml','C:\path\to\task.xml','/f' -Verb RunAs -WindowStyle Hidden -Wait"
```
This completed cleanly where the bare `schtasks /create` was denied.

### 3. LogonTrigger alone does NOT survive a reboot
A task with only a `<LogonTrigger>` fires 30s after an **interactive logon**. On a
reboot that lands on the lock screen, or with Fast Startup / hibernate in play, it
may not fire — the service stays dead until the next human logon. Add a
`<BootTrigger>` alongside the LogonTrigger so it also fires on cold boot (give it a
`Delay` like `PT30S` so the network is up before the child connects):
```xml
<Triggers>
  <BootTrigger><Enabled>true</Enabled><Delay>PT30S</Delay></BootTrigger>
  <LogonTrigger><Enabled>true</Enabled><Delay>PT30S</Delay></LogonTrigger>
</Triggers>
```
Use `<RunLevel>HighestAvailable</RunLevel>` in the Principal if the child needs it.

### 4. RestartOnFailure only watches the task's OWN action — not a detached child
If the task's action is a launcher (VBS / wrapper) that spawns the real service
**fire-and-forget** and exits, Task Scheduler sees the launcher finish (exit 0) and
marks the task "succeeded." Its `<RestartOnFailure>` then guards the *launcher*,
which is already gone — so when the real service crashes, nothing restarts it.

**Fix:** make the launcher BLOCK on the child so the task stays "Running" for the
service's whole lifetime. In a VBS wrapper this is the third arg to `Run`:
```vbs
' False = fire-and-forget (BAD for RestartOnFailure); True = wait for child
sh.Run "C:\path\venv\Scripts\python.exe -m mypkg gateway run", 0, True
```
With `True`, `schtasks /query` shows `Status: Running` (not `Ready`) while the
service is alive, and `<RestartOnFailure><Count>999</Count><Interval>PT1M</Interval>`
actually resurrects the service when it dies.

## Verify after editing
```bash
# triggers + run level present?
schtasks /query /tn <Name> /xml | grep -iE "BootTrigger|LogonTrigger|RunLevel|RestartOnFailure"
# is the child actually alive? (Running = launcher is waiting on the child)
schtasks /query /tn <Name> /fo LIST | grep -iE "^Status"
```
To apply a changed launcher/task: stop the service (`hermes gateway stop` for the
gateway case), then `schtasks /run /tn <Name>`, wait ~20–30s, and confirm via the
service's own log / status.

## Pitfalls
- Don't assume a self-stop config (e.g. scale-to-zero / idle timeout) is the boot
  problem — **verify** it's actually armed before changing it. scale_to_zero only
  arms when an env flag is set AND messaging is relay-only; direct Telegram/Discord/
  Slack connections disarm it, so flipping `idle_timeout_minutes` is a no-op there.
- BootTrigger without a `Delay` can race network bring-up; keep `PT30S`.
- `schtasks /query /tn <Name> /fo LIST` "Status: Ready" for a waiting launcher means
  the launcher already exited (child detached) — that's the anti-pattern in #4.

## References
- `references/task-boot-logon.xml` — known-good UTF-16 task XML template
  (BootTrigger + LogonTrigger + HighestAvailable + RestartOnFailure + Exec).
- `references/reregister-workflow.md` — exact PowerShell/encoding steps to edit and
  re-register a task from XML.
