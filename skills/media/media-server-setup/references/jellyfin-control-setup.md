# Jellyfin Control — Setup Notes

## Installation

```bash
hermes skills install jellyfin-control
```

Installed at: `~/AppData/Local/hermes/skills/jellyfin-control/`

## Environment Variables (from session 2026-07-29)

```bash
JF_URL=http://localhost:8096
JF_API_KEY=74e663d2d7244887ae8c312a0b024ff1
JF_USER=Hatem
```

Added to `~/.hermes/.env`.

## Verified Working Commands

- `node cli.js stats` — returns library stats (30 movies, 17 series, 351 episodes, 75 songs)
- `node cli.js scan` — triggers library refresh, picks up new media files
- `node cli.js search "query"` — searches library (requires valid user ID)

## Common Issues

- `searchItem` returns 400 Bad Request → check `JF_USER_ID` matches a valid Jellyfin user ID integer
- `scan` requires admin API key — will fail gracefully with 403 if key lacks admin privileges
- `cli.js` requires `node_modules/` installed — run `npm install` in the skill directory if `Cannot find module` errors

## Key Files

- `cli.js` — main CLI entry point
- `jellyfin.js` — Jellyfin REST API (auth, search, sessions, playback, refreshLibrary)
- `tv.js` — TV control (Home Assistant, WebOS, ADB)
- `SKILL.md` — full usage docs