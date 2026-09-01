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

    if not os.path.exists("script.txt"):
        raise FileNotFoundError("script.txt missing!")

    with open("script.txt", "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    # Bunty Style Natural Male Voice
    VOICE_ID = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    payload = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.40,
            "similarity_boost": 0.75,
            "style": 0.45,
            "use_speaker_boost": True
        }
    }

    success = False
    for idx, key in enumerate(api_keys):
        headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": key}
        res = requests.post(url, json=payload, headers=headers)
        if res.status_code == 200:
            with open("audio.mp3", "wb") as f:
                f.write(res.content)
            success = True
            print("Voiceover generated successfully!")
            break

    if not success:
        raise RuntimeError("ElevenLabs keys failed!")

def build_custom_typography_video():
    with open("script.txt", "r", encoding="utf-8") as f:
        full_text = f.read().strip()

    voice_audio = AudioFileClip("audio.mp3")
    duration = voice_audio.duration

    # Dark background canvas (1080x1920 Vertial Shorts Format)
    bg_clip = ColorClip(size=(1080, 1920), color=(15, 15, 15)).set_duration(duration)

    # Split text into chunks for dynamic word-by-word typography
    words = full_text.split()
    chunk_size = 4
    text_chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    
    chunk_duration = duration / max(len(text_chunks), 1)
    text_clips = []

    for idx, chunk in enumerate(text_chunks):
        start_t = idx * chunk_duration
        
        # Yellow and White Animated Typography Box
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

    # Audio Mix with Background Music
    audio_tracks = [voice_audio]
    if os.path.exists("bg_music.mp3"):
        bg_music = AudioFileClip("bg_music.mp3").fx(volumex, 0.15).set_duration(duration)
        audio_tracks.append(bg_music)

    final_audio = CompositeAudioClip(audio_tracks)
    final_video = CompositeVideoClip([bg_clip] + text_clips).set_audio(final_audio)

    # Render Output
    final_video.write_videofile(
        "final_output.mp4",
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast"
    )
    print("Video Render Complete with MoviePy Typography & BG Music!")

if __name__ == "__main__":
    generate_voiceover()
    build_custom_typography_video()
