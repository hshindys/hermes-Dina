---
name: windows-uwp-automation
description: |
  Drive Windows UWP/Store apps via computer_use on Win11.
version: 1.0.0
platforms: [windows]
metadata:
  hermes:
    tags: [windows, uwp, computer-use, desktop-automation, calendar, microsoft-todo]
    category: windows
    related_skills: [computer-use]
---

# Windows UWP / Store App Automation via computer_use

The bundled `computer-use` skill covers the universal click/type/capture
vocabulary. This skill fills the **Windows-UWP-specific gaps** that skill
doesn't: how to actually *launch* a Store app, and two capture traps that
make UWP windows stubborn to screenshot.

## Launching a UWP app

`list_apps` reports UWP apps with a `launch_path` like
`shell:appsFolder\<bundleId>!<AppId>` (or a plain `.exe` for desktop apps).
**Do NOT** launch the `shell:appsFolder\...` string with `explorer.exe` — on
this host that returned a non-zero exit code and opened **no** window.

The reliable launcher is PowerShell `Start-Process` with the app's
registered **URI protocol**:

```powershell
powershell.exe -NoProfile -Command "Start-Process 'ms-todo://'"
powershell.exe -NoProfile -Command "Start-Process 'outlook:'"
```

Confirm with `list_windows` — the new window's title shows up there.
**Verified:** `Start-Process 'ms-todo://'` opened "Microsoft To Do".

Common first-party URI protocols:
- Microsoft To Do → `ms-todo://`
- Outlook / Mail → `outlook:`
- People → `ms-people:`
- Settings → `ms-settings:`
- Windows Store → `ms-windows-store:`

If unsure of the protocol, search the package's registered protocols
(`Get-AppxPackage *<name>*` then check its `AppxManifest.xml` Declarations).

## Capturing UWP windows — two traps (do NOT present as a working method)

UWP apps are hosted by `ApplicationFrameHost.exe`, NOT a process named after
the app. Two capture failures were observed on this driver:

1. **`capture(app="<display name>")` fails.** e.g. `capture(app="Microsoft To Do")`
   returns *"no on-screen window matched app=…"* even though the window IS
   present in `list_windows`. The display name is not a matchable app key.
2. **`window_id` is transient.** A `window_id` returned by `list_windows`
   rotated within seconds — a later `capture(pid=…, window_id=…)` failed with
   *"No window with window_id exists"*. Re-query `list_windows` **immediately
   before** any pid/window_id capture; never reuse an id.

If SOM capture of a UWP window won't resolve, escalate to
`delivery_mode="foreground"` rather than concluding the app is undrivable
(see the verify→escalate ladder in the computer-use skill).

## Host note (Windows 11) — where the calendar lives

The classic standalone **Calendar** (Mail & Calendar) app is deprecated on
Windows 11. This user's calendar is inside **Outlook for Windows** or
**Microsoft To Do** — there is no `Calendar.exe`. Route any "open my
calendar" / "add a calendar event" request to one of those two UWP apps.
For programmatic calendar read/write + sync (Google/Outlook.com), that
needs an API/OAuth integration, not GUI clicking.

## When to use GUI clicking vs. API

- **GUI (computer_use):** the user wants you to physically open/add a
  calendar item or To Do task on their machine right now.
- **API:** recurring sync, reminders, or programmatic reads/writes — ask the
  user to grant calendar API access (OAuth token) instead of clicking.
