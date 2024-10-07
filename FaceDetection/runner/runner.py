# runner/runner.py

from capture_face.capture import FaceCapture
from speech_recognizer.speech_recognition import SpeechRecognizer
import cv2


class Runner:
    def __init__(self):
        self.face_capture = FaceCapture()
        self.speech_recognizer = SpeechRecognizer()

    def run(self):
        # Initialize video capture
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Failed to capture video")
                break

            # Process frame for face recognition
            recognized_name = self.face_capture.process_frame(frame)

            if recognized_name:
                self.speech_recognizer.greet_person(recognized_name)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    runner = Runner()
    runner.run()
