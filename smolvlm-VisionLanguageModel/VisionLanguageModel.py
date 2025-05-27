import cv2
import requests
import base64
import time
import threading
from SpeechToText import TTS  # Ensure TTS works correctly

# === Configuration ===
SERVER_URL = "http://localhost:9090/v1/chat/completions"
INSTRUCTION = "What do you see?"
INTERVAL_SECONDS = 5  # Time between photo captures

# === Webcam Setup ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

# === Global States ===
last_request_time = 0
processing = False
speaking = False 

status_message = "Idle"

# === Speak response using TTS ===
def speak_response(text):
    global status_message, speaking
    try:
        speaking = True
        status_message = "Speaking..."
        TTS(text=text, lang='en', filename='temp_output.mp3')
    except Exception as e:
        print("TTS failed:", e)
    finally:
        speaking = False
        status_message = "Idle"

# === Process image and send to vision-language model ===
def process_frame(frame):
    global processing, status_message
    processing = True
    status_message = "Encoding image..."

    try:
        _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        image_base64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
        image_data_url = f"data:image/jpeg;base64,{image_base64}"
    except Exception as e:
        print("Image encoding failed:", e)
        processing = False
        status_message = "Idle"
        return

    payload = {
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": INSTRUCTION},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]
    }

    try:
        status_message = "Sending to API..."
        response = requests.post(SERVER_URL, headers={"Content-Type": "application/json"}, json=payload)
        if response.ok:
            answer = response.json()["choices"][0]["message"]["content"]
            print("Response:", answer)

            status_message = "Received response"
            tts_thread = threading.Thread(target=speak_response, args=(answer,), daemon=True)
            tts_thread.start()
        else:
            print(f"API Error {response.status_code}: {response.text}")
            status_message = f"API error: {response.status_code}"
    except Exception as e:
        print("Request failed:", e)
        status_message = "Request failed"

    processing = False

# === Main Loop ===
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            continue

        # Show live feed with status
        cv2.putText(frame, f"Status: {status_message}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow('SmolVLM Detection', frame)

        current_time = time.time()
        should_capture =(current_time - last_request_time >= INTERVAL_SECONDS and not processing and not speaking)

        if should_capture:
            last_request_time = current_time

            # === Countdown with live video feed ===
            for countdown_text in ["Be ready...", "3", "2", "1"]:
                ret, frame = cap.read()
                if not ret:
                    continue
                font_scale = 1.5 if countdown_text == "Be ready..." else 4.0
                thickness = 2 if countdown_text == "Be ready..." else 5
                cv2.putText(frame, countdown_text, (100, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)
                cv2.imshow('SmolVLM Detection', frame)
                cv2.waitKey(1000)

            print("Capturing now!")

            # === Flush camera buffer to get fresh frame ===
            for _ in range(5):
                cap.read()
                time.sleep(0.05)

            ret, final_frame = cap.read()
            if ret:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"captured_{timestamp}.jpg"
                cv2.imwrite(filename, final_frame)
                print(f"Saved image as: {filename}")

                # Start async processing
                thread = threading.Thread(target=process_frame, args=(final_frame.copy(),), daemon=True)
                thread.start()
            else:
                print("Failed to capture final frame.")

        # Break on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Camera closed.")
