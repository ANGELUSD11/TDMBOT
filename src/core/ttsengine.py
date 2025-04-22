from gtts import gTTS
import uuid
import os

def generate_speech(text: str, output_path: str = None):
    if output_path is None:
        output_path = f"./tts/audio_path/audio_{uuid.uuid4().hex}.mp3"

    tts = gTTS(text=text, lang='es')  # Idioma español
    tts.save(output_path)
    return output_path
