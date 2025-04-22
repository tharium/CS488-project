import os
import requests

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