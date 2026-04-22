# whisper_utils.py
import io
from openai import OpenAI

# Sppech to text function
def transcribe_audio(audio_bytes, api_key):
    client = OpenAI(api_key=api_key)
    
    # Create a virtual file in memory
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "audio.wav"
    
    # Execurte transcribing
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text