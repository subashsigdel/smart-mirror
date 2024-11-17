import cv2
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self, model_path, confidence_threshold=0.5, frame_skip=5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.frame_skip = frame_skip

    def detect_objects(self, frame):
        results = self.model(frame)
        detected_classes = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = box.cls[0]
                class_name = self.model.names[int(cls)]

                if conf >= self.confidence_threshold:
                    detected_classes.append((class_name, conf))
                    self._draw_detection(frame, (x1, y1, x2, y2), class_name, conf)

        return detected_classes

    @staticmethod
    def _draw_detection(frame, box, class_name, conf):
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        label = f"{class_name}: {conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
