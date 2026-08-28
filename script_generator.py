import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        # Anime aur Marvel dedicated topics
        topics = [
            "Mind-Blowing Marvel Cinematic Universe Facts",
            "Dark and Unknown Anime Lore Secrets",
            "Iron Man vs Batman Hidden Comic Facts",
            "Goku vs Saitama Power Scalings",
            "Unbelievable Secrets About Naruto and Sasuke",
            "Marvel Multiverse Theories That Will Blow Your Mind",
            "Death Note Psychological Hidden Details"
        ]
        chosen_topic = random.choice(topics)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Audio duration strictly 30-40 sec (550 to 700 chars)
        prompt = (
            f"Write a viral, highly engaging script about '{chosen_topic}' strictly in Roman Hinglish "
            "(e.g. 'Kya aapko pata hai', 'Lekin sach ye hai', 'Waise toh ye baat'). "
            "The tone must be energetic, enthusiastic, and confident like a famous anime/marvel content creator. "
            "IMPORTANT: Script MUST be between 550 to 700 characters long so the voiceover stays strictly 30-40 seconds. "
            "Do NOT output Hindi Devanagari text, English-only text, or metadata."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.95,
                top_p=0.95
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
            "kabhi dikhaya hi nahi gaya! Waise hi Anime ki duniya mein Goku ki Infinite stamina "
            "ke peeche ek aisa secret hai jo aadhe fans ko pata hi nahi. Agar aap bhi Anime aur Marvel "
            "ke aise crazy theories janna chahte ho, toh abhi follow kar lo taaki koi episode miss na ho!"
        )

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found!")

    # Deep, confident storytelling voice ID
    voice_id = "pNInz6obpgDQGcFmaJgB"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    success = False
    for idx, key in enumerate(api_keys):
        print(f"Generating ElevenLabs Voice Over with Key #{idx + 1}...")
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
        else:
            print(f"Key #{idx + 1} failed: {res.status_code}")

    if not success:
        raise Exception("All ElevenLabs API keys failed!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
