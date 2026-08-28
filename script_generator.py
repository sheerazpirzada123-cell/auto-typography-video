import os
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_script():
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        "Give me 1 trending interesting fact in simple English or Hinglish for a short reel. "
        "STRICT LIMIT: Maximum 250 characters long."
    )
    response = model.generate_content(prompt)
    return response.text.strip()[:280]

def generate_audio(text):
    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = "21m00Tcm4TlvDq8ikWAM" # Free voice ID
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
    with open("voice.mp3", "wb") as f:
        f.write(res.content)

if __name__ == "__main__":
    text = get_script()
    generate_audio(text)
