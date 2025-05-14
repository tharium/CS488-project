import os
import requests
from insidertrading.models import newsArticle, WatchedStock

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_stock_news(query, limit=2):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": limit,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def fetch_and_store_news():
    watched_stocks = WatchedStock.objects.all()

    for watched_stock in watched_stocks:
        stock = watched_stock.stock
        news_articles = get_stock_news(stock.ticker, limit=5)
        
        for article in news_articles:
            if not newsArticle.objects.filter(title=article["title"], symbol=stock.ticker).exists():
                newsArticle.objects.create(
                    title=article["title"],
                    description=article["description"],
                    url=article["url"],
                    published_at=article["publishedAt"],
                    source=article["source"]["name"],
                    symbol=stock.ticker,
                )