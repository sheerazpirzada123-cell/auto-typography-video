import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        marvel_topics = [
            "Iron Man Hidden Armor Ability in Marvel Comics",
            "Why Thor's Hammer Mjolnir Is Way Overpowered",
            "Thanos Real Secret Motivation That Was Hidden",
            "Doctor Strange Unknown Time Manipulation Trick"
        ]
        anime_topics = [
            "Goku Infinite Stamina Real Secret in Dragon Ball",
            "Saitama One Punch Man Unknown Origin Fact",
            "Death Note Rule That Nobody Ever Noticed",
            "Naruto Kyuubi Chakra Hidden Secret"
        ]
        
        category = random.choice(["MARVEL", "ANIME"])
        if category == "MARVEL":
            chosen_topic = random.choice(marvel_topics)
            prompt_context = "This video is STRICTLY about Marvel MCU / Comics only. Do NOT mention Anime."
        else:
            chosen_topic = random.choice(anime_topics)
            prompt_context = "This video is STRICTLY about Anime only. Do NOT mention Marvel or Avengers."

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write an energetic viral short reel script about '{chosen_topic}' strictly in Roman Hinglish. "
            f"{prompt_context} "
            "Write exactly around 400-450 characters so voiceover duration stays strictly 20-25 seconds. "
            "STRICT RULES: Do NOT output English translations. Write speech phonetically in Roman Hinglish."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                top_p=0.9
            )
        )
        text = response.text.strip()
        print(f"Generated Script Category ({category}) - Topic ({chosen_topic}):\n{text}")
        
        with open("category.txt", "w", encoding="utf-8") as f:
            f.write(category)
            
        return text
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        with open("category.txt", "w", encoding="utf-8") as f:
            f.write("MARVEL")
        return (
            "Kya aapko pata hai ki Marvel comics mein Iron Man ka armor itna powerful hai "
            "ki wo Celestial powers ko bhi absorb kar sakta hai? Lekin MCU movies mein is detail ko "
            "kabhi dikhaya hi nahi gaya! Agar aap bhi Marvel ke aise crazy details janna chahte ho, "
            "toh abhi follow kar lo!"
        )

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    voice_id = "21m00Tcm4TlvDq8ikWAM" # High-energy engaging voice (Rachel)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Generating Natural Human Voice with Key #{idx + 1}...")
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.40,
                "similarity_boost": 0.80,
                "style": 0.25,
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
