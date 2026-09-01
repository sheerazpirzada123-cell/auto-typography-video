import os
import google.generativeai as genai

# Setup Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing!")

genai.configure(api_key=api_key)

def generate_script():
    # Prompting for human-like conversational Hinglish script with natural pauses and full facts
    prompt = """
    Write a short, viral YouTube Shorts script (around 40-50 words) in Indian Hinglish (Hindi written in Roman script).
    
    TONE & STYLE (HUMAN BUNTY ACCENT):
    - Speak like a young, energetic Indian guy (Bunty style) talking directly to a friend.
    - Use natural human expressions like 'hmm...', 'Waise...', 'Arrey listen...', 'Pata hai?', 'Acha ek baat batao...'.
    - Use natural punctuation (commas, ellipsis '...') so the text-to-speech voice takes realistic human pauses.

    CONTENT REQUIREMENTS:
    1. Start with a quick, punchy hook using Bunty-style slang.
    2. Tell ONE complete, genuine mind-blowing fact clearly. Do NOT leave the fact out!
    3. End with a smooth call-to-action (e.g., "Abhi subscribe karo, milte hain next video mein!").
    4. NO brackets, NO scene instructions, NO speaker names. Output ONLY the raw spoken lines.
    """

    # Updated Model Name to gemini-3.6-flash
    model = genai.GenerativeModel("gemini-3.6-flash")
    response = model.generate_content(prompt)
    
    script_text = response.text.strip()
    
    # Save script to text file
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)
        
    print("--- New Bunty-Style Script Generated ---")
    print(script_text)
    print("---------------------------------------")

if __name__ == "__main__":
    generate_script()
