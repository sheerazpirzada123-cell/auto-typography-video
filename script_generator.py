import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["Tech Facts", "Dark Psychology", "Anime Trivia", "Life Hacks", "Bizarre Facts"]
        selected_category = random.choice(categories)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a 1-minute engaging short video script about {selected_category} in casual Hinglish. "
            "Write around 500 to 700 characters long. Use punchy viral style storytelling."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.9, top_p=0.95)
        )
        text = response.text.strip()
        print(f"Generated Script:\n{text}")
        return text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Kya aap jante hain ki space bilkul silent hai kyunki wahan sound waves move nahi kar sakti!"

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    # Gojo/Anime Male Voice ID (Adam / Antony Voice)
    voice_id = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Generating audio with ElevenLabs Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        data = {
            "text": text,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {"stability": 0.35, "similarity_boost": 0.85}
        }
        
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)
            print("voice.mp3 created successfully!")
            success = True
            break
        else:
            print(f"Key #{idx + 1} failed: {res.status_code}")

    if not success:
        raise Exception("All ElevenLabs API keys failed!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
