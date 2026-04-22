import json
from groq import Groq

def get_visual_nuance_groq(text, key, model_choice="llama-3.3-70b-versatile"):
    client = Groq(api_key=key)
    
    prompt = f"""
    Analyze the emotional nuance of this phrase: "{text}"
    Return ONLY a JSON object with:
    "color": (hex code), "font_weight": "bold" or "normal", 
    "animation": "none", "shake", or "pulse", "explanation": (1 sentence).
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model_choice,
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)