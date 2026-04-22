import streamlit as st
from groq_utils import get_visual_nuance_groq
from whisper_utils import transcribe_audio
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="EyeHear", page_icon="👁️")

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    groq_key = st.text_input("Enter Groq API Key", type="password")
    openai_key = st.text_input("Enter OpenAI API Key (for Whisper)", type="password")

st.title("👁️ EyeHear: Visualizing Nuance")

# --- Audio Input ---
audio_bytes = audio_recorder(text="Click to record voice...", icon_size="2x")

if audio_bytes:
    if not openai_key:
        st.error("Please enter OpenAI API Key in the sidebar.")
    else:
        with st.spinner("Whisper is listening..."):
            user_text = transcribe_audio(audio_bytes, openai_key)
            # nxt -> emotion analysis
            st.info(f"Detected: {user_text}")

            # emotion analysis
            if groq_key and user_text:
                try:
                    nuance = get_visual_nuance_groq(user_text, groq_key)
                    
                    st.markdown(f"""
                        <style>
                        /* animation */
                        .subtitle-text {{ color: {nuance['color']}; ... }}
                        </style>
                        <div class="subtitle-container"><div class="subtitle-text">{user_text}</div></div>
                    """, unsafe_allow_html=True)
                    st.write(f"**Explanation:** {nuance['explanation']}")
                except Exception as e:
                    st.error(f"Groq Error: {e}")