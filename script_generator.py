import os
import random
import time
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        # Endless Niche & Sub-Genre Generators
        universes = [
            "Marvel Comics", "MCU", "DC Comics", "Dragon Ball Z", "Naruto", 
            "One Piece", "Attack on Titan", "Demon Slayer", "Jujutsu Kaisen",
            "Sci-Fi Movies", "Hollywood Movie Easter Eggs", "Popular Video Games Facts"
        ]
        
        angles = [
            "the most disturbing secret theory",
            "an overpowered hidden ability nobody talks about",
            "a mind-blowing plot hole that changes everything",
            "a deleted scene concept that fans missed",
            "the darkest backstory detail",
            "an insane power comparison fact"
        ]

        # Random Seed & Timestamp to ensure 100% uniqueness on every workflow run
        random_seed = int(time.time() * 1000)
        chosen_universe = random.choice(universes)
        chosen_angle = random.choice(angles)

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Random Seed: {random_seed}\n"
            f"Topic Target: Pick a COMPLETELY UNKNOWN or HIGHLY INTERESTING topic about {chosen_universe}.\n"
            f"Angle: Focus on {chosen_angle}.\n\n"
            "STRICT RULES FOR GENERATION:\n"
            "1. NO REPETITION: Do NOT write about Iron Man's Celestial armor, Thor's hammer weight, Goku's stamina, or Batman's Superman plan. Choose something 100% FRESH.\n"
            "2. LANGUAGE: Write strictly in natural, daily-spoken Roman Hinglish (English A-Z alphabets ONLY).\n"
            "3. HUMAN VOICE & ACCENT: Speak like a real Indian guy/influencer chatting with a friend. Use words like 'arrey', 'bhai', 'yaar', 'sach mein', 'matlab'.\n"
            "4. LENGTH: Strictly 30 to 35 words (approx. 15-18 seconds spoken).\n"
            "5. NO SPECIAL CHARACTERS: Strictly standard A-Z alphabets. No Hindi/Urdu/Arabic script.\n"
            "6. HOOK & CTA: Start with a heavy hook line and end with 'Abhi follow karo!' or 'Follow kar lo!'"
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=1.0,  # Maximum randomness for infinite new ideas
                top_p=0.95
            )
        )
        text = response.text.strip()
        print(f"New Infinite Topic Generated ({chosen_universe}):\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Dynamic fallback pool with timestamp randomness
        fallback_pool = [
            "Arrey bhai kya aapko pata hai ki Spider-Man ka Iron Spider suit kitna deadly hai? Isme aise weapons hain jo kisi ko bhi hila de! Aise facts ke liye follow karo!",
            "Bhai Vegeta ki real backstory pata hai? Dragon Ball mein uski training routine dekh kar Goku bhi shock ho gaya tha! Channel ko abhi follow karo!",
            "Arrey yaar Death Note ka ek aisa rule hai jo 99 percent logo ne notice nahi kiya! Yeh fact sach mein mind blowing hai, abhi follow kar lo!"
        ]
        return random.choice(fallback_pool)

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2"),
        os.environ.get("ELEVENLABS_API_KEY_3"),
        os.environ.get("ELEVENLABS_API_KEY_4")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found in secrets!")

    voice_id = "nPczCjzI2devNBz1zbdH" 
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Trying ElevenLabs API Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.25,
                "similarity_boost": 0.85,
                "style": 0.55,
                "use_speaker_boost": True
            }
        }
        
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)
            print(f"voice.mp3 generated successfully using Key #{idx + 1}!")
            success = True
            break
        else:
            print(f"Key #{idx + 1} failed (Status: {res.status_code}). Trying next key...")

    if not success:
        print("Fallback to secondary voice...")
        fallback_voice_id = "pNInz6obpgDQGcFmaJgB"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{fallback_voice_id}"
        headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": api_keys[0]}
        data["voice_settings"]["stability"] = 0.20
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
