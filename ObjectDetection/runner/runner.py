import cv2
import time
from video_processor.video_capture import VideoCapture
from text_to_speech.text_to_speech import TextToSpeech
from object_detection.object_detector import ObjectDetector


class MayaApp:
    def __init__(self, model_path):
        self.object_detector = ObjectDetector(model_path)
        self.tts = TextToSpeech()
        self.video_capture = VideoCapture()
        self.frame_count = 0
        self.cooldown_duration = 5
        self.last_spoken_time = 0
        self.last_spoken_text = None

    def run(self):
        while True:
            frame = self.video_capture.get_frame()
            if frame is None:
                break

            if self.frame_count % self.object_detector.frame_skip == 0:
                detected_classes = self.object_detector.detect_objects(frame)
                for class_name, conf in detected_classes:
                    if conf >= 0.5 and class_name != self.last_spoken_text:
                        current_time = time.time()
                        if current_time - self.last_spoken_time >= self.cooldown_duration:
                            self.tts.speak(class_name, conf)
                            self.last_spoken_time = current_time
                            self.last_spoken_text = class_name

            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.frame_count += 1

        self.cleanup()

    def cleanup(self):
        self.video_capture.release()
        cv2.destroyAllWindows()
