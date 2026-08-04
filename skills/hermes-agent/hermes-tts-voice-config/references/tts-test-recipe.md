# TTS Voice Test Recipe

Use this to verify a voice change actually took effect and to let the user
pick a female voice. The agent CANNOT hear audio — always hand the user the
files to judge.

## 1. Set the voice (correct key)
```
hermes config set tts.openai.voice shimmer --force
hermes config set tts.openai.model gpt-4o-mini-tts --force
```

## 2. Verify the key landed under tts:
```
hermes config get tts
# Look for:
#   openai:
#     model: gpt-4o-mini-tts
#     voice: shimmer
# (must be nested under tts:, NOT a top-level tts.voice or openai: block)
```

## 3. Generate one MP3 per candidate voice
Call text_to_speech once per voice, Arabic test phrase:
"أهلاً يا حاتم بيك، أنا دينا. هذا اختبار لصوت ست."
```
text_to_speech voice=shimmer  -> audio_cache/test_shimmer.mp3
text_to_speech voice=alloy    -> audio_cache/test_alloy.mp3
text_to_speech voice=fable    -> audio_cache/test_fable.mp3
text_to_speech voice=nova     -> audio_cache/test_nova.mp3
```

## 4. Send the files to the user (MEDIA: path) and ask which sounds female.
Do NOT assume — the user's environment determined that `nova` AND `shimmer`
AND `alloy` AND `fable` all sounded male on first attempts, which turned out
to be because the voice key was wrong (default alloy), not because the voice
names were male. Fix the KEY first, then test.
