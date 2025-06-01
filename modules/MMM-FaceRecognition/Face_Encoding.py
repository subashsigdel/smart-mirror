import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import os
import csv

# Disable auto-downloading of models
os.environ['INSIGHTFACE_HOME'] = 'insightface'
os.environ['INSIGHTFACE_DOWNLOAD_DISABLE'] = '1'
model_root = "insightface/models"

# Initialize InsightFace with CPU
app = FaceAnalysis(name='buffalo_s', root=model_root, providers=['CPUExecutionProvider'], download=False)
app.prepare(ctx_id=0, det_size=(640, 640))  
# Remove unused models to save memory & CPU
app.models.pop('genderage', None)

def SaveFaceEncodingToCSV(name, face_embedding, csv_path=str)-> None:
    # Create CSV with header if it doesn't exist
    if not os.path.exists(csv_path):
        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            header = ['name'] + [f'face_embedding_{i}' for i in range(512)]
            writer.writerow(header)

    # Save the embedding
    with open(csv_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        row = [name] + face_embedding.tolist()
        writer.writerow(row)



def FaceEmbedding(imagefolder=str, processedfolder=str, csvfilename=str) -> None:
    """
    Append new face encodings from images in a folder to a CSV file 
    and move processed images to another folder using try-except-finally.

    Args:
        imagefolder (str): Path to the folder containing images.
        processedfolder (str): Path to the folder where processed images will be moved.
        csvfilename (str): Path to the CSV file to store face encodings.
    """
    for filename in os.listdir(imagefolder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        filePath = os.path.join(imagefolder, filename)
        new_image_path = os.path.join(processedfolder, filename)
        name = os.path.splitext(filename)[0]

        try:
            img = cv2.imread(filePath)
            if img is None:
                print(f"Could not read image: {filename}")
                continue

            faces = app.get(img)
            if not faces:
                print(f"No face found in: {filename}")
                continue

            for face in faces:
                face_embedding = face.embedding
                if face_embedding is None:
                    print(f"No embedding generated for: {filename}")
                    continue

                SaveFaceEncodingToCSV(name=name, face_embedding=face_embedding, csv_path=csvfilename)
                print(f"Saved embedding for {name}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

        finally:
            # Move the processed image regardless of success or failure
            try:
                os.rename(filePath, new_image_path)
                print(f"Moved {filename} to {processedfolder}")
            except Exception as move_error:
                print(f"Failed to move {filename}: {move_error}")

if __name__ == "__main__":
    FaceEmbedding(imagefolder="Test_images",processedfolder="Processed_Folder",csvfilename="face_encodings.csv")