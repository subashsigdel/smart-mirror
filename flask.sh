import time
import pygame
import feedparser
from gtts import gTTS

# Function to fetch news from the New York Times RSS feed
def get_nyt_news():
    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    feed = feedparser.parse(url)
    
    # Extract titles of the first 5 news articles
    headlines = []
    for entry in feed.entries[:5]:  # Adjust the number to get more headlines if needed
        headlines.append(entry.title)
    
    return headlines

# Function to speak the news headlines using gTTS
def speak_news(news):
    audio_file = "output.mp3"
    try:
        # Start timing text-to-speech
        start_tts_time = time.time()

        # Initialize pygame mixer
        pygame.mixer.init()

        # Loop through the news headlines and generate speech
        for headline in news:
            print(f"Breaking News: {headline}")

            # Generate the speech file for each headline
            tts = gTTS(text=f"Breaking news: {headline}", lang='en', slow=False)
            tts.save(audio_file)

            # Load and play the audio file asynchronously
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Wait until the audio finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

        # End timing for text-to-speech
        end_tts_time = time.time()
        print(f"Text-to-speech took {end_tts_time - start_tts_time:.2f} seconds.")

    except Exception as e:
        print(f"Error during text-to-speech: {e}")

# Get and speak the New York Times breaking news
news = get_nyt_news()
if news:
    speak_news(news)
else:
    print("No news to speak.")
