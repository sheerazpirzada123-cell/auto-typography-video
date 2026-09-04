# auto-typography-video

Daily automated Hinglish "fact/theory" YouTube Shorts: **Gemini** writes the script → **ElevenLabs** voices it → **MoviePy** builds a word-by-word typography video → **YouTube API** uploads it. Runs on GitHub Actions, 2 videos/day.

## 1. Add these Repo Secrets
`Settings → Secrets and variables → Actions → New repository secret`

| Secret | Where to get it |
|---|---|
| `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| `ELEVENLABS_API_KEY` | ElevenLabs account #1 → Profile → API Keys |
| `ELEVENLABS_API_KEY_2` | ElevenLabs account #2 (for extra monthly quota) |
| `ELEVENLABS_API_KEY_3` | ElevenLabs account #3 (for extra monthly quota) |
| `ELEVENLABS_VOICE_ID` | See "Picking a voice" below |
| `YOUTUBE_CLIENT_ID` | Google Cloud Console → OAuth Client (Desktop app) |
| `YOUTUBE_CLIENT_SECRET` | Same OAuth Client |
| `YOUTUBE_REFRESH_TOKEN` | Generated once via OAuth consent flow for your channel |

The script automatically tries key #1, then #2, then #3 if one runs out of monthly ElevenLabs credits — so 3 free/starter ElevenLabs accounts should comfortably cover 2 shorts/day.

## 2. Picking a voice that doesn't sound "AI"
1. Log into elevenlabs.io → **Voice Library**
2. Search "Hindi" / "Hinglish", filter by Narrative or Social Media voices
3. Preview a few, click **Use voice** to add it to your account
4. Open it under **My Voices** → copy the **Voice ID**
5. Save it as the `ELEVENLABS_VOICE_ID` secret

Without this secret it falls back to a generic English voice, which is why it can sound flat/robotic. `stability`/`style` in `video_builder.py` are already tuned lower/higher than default for a more natural, less monotone read — adjust further once you've picked your voice.

## 3. Schedule
Currently runs at `08:00` and `16:00` UTC (≈ 1 PM and 9 PM PKT) — 2 videos/day. Edit the `cron` line in `.github/workflows/generate_video.yml` to change times. You can also trigger a manual run anytime from the **Actions** tab → **Run workflow**.

## 4. Files
- `script_generator.py` — Gemini writes a 50-60 word Hinglish fact/theory script (`script.txt`)
- `video_builder.py` — ElevenLabs TTS (`audio.mp3`) + MoviePy renders the vertical 1080x1920 typography video (`final_output.mp4`)
- `uploader.py` — uploads `final_output.mp4` to your YouTube channel as a public Short
