import cv2
import time
from video_processor.video_capture import VideoCapture
from text_to_speech.text_to_speech import TextToSpeech
from object_detection.object_detector import ObjectDetector
from threading import Thread


class MayaApp:
    def __init__(self, model_path):
        self.object_detector = ObjectDetector(model_path)
        self.tts = TextToSpeech()
        self.video_capture = VideoCapture(0, width=640, height=480, fps=15)  # Initialize once
        self.frame_count = 0
        self.cooldown_duration = 5  # Cooldown duration in seconds
        self.last_spoken_time = 0
        self.last_spoken_text = None
        self.excluded_class = ["toilet"]
        self.week_classes = ["person", "cat", "donut", "pizza", "spoon"]
        self.last_spoken_count = 0
        self.stop_flag = False
        self.detection_thread = Thread(target=self._process_detection, daemon=True)

    def run(self):
        """Start the camera and detection in separate threads."""
        self.detection_thread.start()

        while not self.stop_flag:
            frame = self.video_capture.get_frame()
            if frame is None:
                print("Warning: No frame received from video capture.")
                time.sleep(0.1)
                continue

            cv2.imshow("YOLOv8 Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_flag = True
                break

            self.frame_count += 1

        self.cleanup()

    def _process_detection(self):
        """Run object detection and handle TTS in the background."""
        while not self.stop_flag:
            frame = self.video_capture.get_frame()
            if frame is None:
                print("Warning: No frame received in detection thread.")
                time.sleep(0.1)
                continue

            if self.frame_count % self.object_detector.frame_skip == 0:
                detected_classes = self.object_detector.detect_objects(frame)
                for class_name, conf in detected_classes:
                    if class_name in self.excluded_class:
                        continue

                    if conf >= 0.75 and self.last_spoken_count < 10:
                        current_time = time.time()

                        # Speak only if cooldown period is over
                        if current_time - self.last_spoken_time >= self.cooldown_duration:
                            self.tts.speak(class_name)  # Queue speech for processing
                            self.last_spoken_time = current_time  # Update the cooldown timer
                            self.last_spoken_text = class_name

            time.sleep(0.1)  # Reduce CPU usage by adding a small delay

    def cleanup(self):
        """Release resources when stopping the app."""
        self.video_capture.release()
        self.tts.stop()
        cv2.destroyAllWindows()
