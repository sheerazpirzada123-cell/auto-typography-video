import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        topics = [
            "Mind-Blowing Marvel MCU Secrets",
            "Dark Anime Secrets That Nobody Noticed",
            "Goku vs Saitama Real Power Levels",
            "Death Note Unknown Facts",
            "Iron Man Hidden Armor Abilities"
        ]
        chosen_topic = random.choice(topics)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a viral short reel script about '{chosen_topic}' strictly in Roman Hinglish "
            "(e.g. 'Kya aapko pata hai', 'Lekin sach ye hai', 'Waise toh ye baat'). "
            "Write exactly around 600 characters so voiceover duration stays strictly 30-40 seconds. "
            "STRICT RULES: Do NOT output English translations, only write speech phonetically in Roman Hinglish."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.9
            )
        )
        text = response.text.strip()
        print(f"Generated Script Topic ({chosen_topic}):\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return (
            "Kya aapko pata hai ki Marvel comics mein Iron Man ka armor itna powerful hai "
            "ki wo Celestial powers ko bhi absorb kar sakta hai? Lekin MCU movies mein is detail ko "
            "kabhi dikhaya hi nahi gaya! Waise hi Anime ki duniya mein Goku ki stamina "
            "ke peeche ek aisa secret hai jo aadhe fans ko pata hi nahi. Agar aap bhi Anime aur Marvel "
            "ke aise crazy details janna chahte ho, toh abhi follow kar lo!"
        )

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

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
                "stability": 0.55, 
                "similarity_boost": 0.75,
                "style": 0.18,
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
