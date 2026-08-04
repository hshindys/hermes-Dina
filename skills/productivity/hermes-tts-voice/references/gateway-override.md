# Gateway Voice Override — source-level diagnostic

Verified during a 2026-08 session where a user's `tts.voice: shimmer`
set via `hermes config set tts.voice shimmer` had no effect (voice still
sounded male). Root cause found by reading the bundled Hermes source.

## Where the voice is actually read
File: `~/.hermes/hermes-agent/tools/tts_tool.py`

```python
# _generate_openai_tts(...)
oai_config = (tts_config.get("openai") if isinstance(tts_config, dict) else None) or {}
if voice is None:
    voice = oai_config.get("voice", DEFAULT_OPENAI_VOICE)   # DEFAULT_OPENAI_VOICE = "alloy"
```

So the resolver looks at `tts.openai.voice`, falling back to `"alloy"`.
A top-level `tts.voice` key is NOT consulted here.

## The managed-gateway model coercion
```python
if (
    is_managed
    and not explicit_base_url
    and not config_base_url
    and model not in MANAGED_OPENAI_TTS_MODELS
):
    model = DEFAULT_OPENAI_MODEL
```
`MANAGED_OPENAI_TTS_MODELS = frozenset({"gpt-4o-mini-tts"})`.
`is_managed` is True when credentials came from the managed Nous portal
(`_resolve_openai_audio_client_config`), i.e. no direct OpenAI key.

The same managed proxy that coerces the model may also ignore/override
the voice — observed symptom: every voice id (nova, shimmer, alloy,
fable) produced an identical male voice.

## How to confirm which path you're on
```bash
# 1. what voice is configured
hermes config get tts.openai.voice

# 2. what auth is active
python -c "import json,glob; \
  p=glob.glob(r'C:/Users/hshin/AppData/Local/hermes/auth.json')[0]; \
  print(json.load(open(p))['active_provider'])"

# 3. is use_gateway on?
hermes config get tts.use_gateway

# 4. any direct OpenAI key?
grep -i "VOICE_TOOLS_OPENAI_KEY\|OPENAI_API_KEY" ~/.hermes/.env | grep -v '^#'
```

If (2)=="nous" and (4) empty and (3)=="true" → you are on the managed
gateway and the voice override is expected to be ignored. Fix options:
provide `VOICE_TOOLS_OPENAI_KEY` + set `tts.use_gateway: false`, or switch
provider to `edge` (free, supports Arabic female neural voices) or
`elevenlabs`.
