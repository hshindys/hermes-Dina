---
name: jellyfin-control-wrapper
description: Use when controlling Jellyfin media server from Hermes.
version: 1.0.0
author: Hermes Agent (adapted from Titunito)
license: ISC
metadata:
  hermes:
    tags: [media, streaming, jellyfin]
    related_skills: []
---

# Jellyfin Control — Hermes Wrapper

Wrapper for hub-installed `jellyfin-control` (clawhub, v1.3.0). Hub skills are read-only; this wraps them with Hermes guidance.

## Quick Start

1. Get API key: Jellyfin Dashboard → Advanced → API Keys → create "Hermes"
2. Configure `openclaw.json` with `JF_URL`, `JF_API_KEY`
3. Install deps: `cd ~/.hermes/skills/jellyfin-control/ && npm install`
4. Ensure `lib/` dir exists: `mkdir -p lib && cp jellyfin.js lib/ && cp tv.js lib/`
5. Test: `JF_URL=http://YOUR_IP:8096 JF_API_KEY=YOUR_KEY node cli.js stats`

## Key Commands

- `node cli.js scan` — trigger library scan (admin key required)
- `node cli.js stats` — library statistics
- `node cli.js search "query"` — search content
- `node cli.js resume "query"` — resume playback
- `node cli.js tv play "query"` — one-command play (TV + Jellyfin)
- `node cli.js control pause` — remote control

## Troubleshooting

- `MODULE_NOT_FOUND` for `lib/jellyfin` — copy `jellyfin.js` and `tv.js` into `lib/` dir
- `JF_API_KEY is required` — set env var or configure `openclaw.json`
- Scan fails with 403 — API key needs admin privileges