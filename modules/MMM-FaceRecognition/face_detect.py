# import face_recognition
# import cv2
# import numpy as np
# from gtts import gTTS
# from playsound import playsound
# import os
# import time
# from new_person import newperson
# from face_encoding import append_face_encodings_to_csv, load_face_encodings_from_csv
# csv_filename = 'modules/MMM-FaceRecognition/facedetails.csv'
# known_face_encodings, known_face_names = load_face_encodings_from_csv(csv_filename)
# # Get a reference to webcam #0 (the default one)
# # Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)

# def greet_person(name):
#     base_name = name.split('-')[0]
#     # Create a text-to-speech object
#     tts = gTTS(text=f"{base_name} नमस्कार!", lang='ne', tld='co.in', slow=False)
#     # Save the audio file
#     audio_file = "output.mp3"
#     tts.save(audio_file)
#     # Play the audio file
#     playsound(audio_file)
#     # Remove the audio file after playing
#     os.remove(audio_file)

# # Initialize variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
# greeted_names = set()  # Set to keep track of greeted names

# # Static bounding box for face alignment (in the middle of the screen)
# static_box_start = (150, 100)  # top-left corner of the static bounding box
# static_box_end = (450, 400)    # bottom-right corner of the static bounding box

# # Initialize a timer
# last_reset_time = time.time()  # Get the current time
# reset_interval = 3600  # Set the reset interval to 1 hour (3600 seconds)
#  # Create a window for displaying video
# # cv2.namedWindow('Video', cv2.WND_PROP_FULLSCREEN)
# # cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# while True:
#      # Clear the greeted names every hour
#     current_time = time.time()
#     if current_time - last_reset_time >= reset_interval:
#         greeted_names.clear()  # Clear the greeted names
#         last_reset_time = current_time  # Reset the timer
#     # Grab a single frame of video
#     ret, frame = video_capture.read()

#     # Draw the static bounding box on the frame
#     cv2.rectangle(frame, static_box_start, static_box_end, (0, 255, 0), 2)

#     # Only process every other frame of video to save time
#     if process_this_frame:
#         # Resize frame of video to 1/4 size for faster face recognition processing
#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

#         # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#         rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#         # Find all the faces and face encodings in the current frame of video
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

#         face_names = []
#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             # Scale up the face location
#             top, right, bottom, left = [v * 4 for v in face_location]

#             # See if the face is a match for the known face(s)
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"

#             # Use the known face with the smallest distance to the new face
#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]

#             face_names.append(name)

#             # Check if the face is inside the static bounding box
#             if (left > static_box_start[0] and right < static_box_end[0] and 
#                 top > static_box_start[1] and bottom < static_box_end[1]):
                
#                 if name == "Unknown":
#                     # Capture the image and save it for a new person
#                     newperson(frame)  # Custom function to handle new person
#                     append_face_encodings_to_csv(image_folder='modules/MMM-FaceRecognition/testimage', csv_filename='facedetails.csv')
#                     known_face_encodings, known_face_names = load_face_encodings_from_csv('modules/MMM-FaceRecognition/facedetails.csv')

#                 # Greet the detected person if not already greeted
#                 if name != "Unknown" and name not in greeted_names:
#                     greet_person(name)
#                     greeted_names.add(name)  # Add name to the set of greeted names

#     process_this_frame = not process_this_frame

#     # Display the results
#     for (top, right, bottom, left), name in zip(face_locations, face_names):
#         # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#         top *= 4
#         right *= 4
#         bottom *= 4
#         left *= 4

#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#         # Optionally, draw the person's name on the screen
#         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#     # Display the resulting image
#     cv2.imshow('Video', frame)

#     # Hit 'q' on the keyboard to quit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release handle to the webcam
# video_capture.release()
# cv2.destroyAllWindows()

import face_recognition
import cv2
import numpy as np
from gtts import gTTS
from playsound import playsound
import os
import time
from new_person import newperson
from face_encoding import append_face_encodings_to_csv, load_face_encodings_from_csv

csv_filename = 'modules/MMM-FaceRecognition/facedetails.csv'
known_face_encodings, known_face_names = load_face_encodings_from_csv(csv_filename)

video_capture = cv2.VideoCapture(0)

def greet_person(name):
    base_name = name.split('-')[0]
    tts = gTTS(text=f"{base_name} नमस्कार!", lang='ne', tld='co.in', slow=False)
    audio_file = "output.mp3"
    tts.save(audio_file)
    playsound(audio_file)
    os.remove(audio_file)

# Initialize variables
greeted_names = set()
static_box_start = (150, 100)
static_box_end = (450, 400)
last_reset_time = time.time()
reset_interval = 3600
frame_batch = []
batch_size = 5  # Number of frames to process in one go

def process_batch(frames, known_face_encodings, known_face_names):
    global greeted_names
     
    for frame in frames:
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and compute encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            top, right, bottom, left = [v * 4 for v in face_location]
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches and matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            # Check bounding box and greet logic
            if (left > static_box_start[0] and right < static_box_end[0] and 
                top > static_box_start[1] and bottom < static_box_end[1]):
                
                if name == "Unknown":
                    newperson(frame)
                    append_face_encodings_to_csv(image_folder='modules/MMM-FaceRecognition/testimage', 
                                                 csv_filename='facedetails.csv')
                    known_face_encodings, known_face_names = load_face_encodings_from_csv(csv_filename)

                if name != "Unknown" and name not in greeted_names:
                    greet_person(name)
                    greeted_names.add(name)

        # Draw boxes and names
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    return frames
# Initialize processed_frames to avoid NameError
processed_frames = []

while True:
   
    # Clear greeted names every hour
    current_time = time.time()
    if current_time - last_reset_time >= reset_interval:
        greeted_names.clear()
        last_reset_time = current_time

    # Capture frame and add to batch
    ret, frame = video_capture.read()
    if not ret:
        break
    frame_batch.append(frame)

     # Draw the static bounding box on the frame
    cv2.rectangle(frame, static_box_start, static_box_end, (0, 255, 0), 2)

    # Process batch when it reaches batch size
    if len(frame_batch) == batch_size:
        processed_frames = process_batch(frame_batch, known_face_encodings, known_face_names)
        frame_batch = []  # Clear the batch

    # Display the last processed frame
    if len(processed_frames) > 0:
        cv2.imshow('Video', processed_frames[-1])

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
