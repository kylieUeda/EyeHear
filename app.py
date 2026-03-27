import streamlit as st
from groq import Groq 

# --- Page Config ---
st.set_page_config(page_title="EyeHear | Groq Edition", page_icon="👁️")

# --- Sidebar: Groq API Setup ---
with st.sidebar:
    st.title("Settings")
    st.markdown("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")
    api_key = st.text_input("Enter Groq API Key", type="password")
    model_choice = "llama-3.3-70b-versatile"

st.title("👁️ EyeHear: Visualizing Nuance")
st.info("Milestone 1: Powered by Groq (High Speed)")

def get_visual_nuance_groq(text, key):
    client = Groq(api_key=key) #  Initialize Groq client
    
    prompt = f"""
    Analyze the emotional nuance of this phrase: "{text}"
    Return ONLY a JSON object with:
    "color": (hex code), "font_weight": "bold" or "normal", 
    "animation": "none", "shake", or "pulse", "explanation": (1 sentence).
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_choice,
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)

# --- User Input & Logic ---
user_text = st.text_area("What is being said?", placeholder="e.g., 'That is amazing!'")

if st.button("Generate Visual Subtitle"):
    if not api_key:
        st.error("Please enter your Groq API Key.")
    elif not user_text:
        st.warning("Please enter some text.")
    else:
        with st.spinner("Groq is processing at lightning speed..."):
            try:
                nuance = get_visual_nuance_groq(user_text, api_key)
                
                # --- Visual Output ---
                st.markdown(f"""
                    <style>
                    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
                    @keyframes shake {{ 0% {{ translate: 2px 2px; }} 50% {{ translate: -2px 2px; }} 100% {{ translate: 2px -2px; }} }}
                    .subtitle-container {{
                        background-color: #0e1117; padding: 40px; border-radius: 20px;
                        text-align: center; border: 3px solid {nuance['color']};
                    }}
                    .subtitle-text {{
                        color: {nuance['color']}; font-weight: {nuance['font_weight']};
                        font-size: 3.5rem; animation: {nuance['animation']} 0.6s infinite;
                        display: inline-block;
                    }}
                    </style>
                    <div class="subtitle-container">
                        <div class="subtitle-text">{user_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.write(f"**Emotion Analysis:** {nuance['explanation']}")
                
            except Exception as e:
                st.error(f"Error: {e}")