import requests
import os
import dotenv
import feedparser
dotenv.load_dotenv()

webhook_url=os.getenv("DISCORD_WEBHOOK_URL")




NEWS_FEEDS = {
    "indian_news": "https://indianexpress.com/section/india/feed/",
    "technology_news": "https://feeds.bbci.co.uk/news/technology/rss.xml?",
    "international_news":"https://feeds.bbci.co.uk/news/world/rss.xml?"
}

news={}


def collect_news():
    """collects news articles from the specified RSS feeds and stores them in the news dictionary"""
    for source, url in NEWS_FEEDS.items():
        feed = feedparser.parse(url)
        category = source.replace("_news", "").capitalize()
        category_news=[]
        for entry in feed.entries[:5]:
            category_news.append({
                "title": entry.get("title"),
                "link": entry.get("link"),
                "image": entry.get("media_thumbnail", [{}])[0].get("url",None),
                "published": entry.get("published", "Unknown")
            })
        news[category] = category_news



   

collect_news()
print("Collected news articles:",news)


def send_webhook_message(category, articles):
    """send discord message to webhook with news articles"""
    embeds = []

    for article in articles:
        embed = {
            "title": article["title"],
            "url": article["link"],
            "description": f"Published: {article['published']}"
        }

        if article.get("image"):
            embed["thumbnail"] = {
                "url": article["image"]
            }

        embeds.append(embed)

    response = requests.post(
        webhook_url,
        json={
            "content": f"📰 **{category} news**",
            "embeds": embeds
        }
    )

    if response.status_code in (200, 204):
        print(f"{category} sent successfully!")
    else:
        print("Failed:", response.status_code, response.text)




for category, articles in news.items():
    send_webhook_message(
        category.replace("_", " ").title(),
        articles
    )
