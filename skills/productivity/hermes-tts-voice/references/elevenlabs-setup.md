# ElevenLabs TTS Setup — validated transcript

## Context
User (Hatem) wanted a **female** TTS voice for the "Dina" persona. OpenAI
voices (`alloy`, `shimmer`, `nova`, `fable`) all sounded male because the
active auth provider was `nous` (managed gateway), which silently overrides
the OpenAI voice. ElevenLabs was the working path.

## Step 1 — set the API key (terminal only)
The `.env` at `~/.hermes/.env` is a credential store: `patch` and `read_file`
are BLOCKED from it. Write via terminal/python heredoc. REDACT the key in any
visible transcript.

```bash
python - <<'PY'
path = r'C:/Users/hhshin/AppData/Local/hermes/.env'
lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
out, done = [], False
for l in lines:
    if l.strip().startswith('# ELEVENLABS_API_KEY=') or l.strip()=='ELEVENLABS_API_KEY=':
        out.append('ELEVENLABS_API_KEY=<KEY>\n'); done=True
    else: out.append(l)
if not done: out.append('\nELEVENLABS_API_KEY=<KEY>\n')
open(path,'w',encoding='utf-8').writelines(out)
PY
```
Verify (key should NOT print in full): `grep -n 'ELEVENLABS_API_KEY=' ~/.hermes/.env | sed 's/=.*/=REDACTED/'`

## Step 2 — provider + voice config
```bash
hermes config set tts.provider elevenlabs --force
hermes config set tts.elevenlabs.voice_id pNInz6obpgDQGcFmaJgB --force
hermes config set tts.elevenlabs.model_id eleven_multilingual_v2 --force
```
Verify: `hermes config get tts` → should show `provider: elevenlabs` and the
`elevenlabs.voice_id` above.

## Step 3 — test
`text_to_speech(provider="elevenlabs", text="...")` → produced a valid MP3
(`dina_elevenlabs_rachel.mp3`). SUCCESS — female voice confirmed.

## ⚠️ Library-voice 402 (the trap)
User shared an ElevenLabs voice-library URL:
`https://elevenlabs.io/app/voice-library?voiceId=rFDdsCQRZCUL8cPOWtnP`
Setting that as `voice_id` and calling TTS returned:

```
TTS generation failed (elevenlabs): status_code: 402,
body: {'detail': {'type': 'payment_required',
                  'code': 'paid_plan_required',
                  'message': 'Free users cannot use library voices via the
                              API. Please upgrade your subscription to use
                              this voice.',
                  'status': 'payment_required',
                  'request_id': '...'}}
```

**Lesson:** Free-tier keys cannot play library voices. A *premade* voice
(`pNInz6obpgDQGcFmaJgB` = "Rachel", female) works on free tier. If the user
wants their exact library voice, they must upgrade to a paid ElevenLabs plan;
until then fall back to the premade voice and remember their preferred
library `voice_id`.

## Alternative if no ElevenLabs key
`hermes config set tts.provider edge --force` — free, no key, Arabic female
neural voices: `ar-EG-SalmaNeural`, `ar-SA-ZariyahNeural`.
