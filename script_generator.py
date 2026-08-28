import os
import requests
import google.generativeai as genai

# Setup Gemini API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    try:
        # gemini-1.5-flash standard model name hai
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "Give me 1 trending interesting short fact in Hinglish for a short reel. "
            "STRICT LIMIT: Maximum 200 characters long. Punchy script."
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        print(f"Generated Text: {text}")
        return text[:250]
    except Exception as e:
        print(f"Gemini API Error: {e}")
        # Fallback text in case API fails
        return "Did you know that Honey never spoils? Archeologists found 3000 year old edible honey!"

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
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
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
