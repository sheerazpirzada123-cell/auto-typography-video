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
        script_text = f.read()

    # Energetic Male Voice ID
    VOICE_ID = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    payload = {
        "text": script_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.35,        # Low stability = Energetic & Pitch-varied human expression
            "similarity_boost": 0.80,
            "style": 0.50,            # High expressiveness
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

def build_video_with_typography():
    # Audio duration ke according background generate aur typography render karna
    # Multiline wrap + Yellow-White Typography style overlay
    cmd = (
        'ffmpeg -y -f lavfi -i color=c=black:s=1080x1920 '
        '-i audio.mp3 '
        '-vf "drawtext=textfile=script.txt:fontcolor=white:fontsize=42:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=20:box=1:boxcolor=black@0.6:boxborderw=15" '
        '-c:v libx264 -preset ultrafast -c:a aac -shortest final_output.mp4'
    )
    subprocess.run(cmd, shell=True, check=True)
    print("Video Render Complete: final_output.mp4 generated.")

if __name__ == "__main__":
    generate_voiceover()
    build_video_with_typography()
