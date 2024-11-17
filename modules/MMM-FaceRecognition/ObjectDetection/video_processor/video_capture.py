import cv2

class VideoCapture:
    def __init__(self, source=0, width=640, height=480, fps=15):
        self.capture = cv2.VideoCapture(source)
        # Set video resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # Set frame rate
        self.capture.set(cv2.CAP_PROP_FPS, fps)

        if not self.capture.isOpened():
            raise ValueError(f"Error: Cannot open video source {source}")

    def get_frame(self):
        ret, frame = self.capture.read()
        return frame if ret else None

    def release(self):
        self.capture.release()
