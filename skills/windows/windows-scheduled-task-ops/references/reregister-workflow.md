# Re-register / edit a Windows scheduled task from XML (validated workflow)

Scenario: you edited a launcher (e.g. changed a VBS `sh.Run ..., False` to `True`)
and/or want to add a BootTrigger. Steps that actually worked:

## 1. Author the XML as UTF-8
Write the task XML with `encoding="UTF-16"` in the declaration but as a plain UTF-8
file (easiest to produce from an agent). Do NOT try to hand-write UTF-16.

## 2. Convert UTF-8 -> UTF-16 LE BOM with PowerShell
```powershell
powershell -NoProfile -Command "$c=Get-Content -Raw -Encoding UTF8 'C:\path\to\task.utf8.xml'; [System.IO.File]::WriteAllText('C:\path\to\task.xml',$c,[System.Text.Encoding]::Unicode)"
```
`[System.Text.Encoding]::Unicode` == UTF-16 LE with BOM. `schtasks /create` now
accepts it. (Avoid a Python heredoc here: the `\` in the task URI `\MyService`
raises a Python `unicodeescape` error in a normal string.)

## 3. Register (elevated via PowerShell — bypasses git-bash "Access is denied")
```powershell
powershell -NoProfile -Command "Start-Process schtasks.exe -ArgumentList '/create','/tn','MyService','/xml','C:\path\to\task.xml','/f' -Verb RunAs -WindowStyle Hidden -Wait"
```
A bare `schtasks /create /xml ... /f` from git-bash returned "Access is denied" for a
current-user task; the PowerShell RunAs path succeeded.

## 4. Stop old instance, start via task, verify
```bash
# stop the running service however its CLI provides (e.g. hermes gateway stop)
schtasks /run /tn MyService
sleep 25
schtasks /query /tn MyService /fo LIST | grep -iE "^Status"   # expect: Running
schtasks /query /tn MyService /xml | grep -iE "BootTrigger|LogonTrigger|RunLevel"
```
`Status: Running` (not `Ready`) confirms the launcher is waiting on the child, so
RestartOnFailure now guards the real service.
