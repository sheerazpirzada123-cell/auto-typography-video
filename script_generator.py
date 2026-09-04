import os
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable missing!")

genai.configure(api_key=api_key)

def generate_script():
    prompt = """
    Write a complete YouTube Shorts script in Indian Hinglish (Hindi written in Roman script).

    RULES:
    1. Length: Exactly 50 to 60 words (30 to 35 seconds total video duration).
    2. Tone: Energetic guy telling his friend a crazy fact/theory. Casual, punchy, natural spoken rhythm (not written/formal). Use hooks like 'Sun bhai...', 'Pata hai?', 'Ye sunke tera dimaag ghoom jayega'.
    3. Content: Must deliver ONE COMPLETE, mind-blowing fact, theory, or story without leaving the sentence cutoff or incomplete at the end. Pick genuinely surprising science, history, psychology, space, or "how things really work" facts — not generic trivia.
    4. Format: Hook (first 3 seconds must grab attention) -> Full Fact/Theory explained simply -> Punchy ending line that makes people want to share it or comment.
    5. Output: ONLY spoken script text. NO labels, brackets, scene titles, or emojis.
    """

    # Ordered newest -> oldest so the pipeline auto-upgrades and still has working
    # fallbacks. Update this list if Google deprecates a model (check
    # https://ai.google.dev/gemini-api/docs/models for current IDs).
    models_to_try = ["gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash"]
    response = None

    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            if response and response.text:
                print(f"Generated script using model: {model_name}")
                break
        except Exception as e:
            print(f"Skipping model {model_name}: {e}")

    if not response or not response.text:
        raise RuntimeError("All Gemini models failed.")

    script_text = response.text.strip()
    
    with open("script.txt", "w", encoding="utf-8") as f:
        f.write(script_text)
        
    print("--- New 30-Sec Complete Script Generated ---")
    print(script_text)

if __name__ == "__main__":
    generate_script()
