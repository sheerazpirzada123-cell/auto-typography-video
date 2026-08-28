import os
import random
import google.generativeai as genai
from gtts import gTTS

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        categories = ["Technology", "Space & Science", "Human Psychology", "World History", "Bizarre Facts"]
        selected_category = random.choice(categories)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            f"Write a 1-minute deep-explain interesting fact script about {selected_category} in simple Hinglish (Hindi written in Roman English Script). "
            "Make it sound very engaging for a YouTube Short / Instagram Reel. Write around 600-800 characters long script."
        )
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                top_p=0.95
            )
        )
        text = response.text.strip()
        print(f"Generated Script:\n{text}")
        return text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Kya aap jante hain ki space bilkul silent hai kyunki wahan sound wave carry karne ke liye koi atmosphere nahi hota!"

def generate_audio(text):
    # gTTS with Devanagari/Hindi voice pronunciation output
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save("voice.mp3")
    print("voice.mp3 successfully created via gTTS!")

if __name__ == "__main__":
    text = get_script()
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(text)
    generate_audio(text)
