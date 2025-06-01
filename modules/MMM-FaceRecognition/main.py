import time
import cv2
import numpy as np
import threading
import queue
from typing import List, Set, Tuple
from Load_Face_Encoding import load_face_encodings_from_csv
from Face_Detect import process_batch

# === CONFIGURATION ===
CSV_FILEPATH = "face_encodings.csv"
BATCH_SIZE = 3
RESET_INTERVAL = 180  # seconds

STATIC_BOX_START: Tuple[int, int] = (150, 100)
STATIC_BOX_END: Tuple[int, int] = (450, 400)

# === THREADING UTILITIES ===
frame_queue = queue.Queue(maxsize=10)
batch_queue = queue.Queue(maxsize=5)
stop_event = threading.Event()

# === LOAD ENCODINGS ===
known_face_embeddings, known_face_names = load_face_encodings_from_csv(csv_filename=CSV_FILEPATH)

# === CAMERA THREAD ===
def camera_thread_func(cap):
    last_time = time.time()
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            continue

        # Optional: Resize for performance
        frame = cv2.resize(frame, (640, 480))

        # Draw static box
        cv2.rectangle(frame, STATIC_BOX_START, STATIC_BOX_END, (0, 255, 0), 2)
        roi = frame[STATIC_BOX_START[1]:STATIC_BOX_END[1], STATIC_BOX_START[0]:STATIC_BOX_END[0]]

        # Drop frame if queue is full
        if not frame_queue.full():
            frame_queue.put((frame.copy(), roi.copy()))
        else:
            print("[INFO] Dropped frame to maintain FPS")

        # Throttle to ~30 FPS
        time.sleep(max(0, 1/30 - (time.time() - last_time)))
        last_time = time.time()

# === BATCH PROCESSING THREAD ===
def batch_worker(greeted_names):
    while not stop_event.is_set():
        try:
            batch = batch_queue.get(timeout=1)
            process_batch(batch, greeted_names, known_face_embeddings, known_face_names)
        except queue.Empty:
            continue

# === MAIN APPLICATION ===
def main():
    greeted_names: Set[str] = set()
    last_reset_time = time.time()
    frame_batch: List[np.ndarray] = []

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("[ERROR] Cannot access webcam.")
        return

    # Start camera and processing threads
    cam_thread = threading.Thread(target=camera_thread_func, args=(cap,))
    batch_thread = threading.Thread(target=batch_worker, args=(greeted_names,))
    cam_thread.start()
    batch_thread.start()

    try:
        while True:
            # Reset greeted names every few minutes
            current_time = time.time()
            if current_time - last_reset_time >= RESET_INTERVAL:
                greeted_names.clear()
                last_reset_time = current_time
                print("[INFO] Greeting list reset.")

            # Get frame from queue if available
            if not frame_queue.empty():
                frame, roi = frame_queue.get()
                frame_batch.append(roi)

                # Process batch if full
                if len(frame_batch) == BATCH_SIZE:
                    if not batch_queue.full():
                        batch_queue.put(frame_batch.copy())
                    frame_batch.clear()

                # Show current frame
                cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
                print("[INFO] Exiting...")
                break

    finally:
        stop_event.set()
        cam_thread.join()
        batch_thread.join()
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Threads stopped, camera released.")

if __name__ == "__main__":
    main()
