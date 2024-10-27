# importing OpenCV library 
import cv2
from gtts import gTTS
from playsound import playsound
import os
import speech_recognition as sr
import uuid  # To generate unique IDs


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
                     # Process the text to remove unnecessary words
                    # Remove "मेरो नाम" or "नाम" and extract the first name
                    if "मेरो नाम" in name:
                        name = name.replace("मेरो नाम", "").strip()
                    elif "नाम" in name:
                        name = name.replace("नाम", "").strip()
                    elif "हो" in name:
                        name = name.replace("हो", "").strip()
                        
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
        





    # initialize the camera 
    # If you have multiple camera connected with 
    # current device, assign a value in cam_port 
    # variable according to that 
    # cam_port = 0
    # cam = cv2.VideoCapture(cam_port)

    # while True:
    #     success, img = cam.read()
    #     #img = captureScreen()
    #     # saving image in local storage
    unique_id = str(uuid.uuid4().hex[:4])
    cv2.imwrite(f"testimage/{name_input()}-{unique_id}.png", frame)
        # # break
        # #cv2.imshow('Webcam',img)
        # #cv2.waitKey(1)
        # cv2.imshow('my video', img)
        # if cv2.waitKey(13) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break