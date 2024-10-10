import cv2
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as sr

def newperson(frame):
    def ask_name():
        """Uses text-to-speech to ask for the person's name in Nepali."""
        tts = gTTS(text="तपाईको नाम के हो ?", lang='ne', tld='co.in', slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)

    def name_input(max_retries=2, timeout=30):
        """Listens for the user's name using speech recognition."""
        recognizer = sr.Recognizer()

        for attempt in range(max_retries + 1):
            with sr.Microphone() as source:
                print(f"Attempt {attempt + 1}: Listening in Nepali...")
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                try:
                    audio = recognizer.listen(source, timeout=timeout)  # Listen for audio
                    name = recognizer.recognize_google(audio, language="ne-NP")  # Recognize speech
                    print(f"Recognized Name: {name}")
                    return name  # Return the recognized name
                except sr.UnknownValueError:
                    print("Could not understand the audio, please say it again.")
                except sr.WaitTimeoutError:
                    print("Listening timed out, please try saying your name again.")
                except sr.RequestError:
                    print("Request failed; check your internet connection.")
                    break  # Exit if there's a connection issue

        print("Failed to recognize after several attempts.")
        return None  # Return None if name recognition failed

    ask_name()

    name = name_input()
    if name:  # Check if a name was successfully recognized
        # Save the image with the recognized name
        cv2.imwrite(f"testimage/{name}.png", frame)
        print(f"Image saved as: testimage/{name}.png")
    else:
        print("Image not saved due to name recognition failure.")
