---
name: ai-cost-optimization
description: "Cut AI costs via Valuemaxxing pipelines."
platforms: [linux, macos, windows]
---

# AI Cost Optimization — Valuemaxxing

## When to use

Use when the user wants to reduce AI API costs for recurring workflows. Activated when: user says "reduce AI costs", "cheapen the pipeline", or shares a Valuemaxxing tokenmaxxing video.

## Core Methodology

The Valuemaxxing framework has 5 rules:

1. **Identify the judgment step** — Only ONE step in any workflow actually needs AI. Find it.
2. **Make everything else deterministic** — Data fetching, routing, formatting, distribution — all free/non-AI steps.
3. **Use a single strong model for the AI step** — One call for the judgment/creative step. No chaining multiple AI calls.
4. **Batch where possible** — One prompt producing multiple outputs beats multiple single-output prompts.
5. **Measure everything** — Track tokens and dollars per run. Formula: `cost = token_count × model_rate`.

## Cost Comparison Pattern

| Approach | Cost per run | Tokens | When to use |
|----------|-------------|--------|-------------|
| Full AI pipeline (Tokenmaxxing) | $1.00+ | 500K+ | Only if you have no other option |
| Hybrid (Valuemaxxing) | $0.11 | ~4,700 | Default — AI for writing, everything else deterministic |
| Fully deterministic | $0.00 | 0 | Everything non-AI |

## Deterministic Steps (free)
- Data fetching (YouTube API, web scraping, database queries)
- Formatting & routing (JSON transformation, column mapping)
- Distribution (Telegram bot, email via SMTP, webhooks)
- Scheduling (cron triggers, event-based triggers)

## AI Step (costs tokens)
- Writing/copying where judgment matters
- Summarization requiring nuance
- Classification requiring context understanding
- Creative generation

## Platform Notes (Windows)

On Windows, `python3` resets to the MS Store stub. Use Hermes-managed Python directly:
```bash
/c/Users/hshin/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe
```
For `uv run`, set `script_venv` in config to avoid MS Store redirect. Also see: `scripts/youtube_valuemaxxing.py`.

## OKF Knowledge Base Integration

When the user shares a Cole Medin OKF video (YouTube link, e.g., `8JWhwhxWtJw`), apply the OKF methodology to the Dina vault:
1. Clone Cole's repo (or the Google OKF spec repo) into `📚 Knowledge-Bases/`
2. Use `okf-cli.py` to generate the knowledge base from a YouTube channel URL
3. Copy concept files into `📚 Knowledge-Bases/concepts/`
4. Update `index.md` with new themes and entities
5. Dina agents can query the knowledge base directly — no embeddings, no database

The OKF bundle structure mirrors Cole Medin's repo: `raw/`, `concepts/`, `entities/`, `index.md`.

## Pitfalls

- **Don't use AI for data fetching** — youtube-transcript-api, web scraping, API calls are all free. Don't route them through an LLM.
- **Don't chain AI agents** — Each handoff burns tokens on context passing. One model, one prompt, one output.
- **Don't ignore setup cost** — Building a deterministic pipeline once costs time but zero recurring tokens. Break-even is usually 2-3 runs.
- **OKF bundles are read-only for agents** — The knowledge base is a reference, not writable state. Agents query it; humans update it.
3. Copy concept files into `📚 Knowledge-Bases/concepts/`
4. Update `index.md` with new themes and entities
5. Dina agents can query the knowledge base directly — no embeddings, no database

The OKF bundle structure mirrors Cole Medin's repo: `raw/`, `concepts/`, `entities/`, `index.md`.

## Pitfalls

- **Don't use AI for data fetching** — youtube-transcript-api, web scraping, API calls are all free. Don't route them through an LLM.
- **Don't chain AI agents** — Each handoff burns tokens on context passing. One model, one prompt, one output.
- **Don't ignore setup cost** — Building a deterministic pipeline once costs time but zero recurring tokens. Break-even is usually 2-3 runs.
- **OKF bundles are read-only for agents** — The knowledge base is a reference, not a writable state. Agents query it; humans update it.

## Workflow Template

```
Trigger (deterministic) → Fetch (deterministic) → Transform (deterministic) → AI step (judgment only) → Distribute (deterministic)
```

## Verification

After setting up a Valuemaxxing pipeline:
1. Run with AI for 3 runs — record avg cost/tokens
2. Rebuild as deterministic pipeline — record avg cost/tokens
3. Compare — target ≥70% cost reduction
4. If savings < 70%, re-examine which steps actually need AI judgment

## Related Skills

- `youtube-content` — fetch transcripts for OKF knowledge base pipelines