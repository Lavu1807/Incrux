"""
Phase 1: Fetch Latest News
This module handles fetching news articles from NewsAPI.
"""

import requests
from typing import List, Dict
from config import Config


def fetch_news(topic: str = None, max_articles: int = None) -> List[Dict[str, str]]:
    """
    Fetch latest news articles for a given topic from NewsAPI.
    
    Args:
        topic (str): The news topic to search for. Defaults to NEWS_TOPIC from config.
        max_articles (int): Maximum number of articles to fetch. Defaults to MAX_ARTICLES from config.
    
    Returns:
        List[Dict]: List of articles with keys: title, description, url, source
    
    Raises:
        requests.exceptions.RequestException: If API request fails.
        ValueError: If API response contains an error.
    """
    
    topic = topic or Config.NEWS_TOPIC
    max_articles = max_articles or Config.MAX_ARTICLES
    
    # Prepare request parameters
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_articles,
        "apiKey": Config.NEWS_API_KEY
    }
    
    try:
        print(f"📡 Fetching news for: {topic}...")
        response = requests.get(Config.NEWS_API_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        
        # Check for API errors
        if data.get("status") != "ok":
            raise ValueError(f"NewsAPI error: {data.get('message', 'Unknown error')}")
        
        articles = data.get("articles", [])
        
        if not articles:
            print(f"⚠️  No articles found for topic: {topic}")
            return []
        
        # Clean and structure articles
        cleaned_articles = []
        for article in articles:
            cleaned_article = {
                "title": article.get("title", "N/A"),
                "description": article.get("description", "N/A"),
                "url": article.get("url", "#"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "publishedAt": article.get("publishedAt", "N/A")
            }
            cleaned_articles.append(cleaned_article)
        
        print(f"✓ Successfully fetched {len(cleaned_articles)} articles")
        return cleaned_articles
    
    except requests.exceptions.Timeout:
        print("✗ Error: Request timeout. Check your internet connection.")
        return []
    except requests.exceptions.ConnectionError:
        print("✗ Error: Connection failed. Check your internet connection.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e.response.status_code}")
        if e.response.status_code == 401:
            print("  → Invalid API key. Please check your NEWS_API_KEY in .env")
        elif e.response.status_code == 429:
            print("  → Rate limit exceeded. Please try again later.")
        return []
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        return []


def print_articles(articles: List[Dict[str, str]]) -> None:
    """
    Pretty print articles for debugging.
    
    Args:
        articles (List[Dict]): List of articles to print.
    """
    if not articles:
        print("No articles to display.")
        return
    
    for idx, article in enumerate(articles, 1):
        print(f"\n📰 Article {idx}: {article.get('title')}")
        print(f"   Source: {article.get('source')}")
        print(f"   Description: {article.get('description')[:100]}...")
        print(f"   URL: {article.get('url')}")


if __name__ == "__main__":
    # Test the fetch_news function
    articles = fetch_news(topic="Indian Startups", max_articles=5)
    print_articles(articles)
