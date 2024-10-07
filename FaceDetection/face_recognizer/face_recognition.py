# face_capture/capture.py

import os
import csv
import numpy as np
import face_recognition

class FaceCapture:
    def __init__(self, csv_filename='facedetails.csv'):
        self.csv_filename = csv_filename
        self.known_face_encodings, self.known_face_names = self.load_face_encodings_from_csv(csv_filename)

    def load_face_encodings_from_csv(self, csv_filename):
        known_face_encodings = []
        known_face_names = []

        if os.path.exists(csv_filename):
            with open(csv_filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                for row in reader:
                    name = row[0]
                    encoding = list(map(float, row[1:]))  # Convert all encoding values to float

                    known_face_names.append(name)
                    known_face_encodings.append(np.array(encoding))

        return known_face_encodings, known_face_names

    def process_frame(self, frame):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            return name  # Return the recognized name

        return None  # Return None if no face is recognized
