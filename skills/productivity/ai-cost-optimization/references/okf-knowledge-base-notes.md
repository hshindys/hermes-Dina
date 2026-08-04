# OKF Knowledge Base — Session Notes

> Captured from Cole Medin's OKF video and subsequent Dina vault setup.
> Video: https://www.youtube.com/watch?v=8JWhwhxWtJw
> Duration: ~14:56

## OKF Spec Key Points

- **Agent→knowledge base** standard (complement to MCP agent→tool, A2A agent→agent)
- **Markdown-only** — no database, no embeddings, no API needed
- **Bundles** are plain folders of markdown files with YAML frontmatter
- **index.md** is the master navigation file with themes and concepts
- **raw/** contains original transcripts/sources
- **concepts/** aggregates concepts across multiple sources
- **entities/** catalogues tools and platforms
- **knowledge-graph/** Obsidian backlinks for graph view

## OKF v0.2 Changes (from Google Cloud repo)

- `generated:{by, at}` replaces `timestamp`
- `sources` frontmatter family for provenance tracking
- `type` is the only always-required key
- Trust tiers: `generated`, `verified`
- Status lifecycle: `active`, `deprecated`, `stale_after`

## Cole Medin's YouTube Channel Bundle

Repos: Cole's repo + Google's reference implementation
- Cole's: coleam00/cole-medin-ai-coding (5 videos, 5 concepts, okf-cli.py)
- Google's: GoogleCloudPlatform/knowledge-catalog (OKF spec + bundles)

## Workflow for Dina Vault

1. User shares OKF video URL
2. Fetch transcript via youtube-transcript-api (free, deterministic)
3. Clone Cole's repo or Google OKF repo into 📚 Knowledge-Bases/
4. Use okf-cli.py to generate knowledge base for any YouTube channel
5. Copy relevant concepts into 📚 Knowledge-Bases/concepts/
6. Update index.md with new themes + entities
7. Dina agents query via the prompt in 📚 Knowledge-Bases/README.md

## Cost

- Setup: $0.00 (git clone + manual copy)
- AI copywriting step: $0.11 per batch
- Ongoing queries: $0.00 (local markdown, no API)

## Pitfalls

- Cole's repo is NOT the same as Cole's channel knowledge base — the repo is the OKF bundle format reference; the channel bundle is what Cole built for his own videos
- okf-cli.py requires Python stdlib only — no pip install needed
- OKF bundles are READ-ONLY for AI agents (agents query, humans update)