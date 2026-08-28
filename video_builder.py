import os
import random
import requests
import google.generativeai as genai

# Setup Gemini API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        # Har run par random category choose hogi
        categories = ["Technology", "Space & Science", "Human Psychology", "World History", "Bizarre Facts", "Life Hacks"]
        selected_category = random.choice(categories)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Give me 1 extremely shocking, rare, and interesting short fact about {selected_category} in simple Hinglish for a viral short reel. "
            "STRICT LIMIT: Maximum 200 characters long. Punchy typography style script."
        )
        
        # temperature=0.9 se har baar bilkul unique output milega
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95
            )
        )
        
        text = response.text.strip()
        print(f"Category: {selected_category}")
        print(f"Generated Script: {text}")
        return text[:250]
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Random fallbacks agar API fail ho jaye
        fallbacks = [
            "Did you know? Honey never spoils! Archeologists found 3000 year old edible honey.",
            "Bananas are naturally radioactive because of potassium! Crazy right?",
            "Octopuses have three hearts and blue blood! Mind blown!"
        ]
        return random.choice(fallbacks)

def generate_audio(text):
    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.7}
    }
    
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        with open("voice.mp3", "wb") as f:
            f.write(res.content)
        print("Audio saved successfully.")
    else:
        print(f"ElevenLabs API Error: {res.status_code} - {res.text}")

if __name__ == "__main__":
    text = get_script()
    generate_audio(text)
