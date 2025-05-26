import time
import pygame
import feedparser
from gtts import gTTS

# RSS Feed URL from Magic Mirror config
RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

# Function to fetch news from RSS
def get_nyt_news():
    try:
        feed = feedparser.parse(RSS_URL)
        if not feed.entries:
            print("No news found.")
            return []
        
        return [entry.title for entry in feed.entries[:5]]  # Fetch top 5 headlines
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# Function to speak the news
def speak_news(news):
    audio_file = "breakingnews.mp3"
    try:
        pygame.mixer.init()
        for headline in news:
            print(f"Breaking News: {headline}")

            # Convert text to speech and save as MP3
            tts = gTTS(text=f"Breaking news: {headline}", lang='en', slow=False)
            tts.save(audio_file)

            # Play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Wait until the audio finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

    except Exception as e:
        print(f"Error during text-to-speech: {e}")

# Fetch and speak the news
news = get_nyt_news()
if news:
    speak_news(news)
else:
    print("No news to speak.")


def process_batch(
    frames: List[np.ndarray],
    greeted_names: Set[str],
    known_face_encodings: List[np.ndarray],
    known_face_names: List[str],
) -> None:
    """Processes a batch of frames for face recognition and greeting."""
    for frame in frames:
        small_frame: np.ndarray = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame: np.ndarray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Start timing face recognition
        start_recognition_time = time.time()

        face_locations: List[Tuple[int, int, int, int]] = face_recognition.face_locations(rgb_small_frame)
        face_encodings: List[np.ndarray] = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_location = [v * 4 for v in face_location]  # Scale back to original size
            matches: List[bool] = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances: np.ndarray = face_recognition.face_distance(known_face_encodings, face_encoding)
            print("known face encoding:",known_face_encodings)
            print("current face encoding:",face_encoding)
            name: str = "Unknown"
            confidence: float = 0.0

            if matches:
                best_match_index: int = np.argmin(face_distances)
                best_distance = face_distances[best_match_index]
                print(f"Best match index: {best_match_index}, Distance: {best_distance:.4f}")

                confidence = 1.0 - best_distance  # Convert distance to confidence score

                # Use a soft threshold on raw distance instead of confidence
                if matches[best_match_index] and best_distance < 0.39:
                    name = known_face_names[best_match_index]

            # End timing face recognition
            end_recognition_time = time.time()
            print(f"Face recognition for {name} took {end_recognition_time - start_recognition_time:.2f} seconds. Confidence: {confidence:.2f}")

            # Check bounding box and greet logic
            if (STATIC_BOX_START[0] < face_location[3] < STATIC_BOX_END[0] and
                    STATIC_BOX_START[1] < face_location[0] < STATIC_BOX_END[1]):

                if name == "Unknown":
                    append_face_encodings_to_csv(image_folder, CSV_FILENAME, processed_folder)
                    pass

                elif name not in greeted_names:
                    # Start timing greeting
                    start_greeting_time = time.time()
                    greet_person(name)
                    end_greeting_time = time.time()

                    print(f"Greeting {name} took {end_greeting_time - start_greeting_time:.2f} seconds.")
                    greeted_names.add(name)

            draw_bounding_box(frame, face_location, f"{name} ({confidence:.2f})")
