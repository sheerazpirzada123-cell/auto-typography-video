import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing!")

genai.configure(api_key=api_key)

def generate_script():
    prompt = """
    Write a complete, full YouTube Shorts script in Indian Hinglish (Hindi in Roman script).
    
    CRITICAL TIME & LENGTH RULES:
    1. Length: Exactly 50 to 60 words (Designed for a 30 to 35-second spoken short video).
    2. Sentence Structure: MUST HAVE A PROPER ENDING. Do NOT cut off mid-sentence.
    3. TONE: Natural, highly energetic Indian guy (Bunty style). Use expressions like 'Sun bhai...', 'Pata hai?'.
    4. Formatting: Hook -> Complete Mind-blowing Fact/Story -> Clear Call to Action ending.
    5. Output: ONLY the pure spoken Hindi/Hinglish text. NO extra labels, brackets, or scene titles.
    """

    # Model fallback list to prevent 404 errors
    models_to_try = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    response = None

    for model_name in models_to_try:
        try:
            print(f"Trying Gemini model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                print(f"Successfully generated script using {model_name}")
                break
        except Exception as e:
            print(f"Failed with {model_name}: {e}")

    if not response or not response.text:
        raise RuntimeError("Failed to generate script with all attempted Gemini models.")

    script_text = response.text.strip()
    
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)
        
    print("--- 30-Second Script Generated ---")
    print(script_text)

if __name__ == "__main__":
    generate_script()
