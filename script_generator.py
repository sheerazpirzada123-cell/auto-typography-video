import os
import random
import requests
import google.generativeai as genai

# Setup Gemini API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["Technology", "Space & Science", "Human Psychology", "World History", "Bizarre Facts", "Life Hacks"]
        selected_category = random.choice(categories)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a 45 to 60 seconds engaging short story/fact script about {selected_category} in simple Hinglish (Hindi written in Roman script) for a viral reel. "
            "Write around 500 to 700 characters long. Make it extremely exciting with punchy typography lines."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95
            )
        )
        
        text = response.text.strip()
        print(f"Category: {selected_category}")
        print(f"Generated Script:\n{text}")
        return text
        
    except Exception as e:
        print(f"Gemini API Exception (using fallback): {e}")
        fallbacks = [
            "Kya aap jante hain ki Honey kabhi kharab nahi hota? Archeologists ko 3000 saal purana khane layak honey mila tha! Iska main reason hai iska low moisture aur natural acidity.",
            "Bananas naturally radioactive hote hain kyunki unme Potassium-40 hota hai! Lekin ghabrao mat, aapko harm pahunchane ke liye 1 crore bananas ek saath khane padenge!"
        ]
        return random.choice(fallbacks)

def generate_audio(text):
    # Multiple ElevenLabs Keys Backup List
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    # Filter out empty keys
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found in repository secrets!")

    # Free Tier supported default Voice ID (George)
    voice_id = "JBFqnCBsd6RMkjVDRZzb"
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
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {"stability": 0.4, "similarity_boost": 0.7}
        }
        
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with open("voice.mp3", "wb") as f:
                f.write(res.content)
            print(f"voice.mp3 successfully generated using API Key #{idx + 1}!")
            success = True
            break
        else:
            print(f"Key #{idx + 1} failed or limit exhausted: {res.status_code} - {res.text}")

    if not success:
        raise Exception("All ElevenLabs API keys failed or ran out of character limits!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
