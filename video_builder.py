import os
import requests

def generate_voiceover():
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2"),
        os.environ.get("ELEVENLABS_API_KEY_3")
    ]
    api_keys = [key for key in api_keys if key]
    
    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    if not os.path.exists("script.txt"):
        raise FileNotFoundError("script.txt not found. script_generator.py execute hona zaroori hai.")
        
    with open("script.txt", "r", encoding="utf-8") as f:
        script_text = f.read()

    # Energetic Bunty Voice ID
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
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        
        print(f"ElevenLabs Key #{idx + 1} try kar rahe hain...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            with open("audio.mp3", "wb") as f:
                f.write(response.content)
            print("Voiceover generated successfully!")
            success = True
            break
        else:
            print(f"Key #{idx + 1} fail hui (Status {response.status_code}). Next key try ho rahi hai...")

    if not success:
        raise RuntimeError("ElevenLabs API keys exhaust ho chuki hain.")

def build_dummy_video():
    # File check / Dummy generator to ensure final_output.mp4 is created
    # Replace this block with your MoviePy/FFmpeg rendering pipeline if customized
    os.system("ffmpeg -y -f lavfi -i color=c=black:s=1080x1920:d=10 -i audio.mp3 -c:v libx264 -c:a aac -shortest final_output.mp4")

if __name__ == "__main__":
    generate_voiceover()
    build_dummy_video()
