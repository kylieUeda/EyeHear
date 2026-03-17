import streamlit as st
import google.generativeai as genai
import json

# --- Page Config ---
st.set_page_config(page_title="EyeHear | Gemini Edition", page_icon="👁️")

# --- Sidebar: Gemini API Setup ---
with st.sidebar:
    st.title("Settings")
    st.markdown("[Get a Free Gemini API Key here](https://aistudio.google.com/)")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    # Using 3.1 Flash for maximum speed/low latency
    model_choice = "gemini-3.1-flash" 

# --- App Header ---
st.title("👁️ EyeHear: Visualizing Nuance")
st.info("Milestone 1: Powered by Google Gemini 3.1")

# --- Core Logic ---
def get_visual_nuance(text, key):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_choice)
    
    prompt = f"""
    Analyze the emotional nuance of this phrase: "{text}"
    Return ONLY a JSON object (no markdown, no backticks) with:
    "color": (a hex code representing the emotion),
    "font_weight": ("bold" or "normal"),
    "animation": ("none", "shake", or "pulse"),
    "explanation": (1 sentence explaining the choice).
    """
    
    # Using the generation_config to force JSON output
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)

# --- User Input ---
user_text = st.text_area("What is being said?", placeholder="e.g., 'I can't believe you did that!'")

if st.button("Generate Visual Subtitle"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not user_text:
        st.warning("Please enter some text.")
    else:
        with st.spinner("Gemini is sensing the vibe..."):
            try:
                nuance = get_visual_nuance(user_text, api_key)
                
                # --- Visual Output ---
                st.markdown(f"""
                    <style>
                    @keyframes pulse {{
                        0% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.1); }}
                        100% {{ transform: scale(1); }}
                    }}
                    @keyframes shake {{
                        0% {{ transform: translate(2px, 2px); }}
                        25% {{ transform: translate(-2px, -2px); }}
                        50% {{ transform: translate(-2px, 2px); }}
                        100% {{ transform: translate(2px, -2px); }}
                    }}
                    .subtitle-container {{
                        background-color: #0e1117;
                        padding: 40px;
                        border-radius: 20px;
                        text-align: center;
                        border: 3px solid {nuance['color']};
                    }}
                    .subtitle-text {{
                        color: {nuance['color']};
                        font-weight: {nuance['font_weight']};
                        font-size: 3.5rem;
                        animation: {nuance['animation']} 0.6s infinite;
                        display: inline-block;
                    }}
                    </style>
                    <div class="subtitle-container">
                        <div class="subtitle-text">{user_text}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write(f"**Emotion Analysis:** {nuance['explanation']}")
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")