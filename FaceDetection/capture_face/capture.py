import cv2

class CaptureModule:
    def __init__(self, camera_index=0, static_box_start=(150, 100), static_box_end=(450, 400)):
        self.video_capture = cv2.VideoCapture(camera_index)
        self.static_box_start = static_box_start
        self.static_box_end = static_box_end

    def get_frame(self):
        ret, frame = self.video_capture.read()
        return frame

    def display_frame(self, frame):
        cv2.imshow('Video', frame)

    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

    def draw_static_box(self, frame):
        cv2.rectangle(frame, self.static_box_start, self.static_box_end, (0, 255, 0), 2)

    def is_inside_static_box(self, left, top, right, bottom):
        return (left > self.static_box_start[0] and right < self.static_box_end[0] and
                top > self.static_box_start[1] and bottom < self.static_box_end[1])
