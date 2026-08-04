# Jellyfin Control — Setup Notes

## Session Context (2026-07-29)

User asked to install "KellyFin" (doesn't exist as standalone) and set up Jellyfin as their media server. The hub-installed `jellyfin-control` v1.3.0 (clawhub, Titunito) is the correct and closest match.

## What was done

1. Installed `jellyfin-control` via `hermes skills install "Jellyfin Control" --force`
2. Installed npm dependencies: `npm install` (axios, fuse.js, ws, yargs)
3. Fixed missing `lib/` directory — copied `jellyfin.js` and `tv.js` into `lib/`
4. Verified CLI works: `node cli.js --help` shows all commands including `scan`

## Config needed (not yet done — requires user's server details)

The user needs to provide:
- `JF_URL` — their Jellyfin server URL (e.g. `http://192.168.1.xxx:8096`)
- `JF_API_KEY` — from Jellyfin Dashboard → Advanced → API Keys
- `JF_USER` — optional, their Jellyfin username

## Key insight for future sessions

The `scan` command (`node cli.js scan`) triggers `POST /Library/Refresh` on the Jellyfin API, which scans all configured media folders for new content. This is what the user needs when they say "make jelly fin search the folders for new media."

## Protected skills note

Hub-installed skills (like `jellyfin-control`) cannot be patched via `skill_manage`. The wrapper skill `jellyfin-control-wrapper` in the `media` category provides Hermes-specific guidance for this hub skill.