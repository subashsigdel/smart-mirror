import os
import csv
import face_recognition
import numpy as np
from typing import List, Tuple

import os
import csv
import face_recognition
from typing import List

def append_face_encodings_to_csv(image_folder: str, csv_filename: str, processed_folder: str) -> None:
    """
    Append new face encodings from images in a folder to a CSV file and move processed images to another folder.

    Args:
        image_folder (str): Path to the folder containing images.
        csv_filename (str): Path to the CSV file to store face encodings.
        processed_folder (str): Path to the folder where processed images will be moved.
    """
    face_data: List[List] = []

    # Create the processed folder if it doesn't exist
    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    existing_names: set = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                existing_names.add(row[0])

    for filename in os.listdir(image_folder):
        if filename.lower().endswith((".jpeg", ".jpg", ".png")):
            person_name = os.path.splitext(filename)[0]
            print(f"Processing {person_name}...")

            if person_name in existing_names:
                print(f"qSkipping {person_name}, already encoded.")
                continue

            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)

            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                face_encoding = face_encodings[0]

                face_data.append([person_name] + face_encoding.tolist())
                print(f"Encoded and added {person_name}")

                # Move the processed image to the processed folder
                new_image_path = os.path.join(processed_folder, filename)
                os.rename(image_path, new_image_path)
                print(f"Moved {filename} to {processed_folder}")

    if face_data:
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if os.stat(csv_filename).st_size == 0:
                writer.writerow(["Name"] + [f"Encoding_{i+1}" for i in range(128)])  # Header
            writer.writerows(face_data)

        print(f"New face encodings appended to {csv_filename}")
    else:
        print("No new face encodings to add.")


def load_face_encodings_from_csv(csv_filename: str) -> Tuple[List[np.ndarray], List[str]]:
    """
    Load face encodings and names from a CSV file.

    Args:
        csv_filename (str): Path to the CSV file containing face encodings.

    Returns:
        Tuple[List[np.ndarray], List[str]]: Lists of known face encodings and names.
    """
    known_face_encodings: List[np.ndarray] = []
    known_face_names: List[str] = []

    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                name = row[0]
                encoding = np.array(list(map(float, row[1:])), dtype=np.float32)

                known_face_names.append(name)
                known_face_encodings.append(encoding)

    return known_face_encodings, known_face_names
