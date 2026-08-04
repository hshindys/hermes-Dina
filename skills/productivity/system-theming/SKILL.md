---
name: system-theming
description: Change Windows fonts, DPI, and text size.
---

# System Theming (Windows)

Customize Windows desktop: fonts, DPI scaling, ClearType, and related settings.

## Triggers
- User asks to install a font, change the default font, or adjust display scaling
- User says make text bigger or change DPI
- Running `hermes backup` or other Windows-native tools that mangle POSIX-style paths
- User reports font changes did not take effect

## Workflow

### 1. Install a font per-user
1. Download the ttf/otf file to ~/AppData/Local/Fonts/ (create if missing).
2. Register it in the user registry so Windows discovers it without admin:
   ```powershell
   New-ItemProperty -Path 'HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts' `
     -Name '<FontName> (TrueType)' -Value '<filename.ttf>' -PropertyType String -Force
   ```
3. Restart Explorer to refresh the font cache:
   ```powershell
   Stop-Process -Name explorer -Force; Start-Sleep 3; Start-Process explorer.exe
   ```

### 2. Change DPI scaling (make text bigger)
Set LogPixels in HKCU:\Control Panel\Desktop:
| Scale | DPI | LogPixels |
|-------|-----|-----------|
| 100%  | 96  | 96        |
| 125%  | 120 | 120       |
| 150%  | 144 | 144       |
| 175%  | 168 | 168       |
| 200%  | 192 | 192       |

After changing, log off/on. Also update WindowMetrics heights proportionally (CaptionHeight, MenuHeight, SmCaptionHeight — more negative = taller).

### 3. Set default UI font via WindowMetrics
To make a font the system default, set the binary CaptionFont, MenuFont, MessageFont, StatusFont, and SmCaptionFont values in HKCU:\Control Panel\Desktop\WindowMetrics to the UTF-16LE-encoded font name bytes.

### 4. Variable vs Static fonts
Google Fonts CSS2 API gives a static Bold ttf (e.g., family=Cairo:wght@700). For variable fonts (e.g., Cairo[slnt,wght].ttf), use fonttools to extract a static instance at the desired wght value instead of relying on Windows to pick the right axis.

### 4. MSYS path mangling warning
Bash-on-Windows can double-rewrite Windows paths. /d/Backup becomes C:\d\Backup (a phantom drive). To avoid:
- Always pass Windows paths in native form: D:/Backup/... or C:/Users/...
- Never pass POSIX paths like /d/... to Windows-native tools
- Verify the actual file exists by checking with native Windows paths

## Pitfalls
- Variable fonts do not expose Bold to Windows reliably. The fvar table defaults to Regular. Use the static variant from the CSS2 API.
- MSYS doubles backslashes in heredocs. Use forward slashes or single-quoted Windows paths.
- Permission denied writing to C:\Windows\Fonts without admin. Per-user install works identically.
- LogPixels change requires logoff. It does not take effect live.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.
- **Bash-on-Windows path mangling**: bash can double-rewrite Windows paths (e.g., /d/Backup → C:\d\Backup). Always pass Windows paths in native form (C:/Users/... or D:/document/...) and never POSIX-style (/d/...). Verify the actual file exists with native paths.