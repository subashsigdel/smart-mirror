import os
import time
from typing import List, Set, Tuple
import cv2
import face_recognition
import numpy as np
from gtts import gTTS
from playsound import playsound
from face_encoding import append_face_encodings_to_csv, load_face_encodings_from_csv
from new_person import new_person

# Constants
CSV_FILENAME: str = 'modules/MMM-FaceRecognition/facedetails.csv'
BATCH_SIZE: int = 5
RESET_INTERVAL: int = 3600
STATIC_BOX_START: Tuple[int, int] = (150, 100)
STATIC_BOX_END: Tuple[int, int] = (450, 400)

# Load known face encodings
known_face_encodings: List[np.ndarray]
known_face_names: List[str]
known_face_encodings, known_face_names = load_face_encodings_from_csv(CSV_FILENAME)


def greet_person(name: str) -> None:
    """Greets a person by name using text-to-speech."""
    base_name: str = name.split('-')[0]
    audio_file: str = "output.mp3"
    try:
        tts: gTTS = gTTS(text=f"{base_name} नमस्कार!", lang='ne', tld='co.in', slow=False)
        tts.save(audio_file)
        playsound(audio_file)
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

        face_locations: List[Tuple[int, int, int, int]] = face_recognition.face_locations(rgb_small_frame)
        face_encodings: List[np.ndarray] = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_location = [v * 4 for v in face_location]  # Scale back to original size
            matches: List[bool] = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances: np.ndarray = face_recognition.face_distance(known_face_encodings, face_encoding)

            name: str = "Unknown"
            if matches:
                best_match_index: int = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            # Check bounding box and greet logic
            if (STATIC_BOX_START[0] < face_location[3] < STATIC_BOX_END[0] and
                    STATIC_BOX_START[1] < face_location[0] < STATIC_BOX_END[1]):

                if name == "Unknown":
                    new_person(frame)
                    append_face_encodings_to_csv(image_folder='modules/MMM-FaceRecognition/testimage',
                                                 csv_filename=CSV_FILENAME)
                    known_face_encodings, known_face_names = load_face_encodings_from_csv(CSV_FILENAME)

                elif name not in greeted_names:
                    greet_person(name)
                    greeted_names.add(name)

            draw_bounding_box(frame, face_location, name)


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
