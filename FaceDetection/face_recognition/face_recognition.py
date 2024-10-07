import cv2
import numpy as np

from
from face_encoding import load_face_encodings_from_csv, append_face_encodings_to_csv


class FaceRecognition:
    def __init__(self, csv_filename='facedetails.csv'):
        self.known_face_encodings, self.known_face_names = load_face_encodings_from_csv(csv_filename)
        self.csv_filename = csv_filename

    def recognize_faces(self, frame):
        # Resize the frame for faster processing
        small_frame = self.resize_frame(frame)
        rgb_small_frame = self.convert_to_rgb(small_frame)

        # Detect face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            name = self.match_face(face_encoding)
            face_names.append(name)

        return face_locations, face_names

    def match_face(self, face_encoding):
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            return self.known_face_names[best_match_index]
        return "Unknown"

    def update_encodings(self, new_face_image):
        append_face_encodings_to_csv(new_face_image, self.csv_filename)
        self.known_face_encodings, self.known_face_names = load_face_encodings_from_csv(self.csv_filename)

    @staticmethod
    def resize_frame(frame):
        return cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    @staticmethod
    def convert_to_rgb(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
