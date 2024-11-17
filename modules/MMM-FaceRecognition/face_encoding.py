import face_recognition
import os
import csv

def append_face_encodings_to_csv(image_folder, csv_filename):
    # List to store encodings and names for new images
    face_data = []

    # Get the names of already encoded people from the CSV
    existing_names = set()
    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r") as file:
            reader = csv.reader(file)
            try:
                # Try to skip the header row
                next(reader)
            except StopIteration:
                # If the file is empty, do nothing
                print(f"{csv_filename} is empty, starting fresh.")
            else:
                # Read all existing names
                for row in reader:
                    existing_names.add(row[0])  # The name is the first column

    # Loop through each image in the folder
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
            # Get the person's name from the file name (without extension)
            person_name = os.path.splitext(filename)[0]
            print(person_name)

            # Skip if the name already exists in the CSV
            if person_name in existing_names:
                print(f"Skipping {person_name}, already encoded.")
                continue

            # Load the image file
            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)

            # Get face encodings
            face_encodings = face_recognition.face_encodings(image)

            # Check if a face was found
            if len(face_encodings) > 0:
                # Use the first face encoding
                face_encoding = face_encodings[0]

                # Append the name and encoding to the list
                face_data.append([person_name] + face_encoding.tolist())
                print(f"Encoded and added {person_name}")

    # Append the new face data to the existing CSV file
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write the header row if the file is empty
        if os.stat(csv_filename).st_size == 0:
            writer.writerow(["Name"] + [f"Encoding_{i+1}" for i in range(128)])  # Header
        # Write each new person's name and encodings
        writer.writerows(face_data)

    if face_data:
        print(f"New face encodings appended to {csv_filename}")
    else:
        print("No new face encodings to add.")

# Example usage:
image_folder = "modules/MMM-FaceRecognition/testimage"
csv_filename = "modules/MMM-FaceRecognition/facedetails.csv"
append_face_encodings_to_csv(image_folder, csv_filename)



import csv
import numpy as np

def load_face_encodings_from_csv(csv_filename):
    known_face_encodings = []
    known_face_names = []

    if os.path.exists(csv_filename):
        with open(csv_filename, mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row

            for row in reader:
                name = row[0]
                encoding = list(map(float, row[1:]))  # Convert all encoding values to float

                known_face_names.append(name)
                known_face_encodings.append(np.array(encoding))

    return known_face_encodings, known_face_names

# Example usage
csv_filename = "modules/MMM-FaceRecognition/facedetails.csv"
known_face_encodings, known_face_names = load_face_encodings_from_csv(csv_filename)

print("Known face names:", known_face_names)
print("Number of known face encodings:", known_face_encodings)
