from threading import Lock, Thread
from queue import Queue
from gtts import gTTS
from playsound import playsound
import os
import time
import tempfile


class TextToSpeech:
    def __init__(self):
        self.last_class_spoken = None
        self.speak_lock = Lock()
        self.speak_cooldown = 10  # Cooldown period in seconds
        self.last_spoken_time = 0
        self.queue = Queue()
        self._initialize_background_worker()

    def _initialize_background_worker(self):
        """Start background thread to process TTS requests."""
        Thread(target=self._process_queue, daemon=True).start()

    def speak(self, text):
        """Enqueue text for speech synthesis if cooldown period has passed."""
        current_time = time.time()
        if current_time - self.last_spoken_time >= self.speak_cooldown:
            self.queue.put(text)
        else:
            print(f"Skipping '{text}', still in cooldown.")

    def _process_queue(self):
        """Process the TTS queue and handle text-to-speech generation."""
        while True:
            text = self.queue.get()
            if text is None:
                break
            with self.speak_lock:
                self._generate_and_play_audio(text)
            self.queue.task_done()

    def _generate_and_play_audio(self, text):
        """Generate audio file from text and play it."""
        try:
            # Generate a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
                audio_file = temp_audio.name
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(audio_file)
                playsound(audio_file)

            self.last_class_spoken = text
            self.last_spoken_time = time.time()  # Update the last spoken time

        except Exception as e:
            print(f"Error in speech synthesis: {e}")
        finally:
            self._cleanup_audio_file(audio_file)

    def _cleanup_audio_file(self, file_path):
        """Delete the audio file after it's played."""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting audio file {file_path}: {e}")

    def stop(self):
        """Stop the background TTS processing thread."""
        self.queue.put(None)
