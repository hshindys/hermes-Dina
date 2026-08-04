# Microsoft To Do — adding a task via computer_use (verified working sequence)

Environment: Windows 10/11 host, user `hshin`, account `hshindys@hotmail.com`.
Driver: `cua-driver.exe` (background). App: Microsoft To Do (UWP, hosted by ApplicationFrameHost.exe).

## Launch
```
powershell.exe -NoProfile -Command "Start-Process 'ms-todo://'"
```
sleep ~4s.

## Locate the window
`list_windows` → the titled "Microsoft To Do" window is owned by `ApplicationFrameHost.exe`
(pid was 9280, window_id 263780). The `Todo.exe` process only owns a "PopupHost" placeholder.
Capture with `pid`+`window_id` of the host, NOT by `app="Microsoft To Do"` (that returns 0x0).

## Add a task to "My Day" (the reliable recipe)
1. Navigate to My Day: `click` element index of the "My Day" ListItem (delivery_mode: foreground),
   then confirm header reads "My Day" / "Sunday, August 2".
2. Click the bottom "Add a task" bar by COORDINATE (element-index clicks on this field are flaky):
   `click coordinate=[680,779] delivery_mode=foreground`
3. `type text="<task>" delivery_mode=foreground`
4. `capture mode=vision` → confirm the text is visibly rendered in the field (vision reads Arabic
   + emoji). If empty, re-click the coordinate and re-type.
5. `key keys=return delivery_mode=foreground` EXACTLY ONCE.
6. `capture mode=vision` (or `mode=som`) → confirm the task appears as an unchecked item.

## Pitfalls hit during the live session
- Background `type`/`key` (no delivery_mode) returned `effect: unverifiable` and text NEVER landed.
  Always use `delivery_mode: foreground`.
- Pressing Enter MORE THAN ONCE toggled the task to "Completed" (filed under a "Completed N" group)
  instead of leaving it active. Press Enter once only.
- Element indices on the Suggestions panel / empty-state reshuffle between captures; prefer
  coordinate clicks for the input field and verify by vision after each step.
- The right "Suggestions" panel stayed open and could occlude clicks; it did not block the bottom
  input bar, but closing it (`Hide suggested tasks` X) reduces noise.

## Outcome
Successfully created "☕ قهوة الصبح على البلكونة" in My Day (one stray extra Enter marked it
Completed; un-check via the task's checkbox). Confirms the driver + foreground-input recipe works.

## Bulk / reliable alternative
For many tasks or guaranteed active/incomplete state, use the Microsoft Graph API
(`/me/todo/lists/.../tasks`) with account consent instead of SendInput.
