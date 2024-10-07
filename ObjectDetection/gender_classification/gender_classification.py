import cv2
import os

class GenderDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Specify the correct paths to the configuration and weights files
        config_file = '/home/hitech/smart-mirror/ObjectDetection/gender_classification/gender_deploy.prototxt'
        weights_file = '/home/hitech/smart-mirror/ObjectDetection/gender_classification/gender_net.caffemodel'

        # Ensure these files exist in your directory
        if not os.path.isfile(config_file) or not os.path.isfile(weights_file):
            raise FileNotFoundError("Configuration or weights file not found.")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.gender_net = cv2.dnn.readNetFromCaffe(config_file, weights_file)
        self.gender_list = ['Man', 'Woman']

    def detect_faces(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, 1.1, 4)
        return faces

    def detect_gender(self, face_region):
        blob = cv2.dnn.blobFromImage(face_region, 1.0, (227, 227), (104, 117, 123), swapRB=False)
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        confidence = gender_preds[0].max()  # Get the highest confidence value
        gender = self.gender_list[gender_preds[0].argmax()]
        return gender, confidence
