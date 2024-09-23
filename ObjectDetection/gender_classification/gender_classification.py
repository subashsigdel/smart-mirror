import cv2

class FaceGenderClassifier:
    def __init__(self):
        # Load face detection and gender classification models
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # Face detection model
        self.gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')  # Gender model
        self.GENDER_LIST = ['Male', 'Female']

    def detect_faces(self, frame):
        # Detect faces in the provided frame
        return self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

    def classify_gender(self, face):
        # Preprocess the face for gender classification
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (104.0, 177.0, 123.0), swapRB=False)
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = self.GENDER_LIST[gender_preds[0].argmax()]
        return gender