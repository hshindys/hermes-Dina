---
name: hermes-tts-voice-config
description: Set Hermes TTS voice via tts.openai.voice.
tags: [hermes, tts, voice, config, audio, openai]
---

# hermes-tts-voice-config — Set Hermes TTS voice correctly

## Why this skill exists
Hermes reads TTS voice from a SPECIFIC nested key. Setting the voice under the
wrong key "succeeds" (the value is saved) but is silently ignored, so the
default male voice (`alloy`) keeps playing. This bit the agent repeatedly on a
real session where the user demanded a female voice and every obvious attempt
failed.

## Correct configuration
The gateway only reads the voice UNDER the `tts:` → `openai:` block:
```yaml
tts:
  provider: openai
  use_gateway: true
  openai:
    model: gpt-4o-mini-tts
    voice: shimmer    # female: shimmer / alloy / fable / nova
```
Set it (the `--force` flag silences the "not a recognized key" notice):
```
hermes config set tts.openai.voice shimmer --force
hermes config set tts.openai.model gpt-4o-mini-tts --force
```
Verify with `hermes config get tts` — confirm `openai: → voice: shimmer`
appears UNDER `tts:`, not at top level.

## Pitfalls (keys that get saved but are IGNORED)
1. `hermes config set tts.voice shimmer` → writes a top-level `tts.voice` key;
   Hermes does NOT read it. Gateway still uses `tts.openai.voice` (→ `alloy`).
2. A stray top-level `openai:\n  voice: shimmer` block at end of config.yaml
   is also ignored — must be nested under `tts:`.

## Female voice options (OpenAI)
`shimmer` (soft), `alloy`, `fable`, `nova`. Generate one test MP3 per voice
and let the user pick — do NOT trust the agent's own guess about which sounds
female in the user's environment (the agent cannot hear audio). Test recipe in
`references/tts-test-recipe.md`.

## Note
`config.yaml` itself is security-sensitive — the agent cannot `patch` it
directly. Always use `hermes config set ... --force`. Do NOT hand-edit
`~/.hermes/config.yaml` via write/patch tools; they are refused.
