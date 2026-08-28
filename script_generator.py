import os
import random
import requests
import google.generativeai as genai

# Setup Gemini API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["Technology", "Space & Science", "Human Psychology", "World History", "Bizarre Facts"]
        selected_category = random.choice(categories)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 40-50 Seconds ki video ke liye length adjust kar di gayi hai (approx 500-600 characters)
        prompt = (
            f"Write a 40 to 50 seconds engaging short script about an interesting fact in {selected_category} in natural Hinglish. "
            "Write around 550 to 650 characters. Do NOT use fancy words. Make it sound like a human talking to a friend naturally for a viral reel."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.85,
                top_p=0.9
            )
        )
        text = response.text.strip()
        print(f"Generated Script:\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Kya aap jante hain ki space bilkul silent hai? Space mein sound waves ko travel karne ke liye koi atmosphere nahi hota, isliye wahan chahe kitna bhi bada blast ho jaye, aapko koi aawaz sunai nahi degi!"

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found in repository secrets!")

    # Deep Natural Male Voice ID (Adam)
    voice_id = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Trying ElevenLabs Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        # Stability aur Similarity boost settings change ki hain AI-robot voice effect hatane ke liye
        data = {
            "text": text,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {
                "stability": 0.55, 
                "similarity_boost": 0.75,
                "style": 0.20,
                "use_speaker_boost": True
            }
        }
        
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)
            print(f"voice.mp3 generated successfully with Key #{idx + 1}!")
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
