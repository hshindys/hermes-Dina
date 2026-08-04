---
name: windows-desktop-automation
description: Drive Windows GUI apps via computer_use/cua-driver reliably.
---

# Windows Desktop Automation (computer_use / cua-driver)

Use this when a task needs to interact with a Windows desktop app: Microsoft To Do / tasks,
the (now-removed) Calendar, Outlook, File Explorer, Settings, or any GUI click-through.
On this Windows 10/11 host the `computer_use` tool is backed by **cua-driver** and runs in
the BACKGROUND (it does not steal the user's cursor), so you and the user can share the desktop.

## Step 0 — Verify the driver is actually alive
`computer_use action=list_apps` should return a long JSON array of running apps. If you see
`cua-driver.exe` in the list, the driver is up and you can drive the desktop. Do this before
claiming anything about the desktop.

## Step 1 — Launch the target app
- Win32 apps: `terminal` with `explorer.exe "<shell:appsFolder\\...>"` or `Start-Process`.
  Run launchers in the background (`terminal background=true`) — do NOT use `&` in foreground.
- UWP apps are most reliably launched via a URI scheme:
  - Microsoft To Do → `powershell.exe -NoProfile -Command "Start-Process 'ms-todo://'"`
  - Outlook → `Start-Process 'outlook:'`
  - Then `sleep` ~3–4s for the window to appear.

## Step 2 — Find the REAL window (UWP quirk — easy to get wrong)
For UWP apps (To Do, Mail, Calendar, Settings), the process you launched often only owns a
placeholder `"PopupHost"` window. The **actual visible window is hosted by
`ApplicationFrameHost.exe`**. So:
1. `computer_use action=list_windows` → find the app by title (e.g. "Microsoft To Do") and note
   its `pid` + `window_id`. The title window usually belongs to `ApplicationFrameHost.exe`, NOT
   to `Todo.exe`/`ShellExperienceHost.exe`.
2. `capture` with **`pid` + `window_id` of that host window** (e.g. pid 9280, window_id 263780).
   Capturing by `app=` string alone often returns a 0x0 empty window.

## Step 3 — THE PITFALL: background input is "unverifiable"
Default `computer_use` input (`delivery_mode` omitted = background) returns
`effect: "unverifiable"` for typing and keystrokes — the driver cannot read the field back, so
you CANNOT trust text landed. Symptoms: you "type" into a field, capture shows nothing, the
AX tree still shows the empty placeholder.
**Fix:** always pass `delivery_mode: "foreground"` for `type` and `key` actions, and
**verify with a follow-up `capture` (mode=vision) before pressing Enter**. Foreground mode uses
SendInput and the driver confirms the characters were dispatched.

## Step 4 — Focus an input field reliably
Clicking by element **index** on UWP text fields is flaky (indices reshuffle every capture, and
the field often doesn't expose a ValuePattern). The reliable path for a "Add a task" style field:
1. `computer_use action=click coordinate=[x,y] delivery_mode=foreground` on the field's screen
   coordinates (for the My Day "Add a task" bar this was ~`[680, 779]`).
2. `type` the text with `delivery_mode: foreground`.
3. Immediately `capture mode=vision` and confirm the text is visible in the field (the auxiliary
   vision model reads Arabic/emoji text fine).
4. Only then `key keys=return delivery_mode=foreground` to save.

## Step 5 — Enter pitfall (Microsoft To Do)
Pressing `Enter` **more than once** on a freshly typed task can toggle it to **Completed**
instead of leaving it active — the AX tree then files it under a "Completed N" group. If you
need the task to stay active, press Enter exactly once and verify it appears as an unchecked
item. To un-complete, click the task's checkbox (element index from a fresh SOM capture).

## Step 6 — If GUI clicking is too slow/error-prone, offer the API path
When the user wants many items or reliable read/write, propose the programmatic route instead of
pixel-poking: Microsoft To Do tasks are reachable via the **Microsoft Graph API** once the
account (e.g. `hshindys@hotmail.com`) grants consent. That gives 100% reliable add/edit/read and
enables reminders — far better than foreground SendInput for bulk work.

## Known Windows 11 environment fact
The standalone **Mail & Calendar (windowscommunicationsapps)** app is gone on this machine; the
calendar lives inside **Outlook for Windows** and **Microsoft To Do**. Don't hunt for a separate
"Calendar" UWP — open To Do (tasks) or Outlook (events).

## Reference
- `references/microsoft-todo-recipe.md` — exact step-by-step that worked for adding a My Day task,
  with the capture/verify sequence and the coordinates that succeeded.
