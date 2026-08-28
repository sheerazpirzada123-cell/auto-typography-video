import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["Technology", "Space & Science", "Human Psychology", "World History", "Bizarre Facts"]
        selected_category = random.choice(categories)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a 40 to 50 seconds video script about an interesting fact in {selected_category} strictly in natural Roman Hinglish (like 'Kya aapko pata hai', 'Lekin sach ye hai'). "
            "STRICT RULES: Do NOT use Hindi/Devanagari script, and do NOT use formal Urdu/English words. Keep it around 550-650 characters."
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
        return "Kya aapko pata hai ki space bilkul silent hota hai? Sound waves ko travel karne ke liye hawa chahiye hoti hai jo space mein nahi hoti. Isliye wahan chahe kitna bhi bada blast ho jaye, aapko koi aawaz sunai nahi degi!"

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    # Deep Natural Male Voice
    voice_id = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Generating Audio with Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.50, 
                "similarity_boost": 0.75,
                "style": 0.20,
                "use_speaker_boost": True
            }
        }
        
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)
            print("voice.mp3 generated successfully!")
            success = True
            break

    if not success:
        raise Exception("All ElevenLabs API keys failed!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
