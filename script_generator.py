import os
import google.generativeai as genai

# Setup Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing!")

genai.configure(api_key=api_key)

def generate_script():
    # Prompting for actual factual content
    prompt = """
    Write a short, engaging YouTube Shorts script (maximum 40-50 words) in Hinglish (Hindi written in English alphabets).
    
    STRICT REQUIREMENTS:
    1. Pick ONE specific, interesting, real mind-blowing fact (e.g. space, science, animals, or anime facts).
    2. Start with a catchy 1-line hook.
    3. IMMEDIATELY explain the actual fact clearly in 2-3 sentences. Do not leave the fact blank or incomplete!
    4. End with a 1-line call to action (like "Follow for more!").
    5. Do NOT include scene directions, speaker names, bracketed notes, or timestamps. Output ONLY the spoken text.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    script_text = response.text.strip()
    
    # Save script to text file for moviepy and voiceover generators
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)
        
    print("--- New Script Generated ---")
    print(script_text)
    print("----------------------------")

if __name__ == "__main__":
    generate_script()
