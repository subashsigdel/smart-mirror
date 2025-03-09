import os
import time
import requests

MAGICMIRROR_URL = "http://localhost:8080/api/newsfeed"

def get_latest_news():
    try:
        response = requests.get(MAGICMIRROR_URL)
        news_data = response.json()
        if news_data and "items" in news_data and len(news_data["items"]) > 0:
            return news_data["items"][0]["title"]  # Get the first news headline
    except Exception as e:
        print("Error fetching news:", e)
    return None

def speak_news(news):
    if news:
        print("Speaking:", news)
        os.system(f'espeak "{news}" --stdout | aplay')

if __name__ == "__main__":
    spoken_news = None  # To keep track of already spoken news
    while True:
        latest_news = get_latest_news()
        if latest_news and latest_news != spoken_news:
            speak_news(latest_news)
            spoken_news = latest_news  # Store spoken news

        time.sleep(600)  # Wait 10 minutes before checking again
