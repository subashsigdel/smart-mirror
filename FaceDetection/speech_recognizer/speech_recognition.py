from gtts import gTTS
from playsound import playsound
import os

class SpeechModule:
    def __init__(self, lang='ne', tld='co.in'):
        self.lang = lang
        self.tld = tld

    def greet_person(self, name):
        tts = gTTS(text=f"{name} नमस्ते!", lang=self.lang, tld=self.tld, slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
