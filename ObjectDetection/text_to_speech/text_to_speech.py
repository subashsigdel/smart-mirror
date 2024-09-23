from threading import Lock, Thread
from queue import Queue
from gtts import gTTS
from playsound import playsound
import os
import time


class TextToSpeech:
    def __init__(self):
        self.last_class_spoken = None
        self.audio_file = "output.mp3"
        self.speak_lock = Lock()
        self.speak_cooldown = 10
        self.last_spoken_time = 0
        self.queue = Queue()
        self._initialize_background_worker()

    def _initialize_background_worker(self):
        Thread(target=self._process_queue, daemon=True).start()

    def speak(self, text):
        self.queue.put(text)

    def _process_queue(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            with self.speak_lock:
                self._generate_and_play_audio(text)
            self.queue.task_done()

    def _generate_and_play_audio(self, text):
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(self.audio_file)
            playsound(self.audio_file)
            self.last_class_spoken = text
            self.last_spoken_time = time.time()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
        finally:
            self._cleanup_audio_file()

    def _cleanup_audio_file(self):
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)

    def stop(self):
        self.queue.put(None)
