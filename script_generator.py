import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["MARVEL", "ANIME", "DC_COMICS", "POP_CULTURE", "SCI_FI_FACTS"]
        chosen_category = random.choice(categories)

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Human-like speech prompt
        prompt = (
            f"Write an extremely natural, highly energetic short video script about a mind-blowing secret or fact in {chosen_category}.\n\n"
            "CRITICAL STYLE RULES:\n"
            "1. LANGUAGE: Strict Roman Hinglish (English A-Z alphabets ONLY).\n"
            "2. HUMAN ACCENT & FLOW: Write EXACTLY how a regular Indian guy/influencer speaks out loud to a friend. Use natural conversational words like 'arrey', 'bhai', 'yaar', 'sach mein', 'matlab'.\n"
            "3. NO ROBOTIC WORDS: Avoid formal bookish Hindi translated into English. Make it sound like casual daily conversation.\n"
            "4. LENGTH: 30 to 40 words total (around 18 seconds spoken).\n"
            "5. NO SPECIAL SYMBOLS: Strictly no Urdu, Devanagari, or Arabic letters. Plain A-Z only.\n"
            "6. STRUCTURE: Dynamic hook in the beginning, crazy fact in the middle, fast call-to-action at the end."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.98,
                top_p=0.95
            )
        )
        text = response.text.strip()
        print(f"Generated Script ({chosen_category}):\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        fallback_scripts = [
            "Arrey bhai kya aapko pata hai ki Thor ka hammer Mjolnir kitna heavy hai? Matlab isko sirf wahi utha sakta hai jo truly worthy ho! Aise insane facts ke liye abhi follow karo!",
            "Goku ki strength ka real secret pata hai? DBZ mein uski infinite transformation energy dekh kar sab shock ho gaye the! Channel ko abhi follow karo!",
            "Arrey yaar Batman ke paas Superman ko harane ka secret plan hamesha ready rehta hai! DC ka yeh fact sach mein mind blowing hai! Abhi follow kar lo!"
        ]
        return random.choice(fallback_scripts)

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

    # Bunty Voice Profile ID
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
                "stability": 0.25,        # Adjusted for human-like voice modulation
                "similarity_boost": 0.85,
                "style": 0.55,             # Added expressiveness
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
