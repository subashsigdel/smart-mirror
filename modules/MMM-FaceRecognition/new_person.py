import os
import uuid
from typing import Optional
import cv2
import speech_recognition as sr
from gtts import gTTS
import pygame  # Import pygame for audio playback

def ask_name() -> None:
    """Plays a prompt asking the user for their name in Nepali using pygame."""
    audio_file = "output.mp3"
    tts = gTTS(text="तपाईको नाम के हो?", lang="ne", tld="co.in", slow=False)
    tts.save(audio_file)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load and play the audio file asynchronously
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Clean up the audio file after playback
    if os.path.exists(audio_file):
        os.remove(audio_file)

def name_input(max_retries: int = 2, timeout: int = 30) -> Optional[str]:
    """
    Captures and recognizes the user's name via speech.

    Args:
        max_retries: Maximum number of retries for speech recognition.
        timeout: Time (in seconds) to wait for the user's input.

    Returns:
        The recognized name as a string, or None if recognition fails.
    """
    recognizer = sr.Recognizer()

    for attempt in range(max_retries + 1):
        try:
            with sr.Microphone() as source:
                print(f"Attempt {attempt + 1}: Listening for your name...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=timeout)

            name = recognizer.recognize_google(audio, language="ne-NP")
            name = (
                name.replace("मेरो नाम", "")
                .replace("नाम", "")
                .replace("हो", "")
                .strip()
            )

            if name:
                print(f"Recognized Name: {name}")
                return name
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except sr.WaitTimeoutError:
            print("Listening timed out. Please say your name again.")
        except sr.RequestError:
            print("Request failed. Check your internet connection.")
            break

    print("Failed to recognize name after multiple attempts.")
    return None


def new_person(frame: cv2.Mat) -> None:
    """
    Captures the user's name via speech and saves their photo with a unique ID.

    Args:
        frame: The frame (image) to save.
    """
    ask_name()  # Ask for the user's name
    user_name = name_input()  # Capture the name

    if user_name:
        unique_id = uuid.uuid4().hex[:4]  # Generate a unique ID
        file_path = f"/home/hitech/sm/smart-mirror/modules/MMM-FaceRecognition/testimage/{user_name}-{unique_id}.png"
        cv2.imwrite(file_path, frame)  # Save the image
        print(f"Image saved as {file_path}")
    else:
        print("Could not save the image as no name was provided.")
