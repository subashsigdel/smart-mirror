import os
import time
import cv2
import numpy as np
from typing import List, Tuple, Set
from numpy.linalg import norm
import insightface
from insightface.app import FaceAnalysis
from Load_Face_Encoding import load_face_encodings_from_csv
from Face_Encoding import SaveFaceEncodingToCSV
from Greet_person import greet_person

# Config
os.environ['INSIGHTFACE_HOME'] = 'insightface'
os.environ['INSIGHTFACE_DOWNLOAD_DISABLE'] = '1'
CSV_FILEPATH = "face_encodings.csv"
IMAGE_FOLDER = "Test_images"
PROCESSED_FOLDER = "Processed_Folder"
STATIC_BOX_START: Tuple[int, int] = (150, 100)
STATIC_BOX_END: Tuple[int, int] = (450, 400)
model_root = "insightface/models"

# Initialize InsightFace with CPU
app = FaceAnalysis(name='buffalo_s', root=model_root, providers=['CPUExecutionProvider'], download=False)
app.prepare(ctx_id=0, det_size=(640, 640))  
# Remove unused models to save memory & CPU
app.models.pop('genderage', None)
app.models.pop('landmark_3d_68', None)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if norm(vec1) == 0 or norm(vec2) == 0:
        return -1.0
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))

def recognize_face_from_embedding(
    target_embedding: np.ndarray,
    known_embeddings: List[np.ndarray],
    known_names: List[str],
    threshold: float = 0.4
) -> Tuple[str, float]:
    best_match_name = "Unknown"
    best_similarity = -1.0

    for name, known_embedding in zip(known_names, known_embeddings):
        similarity = cosine_similarity(target_embedding, known_embedding)
        print(f"[DEBUG] Similarity with {name}: {similarity:.4f}")
        if similarity > best_similarity and similarity > threshold:
            best_similarity = similarity
            best_match_name = name

    if best_match_name == "Unknown":
        print("[INFO] No match passed the similarity threshold.")
    return best_match_name, best_similarity

def draw_bounding_box(frame: np.ndarray, bbox: Tuple[int, int, int, int], label: str) -> None:
    left, top, right, bottom = bbox
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

def process_batch(
    frames: List[np.ndarray],
    greeted_names: Set[str],
    known_face_embeddings: List[np.ndarray],
    known_face_names: List[str],
) -> None:
    for frame in frames:
        resized_frame = cv2.resize(frame, (640, 480))
        faces = app.get(resized_frame)

        for face in faces:
            x1, y1, x2, y2 = map(int, face.bbox)
            name, similarity = recognize_face_from_embedding(
                target_embedding=face.embedding,
                known_embeddings=known_face_embeddings,
                known_names=known_face_names
            )

            if STATIC_BOX_START[0] < x1 < STATIC_BOX_END[0] and STATIC_BOX_START[1] < y1 < STATIC_BOX_END[1]:
                if name == "Unknown":
                    print("[INFO] Unrecognized face inside ROI.")
                    # SaveFaceEncodingToCSV(IMAGE_FOLDER, CSV_FILEPATH, PROCESSED_FOLDER)
                elif name not in greeted_names:
                    print(f"[INFO] Recognized {name}, greeting now.")
                    start_time = time.time()
                    greet_person(name)
                    end_time = time.time()
                    print(f"[INFO] Greeting {name} took {end_time - start_time:.2f} seconds.")
                    greeted_names.add(name)

            draw_bounding_box(
                frame,
                bbox=(x1, y1, x2, y2),
                label=f"{name} ({similarity:.2f})"
            )
