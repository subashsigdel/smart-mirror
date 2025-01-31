import os
import time
import pygame
from typing import List, Set, Tuple
import cv2
import face_recognition
import numpy as np
from gtts import gTTS
from face_encoding import append_face_encodings_to_csv,load_face_encodings_from_csv
# from new_person import new_person

# Constants
# CSV_FILENAME: str = '/home/hitech/MagicMirrornew/modules/MMM-FaceRecognition/facedetails.csv'
CSV_FILENAME: str = 'facedetails.csv'
BATCH_SIZE: int = 3
RESET_INTERVAL: int = 3600
STATIC_BOX_START: Tuple[int, int] = (150, 100)
STATIC_BOX_END: Tuple[int, int] = (450, 400)
# image_folder: str = '/home/hitech/MagicMirrornew/modules/MMM-FaceRecognition/testimage'
image_folder: str = 'testimage'
processed_folder: str = 'processed_folder'
# Load known face encodings
known_face_encodings: List[np.ndarray]
known_face_names: List[str]
append_face_encodings_to_csv(image_folder,CSV_FILENAME, processed_folder=processed_folder)
known_face_encodings, known_face_names = load_face_encodings_from_csv(CSV_FILENAME)

def greet_person(name: str) -> None:
    """Greets a person by name using text-to-speech."""
    base_name: str = name.split('-')[0]
    audio_file: str = "output.mp3"
    try:
        # Start timing text-to-speech
        start_tts_time = time.time()

        # Generate the speech file
        tts: gTTS = gTTS(text=f"{base_name} नमस्कार!", lang='ne', tld='co.in', slow=False)
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

def greet_Unknown() -> None:
    """Greets a person by name using text-to-speech."""
    audio_file: str = "output.mp3"
    try:

        # Generate the speech file
        tts: gTTS = gTTS(text="नमस्कार!", lang='ne', tld='co.in', slow=False)
        tts.save(audio_file)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the audio file asynchronously
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if os.path.exists(audio_file):
            os.remove(audio_file)


def draw_bounding_box(frame: np.ndarray, face_location: Tuple[int, int, int, int], name: str) -> None:
    """Draws a bounding box with the person's name on the frame."""
    top, right, bottom, left = face_location
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font: int = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



#             draw_bounding_box(frame, face_location, name)
import time  # Ensure this is imported at the top of your file

CONFIDENCE_THRESHOLD = 0.5  # Adjust threshold based on testing

def process_batch(
    frames: List[np.ndarray],
    greeted_names: Set[str],
    known_face_encodings: List[np.ndarray],
    known_face_names: List[str],
) -> None:
    """Processes a batch of frames for face recognition and greeting."""
    for frame in frames:
        small_frame: np.ndarray = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame: np.ndarray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Start timing face recognition
        start_recognition_time = time.time()

        face_locations: List[Tuple[int, int, int, int]] = face_recognition.face_locations(rgb_small_frame)
        face_encodings: List[np.ndarray] = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_location = [v * 4 for v in face_location]  # Scale back to original size
            matches: List[bool] = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances: np.ndarray = face_recognition.face_distance(known_face_encodings, face_encoding)

            name: str = "Unknown"
            confidence: float = 0.0

            if matches:
                best_match_index: int = np.argmin(face_distances)
                confidence = 1 - face_distances[best_match_index]  # Convert distance to confidence score

                if matches[best_match_index] and confidence > CONFIDENCE_THRESHOLD:
                    name = known_face_names[best_match_index]

            # End timing face recognition
            end_recognition_time = time.time()
            print(f"Face recognition for {name} took {end_recognition_time - start_recognition_time:.2f} seconds. Confidence: {confidence:.2f}")

            # Check bounding box and greet logic
            if (STATIC_BOX_START[0] < face_location[3] < STATIC_BOX_END[0] and
                    STATIC_BOX_START[1] < face_location[0] < STATIC_BOX_END[1]):

                if name == "Unknown":
                    append_face_encodings_to_csv(image_folder, CSV_FILENAME, processed_folder)
                    pass

                elif name not in greeted_names:
                    # Start timing greeting
                    start_greeting_time = time.time()
                    greet_person(name)
                    end_greeting_time = time.time()

                    print(f"Greeting {name} took {end_greeting_time - start_greeting_time:.2f} seconds.")
                    greeted_names.add(name)

            draw_bounding_box(frame, face_location, f"{name} ({confidence:.2f})")


def main() -> None:
    """Main loop for video capture and face recognition."""
    global known_face_encodings, known_face_names

    greeted_names: Set[str] = set()
    last_reset_time: float = time.time()
    video_capture: cv2.VideoCapture = cv2.VideoCapture(0)
    frame_batch: List[np.ndarray] = []

    try:
        while True:
            current_time: float = time.time()
            if current_time - last_reset_time >= RESET_INTERVAL:
                greeted_names.clear()
                last_reset_time = current_time

            ret: bool
            frame: np.ndarray
            ret, frame = video_capture.read()
            if not ret:
                break

            frame_batch.append(frame)
            cv2.rectangle(frame, STATIC_BOX_START, STATIC_BOX_END, (0, 255, 0), 2)

            if len(frame_batch) == BATCH_SIZE:
                process_batch(
                    frame_batch, greeted_names, known_face_encodings, known_face_names
                )
                frame_batch = []  # Clear the batch

            # Display the last frame in the batch
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
