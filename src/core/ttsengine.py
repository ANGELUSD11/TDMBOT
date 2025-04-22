import pyttsx3
import uuid
import os

def generate_speech(text: str, output_path: str = None):
    if output_path is None:
        output_path = f"./tts/audio_path/audio_{uuid.uuid4().hex}.mp3"
        
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    
    engine.setProperty("voice", voices[0].id) # set the tts default voice
    engine.setProperty("rate", 150) # set the rate

    engine.save_to_file(text, output_path)
    engine.runAndWait()