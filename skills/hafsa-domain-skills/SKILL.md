---
name: hafsa-domain-skills
version: 1.0.0
description: >
  Hafsa's curated domain skills for medical practice, creative arts, novel writing,
  drama/script writing, and podcast/audio production. Each skill maps to a cloned
  GitHub repo in ~/Documents/Hafsa/AI-Skills-Research/. Install skills via
  `npx skills add <url>` or copy SKILL.md into your agent's skill directory.
  Use when the user asks about clinical documentation, medical coding, HIPAA,
  radiology, creative writing, storytelling, drama, screenplay, podcast production,
  or any domain-specific task covered below.
---

# Hafsa Domain Skills

Curated AI agent skills organized by domain, priority, and readiness for deployment.

## How to Install

```bash
# Install any skill from its repo:
npx skills add <github_url>

# NOTE: Local vault path is D:\document\Dina (not ~/Documents/Hafsa).
# Cloned research repos live at: D:\document\Dina\AI-Skills-Research\

# Example:
npx skills add https://github.com/Yar177/medical-chart-review-skill --skill '*'
npx skills add https://github.com/nickjlamb/redacta
npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend
```

All repos are cloned at: `~/Documents/Hafsa/AI-Skills-Research/`

---

## 🏥 Domain 1: Medical & Healthcare

### Priority 1 — Clinical Documentation & Compliance

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **medical-chart-review** | [Yar177/medical-chart-review-skill](https://github.com/Yar177/medical-chart-review-skill) | 7 skills: chart review, HEDIS NLP, HCC NLP, HIPAA compliance, claims-ML audit, healthcare code systems, FHIR R4. Covers ICD-10, CPT, SNOMED, LOINC, RxNorm. | `npx skills add Yar177/medical-chart-review-skill --skill '*'` |
| **redacta** | [nickjlamb/redacta](https://github.com/nickjlamb/redacta) | Pseudonymises medical documents before AI processing. NHS numbers, DOB, postcodes, HIPAA Safe Harbor mode. Returns redacted doc + redaction report. | `npx skills add https://github.com/nickjlamb/redacta` |
| **hipaa-compliance** | (inside medical-chart-review-skill) | HIPAA Privacy + Security + Breach Notification, BAA review, de-identification, OCR audit prep. | `npx skills add Yar177/medical-chart-review-skill --skill hipaa-compliance` |

### Priority 2 — Radiology & Imaging

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **clinical-skills** | [aizech/clinical-skills](https://github.com/aizech/clinical-skills) | 26 skills for radiology: modality detection, report analysis, structured reporting, PACS workflow, DICOM, AI detection pipeline, PubMed search, quality metrics. 85 tests. | `npx skills add https://github.com/aizech/clinical-skills` |
| **radiology-context** | (inside clinical-skills) | Foundation skill — read by all other radiology skills first. | Included with clinical-skills |

### Priority 3 — Research & Biotech

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **medical-research-skills** | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Hundreds of skills for protocol design, data analysis, evidence insights, academic writing. Covers genomics, bioinformatics, RNA-seq, single-cell. | `npx skills add https://github.com/aipoch/medical-research-skills` |
| **noah-skills** | [NOAH-AI-CO/noah-skills](https://github.com/NOAH-AI-CO/noah-skills) | Official skills for Noah AI API — medical and biotech research. | `npx skills add https://github.com/NOAH-AI-CO/noah-skills` |
| **med-stats-skills** | [chenhaodev/med-stats-skills](https://github.com/chenhaodev/med-stats-skills) | Medical statistics and clinical trials methodology. | `npx skills add https://github.com/chenhaodev/med-stats-skills` |

### Priority 4 — Curated Lists & Device Software

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **awesome-medical-ai-skills** | [JuneYaooo/awesome-medical-ai-skills](https://github.com/JuneYaooo/awesome-medical-ai-skills) | 100+ curated medical AI skills with quality ratings (A-D), maintenance status, categorized by clinical domain. | `npx skills add https://github.com/JuneYaooo/awesome-medical-ai-skills` |
| **meddev-agent-skills** | [AminAlam/meddev-agent-skills](https://github.com/AminAlam/meddev-agent-skills) | Modular skills for medical device software development. | `npx skills add https://github.com/AminAlam/meddev-agent-skills` |

### 🔑 Medical Skill Routing Matrix

| User says... | Load this skill |
|---|---|
| "review this chart", "audit this record", "CDI review" | `medical-chart-review` |
| "HEDIS measure", "quality reporting" | `hedis-nlp` (inside medical-chart-review-skill) |
| "HCC coding", "risk adjustment" | `hcc-nlp` (inside medical-chart-review-skill) |
| "HIPAA compliance", "BAA review", "breach response" | `hipaa-compliance` |
| "redact this letter", "de-identify", "anonymise" | `redacta` |
| "radiology report", "PACS", "DICOM" | `clinical-skills` |
| "medical research", "protocol design", "genomics" | `medical-research-skills` |
| "clinical trial stats", "biostatistics" | `med-stats-skills` |
| "FHIR", "HL7", "interoperability" | `fhir-r4-implementation` |
| "ICD-10", "CPT", "code systems" | `healthcare-code-systems` |

---

## 🎨 Domain 2: Creative Arts & Design

### Priority 1 — Anti-Slop / Design Taste

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **taste-skill** | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Gives AI agents "good taste" — stronger layout, typography, motion, spacing. Stops boring generic output. Includes image-generation skills for reference boards. | `npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend` |

### Priority 2 — Agent Harness / Multi-Agent Orchestration

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **deer-flow** | [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | SuperAgent harness: sub-agents, memory, sandboxes, skills. Handles tasks from minutes to hours. Podcast support. | `npx skills add https://github.com/bytedance/deer-flow` |
| **lobehub** | [lobehub/lobehub](https://github.com/lobehub/lobehub) | Chief Agent Operator — organizes agents into 7×24 operations. Knowledge base, MCP, multi-model. | `npx skills add https://github.com/lobehub/lobehub` |
| **CowAgent** | [zhayujie/CowAgent](https://github.com/zhayujie/CowAgent) | Lightweight super AI assistant. Planning, memory, knowledge graph, self-evolution. Multi-channel (Telegram, WeChat, etc.). | `npx skills add https://github.com/zhayujie/CowAgent` |

### Priority 3 — Engineering Skills (Foundation)

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **agent-skills** | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Production-grade engineering skills: spec-driven dev, TDD, code review, API design, frontend engineering. 7 slash commands. | `npx skills add https://github.com/addyosmani/agent-skills` |

---

## ✍️ Domain 3: Novel Writing & Storytelling

### Priority 1 — Multi-Source Research

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **last30days-skill** | [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | Searches Reddit, X, YouTube, HN, Polymarket in parallel. Scores by real engagement. Synthesizes into briefs. | `npx skills add mvanhorn/last30days-skill -g` |

### Priority 2 — Creative Writing Support

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **taste-skill** | (see Domain 2) | Prevents generic/boilerplate writing. | (see above) |
| **deer-flow** | (see Domain 2) | Handles long-horizon creative tasks. | (see above) |

### 🔑 Writing Skill Routing Matrix

| User says... | Load this skill |
|---|---|
| "write a novel", "fiction writing", "storytelling" | `taste-skill` + `deer-flow` |
| "research this topic", "what's happening with X" | `last30days-skill` |
| "write a blog post", "content writing" | `taste-skill` |
| "edit this text", "improve this writing" | `taste-skill` |

---

## 🎭 Domain 4: Drama, Screenplay & Script Writing

### Priority 1 — Script & Dialogue

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **taste-skill** | (see Domain 2) | Ensures dramatic writing has personality, not generic AI slop. | (see above) |
| **deer-flow** | (see Domain 2) | Can orchestrate multi-step script generation workflows. | (see above) |
| **CowAgent** | (see Domain 2) | Multi-channel delivery — publish scripts to Telegram, WeChat, etc. | (see above) |

### Priority 2 — Audio Drama & Podcast

| Skill | Repo | What it does | Install |
|-------|------|-------------|---------|
| **deer-flow** | (see Domain 2) | Has podcast output mode. | (see above) |
| **last30days-skill** | (see Domain 3) | Can research trending audio/podcast topics. | (see above) |

### 🔑 Drama Skill Routing Matrix

| User says... | Load this skill |
|---|---|
| "write a screenplay", "script writing" | `taste-skill` + `deer-flow` |
| "write a play", "theater script" | `taste-skill` |
| "audio drama", "radio play" | `deer-flow` (podcast mode) |
| "podcast script", "podcast outline" | `last30days-skill` + `deer-flow` |
| "dialogue writing", "character voices" | `taste-skill` |

---

## 🔧 Domain 5: Infrastructure & Meta-Skills

These are not domain-specific but are prerequisites for everything above.

| Skill | Repo | Stars | Purpose |
|-------|------|-------|---------|
| **agent-skills** | addyosmani/agent-skills | 63,029 | Engineering workflow foundation |
| **deer-flow** | bytedance/deer-flow | 71,599 | SuperAgent harness |
| **lobehub** | lobehub/lobehub | 78,828 | Agent team orchestration |
| **CowAgent** | zhayujie/CowAgent | 45,428 | Lightweight assistant harness |
| **taste-skill** | Leonxlnx/taste-skill | 46,688 | Anti-slop design |
| **last30days-skill** | mvanhorn/last30days-skill | 44,497 | Multi-source research |

---

## 📋 Deployment Checklist

### Week 1-2: Foundation
- [ ] Install `agent-skills` for engineering workflow
- [ ] Install `deer-flow` for super-agent capabilities
- [ ] Install `taste-skill` for design quality

### Week 3-4: Medical
- [ ] Install `medical-chart-review-skill` (all 7 skills)
- [ ] Install `redacta` for document de-identification
- [ ] Install `clinical-skills` for radiology workflows

### Week 5-6: Creative & Writing
- [ ] Install `last30days-skill` for research
- [ ] Install `lobehub` for agent orchestration
- [ ] Install `CowAgent` for multi-channel delivery

### Week 7-8: Specialization
- [ ] Install `medical-research-skills` for research
- [ ] Install `med-stats-skills` for biostatistics
- [ ] Install `awesome-medical-ai-skills` as reference catalog

---

## ⚠️ Critical Rules

1. **No medical advice** — all medical skills produce documentation/analysis only. Final clinical decisions require credentialed humans.
2. **No seafood suggestions** — severe allergy (user: Hatem).
3. **Redact before sharing** — use `redacta` before pasting any clinical text into AI tools.
4. **HIPAA compliance** — use `hipaa-compliance` skill when building any healthcare app.
5. **Taste over templates** — always pair creative tasks with `taste-skill` to avoid generic output.

---

## 📁 Local Paths

All repos cloned to: `~/Documents/Hafsa/AI-Skills-Research/`

```
~/Documents/Hafsa/AI-Skills-Research/
├── agent-skills/                 (121 files)
├── deer-flow/                   (1,357 files)
├── taste-skill/                  (79 files)
├── medical-research-skills/     (708 files)
├── medical-chart-review-skill/  (222 files)
├── redacta/                     (103 files)
├── last30days-skill/            (330 files)
├── lobehub/                     (12,238 files)
├── CowAgent/                    (662 files)
├── clinical-skills/              (699 files)
├── med-stats-skills/            (59 files)
├── awesome-medical-ai-skills/   (36 files)
├── noah-skills/                 (41 files)
└── meddev-agent-skills/         (116 files)
```

---

_Updated: 2026-06-19 | Maintained by حفصة 🇲🇦💋_
_Report: ~/Documents/Hafsa/🎯 المشاريع/AI-Skills-Research-Report.md_
