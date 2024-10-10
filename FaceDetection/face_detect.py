import face_recognizer
import cv2
import numpy as np
from gtts import gTTS
from playsound import playsound
import os
from new_person import newperson
from face_encoding import append_face_encodings_to_csv, load_face_encodings_from_csv

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


def greet_person(name):
    # Create a text-to-speech object
    tts = gTTS(text=f"{name} नमस्ते!", lang='ne', tld='co.in', slow=False)
    # Save the audio file
    audio_file = "output.mp3"
    tts.save(audio_file)
    # Play the audio file
    playsound(audio_file)
    # Remove the audio file after playing
    os.remove(audio_file)


# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
greeted_names = set()  # Set to keep track of greeted names

# Static bounding box for face alignment (in the middle of the screen)
static_box_start = (150, 100)  # top-left corner of the static bounding box
static_box_end = (450, 400)  # bottom-right corner of the static bounding box

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Draw the static bounding box on the frame
    cv2.rectangle(frame, static_box_start, static_box_end, (0, 255, 0), 2)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognizer.face_locations(rgb_small_frame)
        face_encodings = face_recognizer.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Scale up the face location
            top, right, bottom, left = [v * 4 for v in face_location]
            known_face_encodings, known_face_names = load_face_encodings_from_csv('facedetails.csv')
            # See if the face is a match for the known face(s)
            matches = face_recognizer.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognizer.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # Check if the face is inside the static bounding box
            if (left > static_box_start[0] and right < static_box_end[0] and
                    top > static_box_start[1] and bottom < static_box_end[1]):

                if name == "Unknown":
                    # Capture the image and save it for a new person
                    newperson(frame)  # Custom function to handle new person
                    append_face_encodings_to_csv(image_folder='testimage', csv_filename='facedetails.csv')
                    known_face_encodings, known_face_names = load_face_encodings_from_csv('facedetails.csv')

                # Greet the detected person if not already greeted
                if name != "Unknown" and name not in greeted_names:
                    greet_person(name)
                    greeted_names.add(name)  # Add name to the set of greeted names

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Optionally, draw the person's name on the screen
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
