import pyttsx3
import feedparser

# Function to fetch news from the New York Times RSS feed
def get_nyt_news():
    url = "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
    feed = feedparser.parse(url)
    
    # Extract titles of the first 5 news articles
    headlines = []
    for entry in feed.entries[:5]:  # Adjust the number to get more headlines if needed
        headlines.append(entry.title)
    
    return headlines

# Function to speak the news headlines
def speak_news(news):
    engine = pyttsx3.init()
    for headline in news:
        print(f"Breaking News: {headline}")
        engine.say(f"Breaking news: {headline}")
    engine.runAndWait()

# Get and speak the New York Times breaking news
news = get_nyt_news()
if news:
    speak_news(news)
else:
    print("No news to speak.")
