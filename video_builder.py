import os
import requests
from moviepy.editor import (
    ColorClip, TextClip, AudioFileClip, 
    CompositeVideoClip, CompositeAudioClip
)
from moviepy.audio.fx.all import volumex

def generate_voiceover():
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2"),
        os.environ.get("ELEVENLABS_API_KEY_3")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found in secrets!")

    if not os.path.exists("script.txt"):
        raise FileNotFoundError("script.txt missing! Make sure script_generator.py ran first.")

    with open("script.txt", "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    # Voice ID is read from a secret so you can swap voices without touching code.
    # How to pick one that actually matches an energetic Hinglish narrator:
    #   1. Log into elevenlabs.io -> Voice Library
    #   2. Search "Hindi" or "Hinglish" and filter by "Narrative & Story" / "Social Media"
    #   3. Preview a few, pick one, click "Use voice" to add it to your account
    #   4. Open it in "My Voices" -> copy the Voice ID
    #   5. Set it as the ELEVENLABS_VOICE_ID repo secret
    # (Adam's ID below is only a safe default fallback, it is a generic English
    # voice and is the reason the narration currently sounds flat/AI-ish.)
    VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    payload = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            # Lower stability + higher style = more natural pitch/pace variation
            # instead of the flat, over-smoothed "AI narrator" sound.
            "stability": 0.32,
            "similarity_boost": 0.8,
            "style": 0.65,
            "use_speaker_boost": True
        }
    }

    success = False
    for idx, key in enumerate(api_keys):
        headers = {
            "Accept": "audio/mpeg", 
            "Content-Type": "application/json", 
            "xi-api-key": key
        }
        print(f"Trying ElevenLabs Key #{idx + 1}...")
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            with open("audio.mp3", "wb") as f:
                f.write(res.content)
            success = True
            print("Voiceover generated successfully!")
            break
        else:
            print(f"Key #{idx + 1} failed with status {res.status_code}.")

    if not success:
        raise RuntimeError("All ElevenLabs API keys exhausted/failed!")

def build_video():
    if not os.path.exists("script.txt") or not os.path.exists("audio.mp3"):
        raise FileNotFoundError("Required script or audio files missing for video building!")

    with open("script.txt", "r", encoding="utf-8") as f:
        full_text = f.read().strip()

    voice_audio = AudioFileClip("audio.mp3")
    duration = voice_audio.duration

    # Vertical 1080x1920 background canvas
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 15)).set_duration(duration)

    # Word-by-word dynamic typography box chunks
    words = full_text.split()
    chunk_size = 4
    text_chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    chunk_duration = duration / max(len(text_chunks), 1)
    text_clips = []

    for idx, chunk in enumerate(text_chunks):
        start_t = idx * chunk_duration
        
        txt = TextClip(
            chunk.upper(),
            fontsize=65,
            color='yellow',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=3,
            method='caption',
            size=(900, None)
        ).set_start(start_t).set_duration(chunk_duration).set_position(('center', 'center'))

        text_clips.append(txt)

    # Audio Mixing with optional Background Music
    audio_tracks = [voice_audio]
    if os.path.exists("bg_music.mp3"):
        bg_music = AudioFileClip("bg_music.mp3").fx(volumex, 0.15).set_duration(duration)
        audio_tracks.append(bg_music)

    final_audio = CompositeAudioClip(audio_tracks)
    final_video = CompositeVideoClip([bg_clip] + text_clips).set_audio(final_audio)

    # Render final output file
    final_video.write_videofile(
        "final_output.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast"
    )
    print("Video Render Complete: final_output.mp4 generated successfully!")

if __name__ == "__main__":
    generate_voiceover()
    build_video()
