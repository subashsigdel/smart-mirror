# importing OpenCV library 
import cv2
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as sr



def newperson(frame):
    
    def ask_name():
        # Create a text-to-speech object
        tts = gTTS(text=f"तपाईको नाम के हो ?", lang='ne',tld='co.in',slow=False)
        # Save the audio file
        audio_file = "output.mp3"
        tts.save(audio_file)
        # Play the audio file
        playsound(audio_file)
        # Remove the audio file after playing
        os.remove(audio_file)

    ask_name()


    def name_input(max_retries=2, timeout=30):
        # Initialize recognizer
        recognizer = sr.Recognizer()

        for attempt in range(max_retries + 1):
            # Capture audio from the microphone
            with sr.Microphone() as source:
                print(f"Attempt {attempt + 1}: Listening in Nepali...")

                try:
                    # Adjust for ambient noise and listen with a timeout
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=timeout)

                    # Recognize the speech in Nepali using Google Web Speech API
                    name = recognizer.recognize_google(audio, language="ne-NP")
                    print(f"Recognized Name: {name}")
                    return name  # If successful, return the recognized name

                except sr.UnknownValueError:
                    print("Could not understand the audio, please say it again.")

                except sr.WaitTimeoutError:
                    print("Listening timed out, please try saying your name again.")

                except sr.RequestError:
                    print("Request failed; check your internet connection.")
                    break  # If there's a connection issue, break out of the loop

        # If no valid name is recognized after all attempts
        print("Failed to recognize after several attempts.")
        return name
        




    
    cv2.imwrite(f"testimage/{name_input()}.png", frame)
 