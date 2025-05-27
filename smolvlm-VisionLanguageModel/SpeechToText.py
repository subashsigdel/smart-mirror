import os
from gtts import gTTS
import pygame
import time

def TTS(text, lang='en', filename='temp_output.mp3'):
    # Generate speech and save
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    print(f"Saved speech to {filename}")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Cleanup
    pygame.mixer.music.unload()
    pygame.mixer.quit()

    # Delete the audio file
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted {filename}")

# Example usage

