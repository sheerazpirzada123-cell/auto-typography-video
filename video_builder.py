import os
import requests
import subprocess

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
            break

    if not success:
        raise RuntimeError("ElevenLabs API keys failed!")

def build_original_aesthetic_video():
    # Dynamic Box Styling + Soft Aesthetic Background Filter (Exact Original Look)
    ffmpeg_cmd = (
        'ffmpeg -y -f lavfi -i color=c=0xF0F4F1:s=1080x1920 '
        '-i audio.mp3 '
        '-vf "drawtext=textfile=script.txt:fontcolor=0x2E1A47:fontsize=52:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20:box=1:boxcolor=0xF4ECC2@0.85:boxborderw=18" '
        '-c:v libx264 -preset ultrafast -c:a aac -shortest final_output.mp4'
    )
    subprocess.run(ffmpeg_cmd, shell=True, check=True)
    print("Video Render Complete with Original Aesthetic Look!")

if __name__ == "__main__":
    generate_voiceover()
    build_original_aesthetic_video()
