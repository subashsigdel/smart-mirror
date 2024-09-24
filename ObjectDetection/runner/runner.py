import cv2
import time
from video_processor.video_capture import VideoCapture
from text_to_speech.text_to_speech import TextToSpeech
from object_detection.object_detector import ObjectDetector
from gender_classification.gender_classification import GenderDetector


class MayaApp:
    def __init__(self, model_path):
        self.object_detector = ObjectDetector(model_path)
        self.tts = TextToSpeech()
        self.video_capture = VideoCapture(2)
        self.frame_count = 0
        self.cooldown_duration = 5
        self.last_spoken_time = 0
        self.last_spoken_text = None
        self.excluded_class = ["toilet"]
        self.week_classe = ["person", "cat", "donut", "pizza", "spoon"]
        self.sleep_time = None
        self.last_spoken_count: int = 0
        self.gender_detector = GenderDetector()
        self.gender_confidence_threshold = 0.8
        self.is_speaking = False

    def run(self):
        while True:
            frame = self.video_capture.get_frame()
            if frame is None:
                break

            # if self.is_speaking:
            #     continue

            if self.frame_count % self.object_detector.frame_skip == 0:
                detected_classes = self.object_detector.detect_objects(frame)
                for class_name, conf in detected_classes:
                    if class_name in self.excluded_class:
                        continue
                    class_name = "monitor" if class_name == "tv" else class_name

                    if conf >= 0.75 and self.last_spoken_count < 10:
                        if self.last_spoken_text == class_name:
                            self.last_spoken_count += 1

                        if class_name == "person":
                            faces = self.gender_detector.detect_faces(frame)
                            for (x, y, w, h) in faces:
                                face_region = frame[y:y + h, x:x + w]
                                gender, confidence = self.gender_detector.detect_gender(face_region)

                                if confidence >= self.gender_confidence_threshold:
                                    class_name = gender
                                else:
                                    class_name = "person"

                        current_time = time.time()
                        if current_time - self.last_spoken_time >= self.cooldown_duration:
                            self.is_speaking = True  # Set flag to avoid processing during speech
                            self.tts.speak(class_name)
                            self.last_spoken_time = current_time
                            self.last_spoken_text = class_name
                            self.is_speaking = False  # Reset flag after speaking

            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.frame_count += 1

        self.cleanup()

    def cleanup(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
