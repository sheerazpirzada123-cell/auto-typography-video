import os
import random
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        topics = [
            "Mind-Blowing Human Psychology Facts",
            "Bizarre Historical Events That Actually Happened",
            "Unbelievable Space and Universe Facts",
            "Dark Secrets of Modern Technology",
            "Deep Ocean Mysteries",
            "Insane Science Facts"
        ]
        chosen_topic = random.choice(topics)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Fixed 30-40 seconds script character length (approx 550-700 characters)
        prompt = (
            f"Write a completely unique, highly engaging short story or viral factual script about '{chosen_topic}' strictly in Roman Hinglish "
            "(e.g. 'Kya aapko pata hai', 'Lekin sach ye hai', 'Waise toh ye baat'). "
            "IMPORTANT: Script MUST be between 550 to 700 characters so that audio lasts around 30 to 40 seconds. "
            "Do NOT output Hindi Devanagari script, English-only text, or any intro metadata."
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
            "Kya aapko pata hai ki hamare dimaag ke paas itni memory space hoti hai "
            "ki wo internet ki saari information ko aasani se store kar sakta hai? "
            "Lekin hum fir bhi apni day-to-day life mein chhote chhote kaam bhool jaate hain. "
            "Scientific research ke mutabiq hamara brain sirf unhi chizon ko yaad rakhta hai "
            "jo hamare emotional state se connected hoti hain. Isliye agli baar koi baat yaad rakhni ho "
            "toh usse kisi interesting feeling ke saath connect karna mat bhoolna!"
        )

def generate_audio(text):
    api_keys = [
        os.environ.get("ELEVENLABS_API_KEY"),
        os.environ.get("ELEVENLABS_API_KEY_2")
    ]
    api_keys = [k for k in api_keys if k]

    if not api_keys:
        raise ValueError("No ElevenLabs API keys found in repository secrets!")

    # Gojo / Anime Narration Viral Voice ID
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
                "stability": 0.45, 
                "similarity_boost": 0.80,
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
        else:
            print(f"Key #{idx + 1} failed: {res.status_code}")

    if not success:
        raise Exception("All ElevenLabs API keys failed!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
