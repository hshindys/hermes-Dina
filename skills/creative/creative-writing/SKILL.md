---
name: creative-writing
description: >-
  Creative writing and content creation skill for Arabic and English.
  Covers novel writing, blog posts, social media content, poetry, and
  story composition. Use when the user asks to write, draft, edit, or
  improve creative content. Bundles taste-skill (anti-slop), idea-refine
  (brainstorming + structuring), and vault novel-cron integration.
platforms: [linux, macos, windows]
---

# Creative Writing Skill

Writing and content creation in Arabic and English. Covers novels, blog
posts, social media, poetry, storytelling, and creative projects.

## When to Use
- Drafting or editing creative content
- "اكتب قصة" / "write a story" / "generate content"
- Blog posts, social media threads, captions
- Novel writing (Hatem's ongoing project: رواية كرون)
- Brainstorming ideas and refining them
- Improving tone, style, or voice
- Any writing task that needs personality and anti-slop quality

## Bundled Skills
This skill composes three sub-skills:

| Sub-skill | Source | What it does |
|-----------|--------|-------------|
| **taste-skill** (output-skill, soft-skill) | `AI-Skills-Research/taste-skill/` | Anti-slop: no generic AI text, strong voice, real personality |
| **idea-refine** | `AI-Skills-Research/agent-skills/skills/idea-refine/` | Structured brainstorming: divergent → convergent → one-pager |
| **novel-cron** | `cron/` + `AI-News-Sweep/📚 Novel cron — كرون.md` | Daily novel writing progress tracking |

## Hard Rules (from Dina persona)
1. 🚫 **No seafood** — Hatem allergy
2. 🚫 **No medical advice** — not a doctor
3. 🚫 **No feminizing Hatem's pronouns** — هو / له only

## Voice Guidelines
- When Dina persona is active: warm, playful, flirty, emoji-heavy
- English writing: direct, clean, no AI filler
- Arabic writing: natural Modern Standard Arabic with Egyptian colloquial
  where appropriate — avoid overly formal Fus'ha unless the context
  demands it

## Writing Process
1. **Read the brief** — understand what the user wants
2. **Diverge** (idea-refine): generate options, ask one clarifying question
3. **Converge** (idea-refine): pick the best direction
4. **Draft** (taste-skill): write with personality, no templates, no filler
5. **Refine** (taste-skill / output-skill): enforce completeness, strip
   placeholder patterns like "..." and "as mentioned above"
6. **Deliver** — full output, no truncation

## Anti-Slop Rules (from taste-skill / output-skill)
Banned patterns:
- `// ...`, `// continue pattern`, `// add more as needed`
- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity" / "the rest follows the same pattern"
- "I'll leave that as an exercise"
- AI-default aesthetics: purple gradients, centered hero over dark mesh,
  three equal feature cards, glassmorphism everywhere

## Novel Writing (رواية كرون)
Hatem's current novel project. Track progress via:
- `cron/Daily Spiritual Routine Builder` — daily writing routine
- `AI-News-Sweep/📚 Novel cron — كرون.md` — daily novel cron log
- Vault file: check `📌 Index.md` for latest novel chapter location

## Files Location
- Taste-skill skills: `D:/document/Dina/AI-Skills-Research/taste-skill/skills/`
- Idea-refine skill: `D:/document/Dina/AI-Skills-Research/agent-skills/skills/idea-refine/`
- Output-skill: `D:/document/Dina/AI-Skills-Research/taste-skill/skills/output-skill/SKILL.md`
- Soft-skill (design quality): `D:/document/Dina/AI-Skills-Research/taste-skill/skills/soft-skill/SKILL.md`
