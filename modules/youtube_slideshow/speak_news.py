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
