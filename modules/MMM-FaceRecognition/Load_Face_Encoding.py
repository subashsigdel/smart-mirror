import csv
from typing import List,Tuple
import numpy as np
import os



def load_face_encodings_from_csv(csv_filename: str) -> Tuple[List[np.ndarray], List[str]]:
    """
    Load face encodings and names from a CSV file.

    Args:
        csv_filename (str): Path to the CSV file containing face encodings.

    Returns:
        Tuple[List[np.ndarray], List[str]]: Lists of known face encodings and names.
    """
    known_face_embedding: List[np.ndarray] = []
    known_face_names: List[str] = []

    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                name = row[0]
                encoding = np.array(list(map(float, row[1:])), dtype=np.float32)

                known_face_names.append(name)
                known_face_embedding.append(encoding)
    print(known_face_embedding)
    print(known_face_names)

    return known_face_embedding, known_face_names
