import cv2
from new_person import newperson
from speech_recognizer.speech_recognition import SpeechModule
from face_recognition.face_recognition import FaceRecognition
from capture_face.capture import CaptureModule


class MainRunner:
    def __init__(self):
        self.face_recognition = FaceRecognition()
        self.speech_module = SpeechModule()
        self.capture_module = CaptureModule()
        self.greeted_names = set()  # To track greeted names
        self.process_this_frame = True  # Process every other frame

    def run(self):
        while True:
            frame = self.capture_module.get_frame()

            # Draw static bounding box on frame
            self.capture_module.draw_static_box(frame)

            if self.process_this_frame:
                face_locations, face_names = self.face_recognition.recognize_faces(frame)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top, right, bottom, left = [v * 4 for v in (top, right, bottom, left)]

                    if name == "Unknown" and self.capture_module.is_inside_static_box(left, top, right, bottom):
                        newperson(frame)  # Capture image for new person
                        self.face_recognition.update_encodings('testimage')  # Update with new face encodings

                    if name != "Unknown" and name not in self.greeted_names:
                        self.speech_module.greet_person(name)
                        self.greeted_names.add(name)

                    # Draw face box and name on the frame
                    self.draw_face_box(frame, top, right, bottom, left, name)

            self.process_this_frame = not self.process_this_frame
            self.capture_module.display_frame(frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture_module.release()

    @staticmethod
    def draw_face_box(frame, top, right, bottom, left, name):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


