---
name: media-server-setup
description: Set up Jellyfin skills for Hermes media control.
metadata:
  hermes:
    tags: [media, server, jellyfin, setup]
---

# Media Server Setup

Set up AI-agent skills for controlling self-hosted media servers through Hermes.

## Workflow

1. Search the hub: `hermes skills search jellyfin`
2. Install: `hermes skills install <identifier>`
3. Configure env vars in `~/.hermes/.env`
4. Verify: `node cli.js stats`

## Config

```bash
JF_URL=http://localhost:8096
JF_API_KEY=your-key
JF_USER=your-username
```

## Common Ops

- `scan` — trigger library scan for new media
- `search "query"` — search library
- `stats` — library stats
- `resume "title"` — resume playback

## Security

- Never commit API keys to workspace files or git
- Use least-privilege keys when possible
- Keep `.env` permissions restricted

## Setup Notes

See [references/jellyfin-control-setup.md](references/jellyfin-control-setup.md) for installation walkthrough, environment variable details, and troubleshooting common issues (400 errors on search, admin key requirements for scan, npm install fix).