import cv2


class VideoCapture:
    def __init__(self, source=0):
        self.capture = cv2.VideoCapture(source)

    def get_frame(self):
        ret, frame = self.capture.read()
        return frame if ret else None

    def release(self):
        self.capture.release()
