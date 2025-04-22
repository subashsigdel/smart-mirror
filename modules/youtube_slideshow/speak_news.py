import time
import os
import pygame
import feedparser
import threading
from gtts import gTTS

# RSS Feed URL from Magic Mirror config
RSS_URL = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"

# Global signals
stop_signal = False  
play_signal = False
news_updated = False

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

# Function to listen for key presses
def listen_for_keys():
    global stop_signal, play_signal
    try:
        while True:
            key = input().strip()
            if key.lower() == "q":
                stop_signal = True
                play_signal = False
                pygame.mixer.music.stop()
                print("News playback stopped.")
            elif key.lower() == "b":
                stop_signal = False
                play_signal = True
                print("News playback triggered.")
    except (EOFError, KeyboardInterrupt):
        stop_signal = True
        play_signal = False
        pygame.mixer.music.stop()
        print("Listener terminated.")

# Function to announce new news
def announce_update():
    try:
        pygame.mixer.init()
        tts = gTTS(text="New news available.", lang='en', slow=False)
        tts.save("new_update.mp3")
        pygame.mixer.music.load("new_update.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        os.remove("new_update.mp3")
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error announcing update: {e}")

# Function to speak the news
def speak_news(news):
    global stop_signal
    audio_file = "breakingnews.mp3"
    
    try:
        pygame.mixer.init()
        for headline in news:
            if stop_signal:
                break

            print(f"Breaking News: {headline}")

            # Convert text to speech and save as MP3
            tts = gTTS(text=f"Breaking news: {headline}", lang='en', slow=False)
            tts.save(audio_file)

            # Play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # Wait until the audio finishes or stop is triggered
            while pygame.mixer.music.get_busy():
                if stop_signal:
                    pygame.mixer.music.stop()
                    break
                time.sleep(0.1)

            if os.path.exists(audio_file):
                os.remove(audio_file)

    except Exception as e:
        print(f"Error during text-to-speech: {e}")
    
    finally:
        pygame.mixer.quit()

# Function to regularly check for news updates
def news_updater():
    global news_updated, latest_news
    latest_news = get_nyt_news()
    while True:
        time.sleep(60)  # Check every 60 seconds (you can make this faster)
        new_news = get_nyt_news()
        if new_news != latest_news and new_news:
            print("News updated!")
            latest_news = new_news
            news_updated = True

# Start listener for keys
listener_thread = threading.Thread(target=listen_for_keys, daemon=True)
listener_thread.start()

# Start news updater thread
updater_thread = threading.Thread(target=news_updater, daemon=True)
updater_thread.start()

# Main loop
latest_news = get_nyt_news()
if not latest_news:
    print("No news to speak.")
else:
    speak_news(latest_news)

while True:
    if play_signal:
        play_signal = False
        speak_news(latest_news)
    if news_updated:
        news_updated = False
        announce_update()
    time.sleep(0.1)
