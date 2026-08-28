import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["MARVEL", "ANIME", "DC_COMICS", "SCI_FI_FACTS", "POP_CULTURE"]
        chosen_category = random.choice(categories)
        
        angles = [
            "crazy dark secret theory",
            "hidden power that nobody noticed",
            "mind blowing fact that was deleted",
            "most overpowered moment explained",
            "shocking backstory detail"
        ]
        chosen_angle = random.choice(angles)

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Generate a completely new, unique, viral short reel script about a {chosen_angle} in {chosen_category}. "
            "Write strictly in Roman Hinglish using ONLY standard A-Z English alphabets. "
            "STRICT RULES:\n"
            "1. Length: Exactly 30 to 40 words (around 18-20 seconds spoken).\n"
            "2. Do NOT use Urdu, Hindi, or Arabic characters.\n"
            "3. Do NOT repeat previous facts about Iron Man Celestial armor or Thor.\n"
            "4. Start with a catchy hook line.\n"
            "5. End with a strong call to action like 'Follow for more!' or 'Abhi subscribe karo!'"
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.98,
                top_p=0.95
            )
        )
        text = response.text.strip()
        print(f"New Random Script Generated ({chosen_category}):\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        fallback_scripts = [
            "Kya aapko pata hai ki Thor ka hammer Mjolnir kitna heavy hai? Isse sirf wahi utha sakta hai jo truly worthy ho! Aise aur facts ke liye follow kar lo!",
            "Goku ki strength ka real secret kya hai? DBZ mein uski infinite transformation energy sabko shock kar deti hai! Channel ko abhi follow karo!",
            "Batman ke paas Superman ko harane ka secret plan hamesha ready hota hai! DC comics ka yeh secret sabhi ko nahi pata! Aise facts ke liye follow kar lo!"
        ]
        return random.choice(fallback_scripts)

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    voice_id = "nPczCjzI2devNBz1zbdH" 
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Generating Bunty Voice with Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.15,
                "similarity_boost": 0.85,
                "style": 0.65,
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
