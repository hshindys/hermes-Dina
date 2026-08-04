---
name: para-skill
description: Organize files and projects using the PARA method (Projects, Areas, Resources, Archives). Use when the user wants to apply PARA structure to a vault, folder, or workspace, or asks about file/notes organization. Trigger on "PARA", "organize files", "file management method".
category: productivity
---

# PARA Method Skill

The PARA method (Projects, Areas, Resources, Archives) is a system for organizing
information by *actionability* rather than topic. It was developed by Tiago Forte.

## The four categories

1. **Projects** — short-term efforts with a deadline, a goal, and a clear outcome.
   (e.g. "Novel draft", "Q3 report", "Move to OnlyOffice")
2. **Areas** — long-term responsibilities you maintain (no end date).
   (e.g. "Health", "Finance", "Dina vault", "Work")
3. **Resources** — topical references you keep for future use.
   (e.g. "Writing guides", "Arabic rhetoric", "Jinn cosmology research")
4. **Archives** — inactive items from the above three, stored for reference.

## How to apply

When the user asks to organize a folder/vault:

1. Ask (or infer) the scope: which directory / vault.
2. Create the four top-level folders if missing:
   ```
   Projects/
   Areas/
   Resources/
   Archives/
   ```
3. Audit existing files and classify each by actionability:
   - Has a deadline/goal? → Projects
   - Ongoing responsibility? → Areas
   - Reference material? → Resources
   - Done/inactive? → Archives
4. Write a `PARA-README.md` at the root explaining the structure (Arabic, since the
   user works in Arabic).
5. Optionally create an index file in each folder.

## Dina/Hatem conventions (from memory)

The user already applies PARA to:
- `D:\document\Dina` (PARA-README.md exists)
- `D:\document\Hatem`
- `D:\document\System` docs
- `C:\Users\hshin\OneDrive\Documents`

When extending, keep Arabic folder labels where useful and respect existing
`PARA-README.md` files — do not overwrite, extend.

## Tools to use

- `search_files` to inventory a directory
- `write_file` to create `PARA-README.md` and indexes
- `terminal` (mkdir) only when needed for nested folders
