# speech_recognizer/speech_recognition.py

from gtts import gTTS
from playsound import playsound
import os

class SpeechRecognizer:
    def greet_person(self, name):
        tts = gTTS(text=f"{name} नमस्ते!", lang='ne', tld='co.in', slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
