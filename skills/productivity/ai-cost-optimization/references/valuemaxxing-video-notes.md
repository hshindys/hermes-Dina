# Valuemaxxing Video — Session-Specific Notes

> Source: https://www.youtube.com/watch?v=OCwNqESh-HA
> Duration: 9:00
> Presenter: Boris Cherny (Hermes agent creator) with Zapier

## Key Numbers

| Metric | Tokenmaxxing (Hermes agent) | Valuemaxxing (Zapier + AI) |
|--------|----------------------------|----------------------------|
| Cost per video | $1.66 | $0.11 |
| Tokens spent | ~500,000 | 4,700 |
| AI steps | 5+ (all cost money) | 1 (copywriting only) |
| Result quality | Same | Same |
| Savings | — | **93%** |

## Zapier Steps (Deterministic = $0)

1. **YouTube trigger** — fires on new video upload
2. **Super Data** — grabs YouTube transcript via webhook
3. **Formatting step** — maps transcript to AI input
4. **Claude Fable 5** — writes newsletter + LinkedIn + Skool post ($0.11)
5. **Telegram distribution** — sends to @hshindy (free)
6. **Optional**: email via Kit, Skool integration

## The "one judgment step" principle

Only the AI copywriting step needs a model that can write. Everything else is:
- Data fetching (YouTube API → Super Data)
- Routing (Zapier triggers)
- Delivery (Telegram bot)

All deterministic, all free, all reliable.

## The YouTube Transcript Tool (Hermes helper)

The `fetch_transcript.py` script uses `youtube-transcript-api`.
On Windows, `python3` redirects to MS Store stub — fails silently.
Fix: use the Hermes venv Python directly:
```
/c/Users/hshin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
-c "import youtube_transcript_api"
```
Or run the helper script directly:
```
/c/Users/hshin/AppData/Local/hermes/skills/media/youtube-content/scripts/fetch_transcript.py "URL" --text-only --timestamps
```

## The Hermes Agent Cost Experiment

In the session, the agent ran a 4-step workflow (transcript → newsletter → LinkedIn → community post → telegram) costing $0.67 before the video was even fully processed. After adding a self-improvement skill, it hit $1.66 with 500K+ tokens. Same task, Valuemaxxing version would cost $0.11.