import pygame
from gtts import gTTS
import time
import os
def greet_person(name: str) -> None:
    """Greets a person by name using text-to-speech."""
    base_name: str = name.split('-')[0]
    audio_file: str = "output.mp3"
    try:
        # Start timing text-to-speech
        start_tts_time = time.time()

        # Generate the speech file
        tts: gTTS = gTTS(text=f"{base_name} नमस्कार!", lang='en', slow=False)
        tts.save(audio_file)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the audio file asynchronously
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # End timing text-to-speech
        end_tts_time = time.time()
        print(f"Text-to-speech and playback for {base_name} took {end_tts_time - start_tts_time:.2f} seconds.")
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)
