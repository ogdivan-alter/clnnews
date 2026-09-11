"""NewsAPI news source."""

import logging

import requests

from ..config import settings
from ..core.exceptions import APIError
from ..core.models import Article
from . import NewsSource


class NewsAPI(NewsSource):
    """News source for NewsAPI."""

    BASE_URL = "https://api.thenewsapi.com/v1/news/all"

    def __init__(self):
        self.api_key = settings.newsapi_api_key

    def fetch_articles(self, query: str):
        """Fetch articles from NewsAPI."""
        logger = logging.getLogger(__name__)
        logger.debug(f"Fetching articles from NewsAPI for query: {query}")

        params = {
            "search": query,
            "api_token": self.api_key,
            "limit": settings.max_articles,
            "language": "es",
        }
        try:
            logger.debug("Making request to NewsAPI")
            response = requests.get(
                self.BASE_URL, params=params, timeout=settings.request_timeout
            )
            print(f"Request URL: {response.request.url}")

            response.raise_for_status()
            data = response.json()
            articles = [
                Article(
                    title=article.get("title", ""),
                    description=article.get("description", ""),
                    url=article.get("url", ""),
                )
                for article in data.get("data", [])
            ]
            logger.info(f"Retrieved {len(articles)} articles from NewsAPI")
            return articles
        except requests.RequestException as e:
            logger.error(f"Failed to fetch articles from NewsAPI: {e}")
            msg = f"Error al obtener artículos de NewsAPI: {e}. Verifique su conexión \
                a internet y la clave de API de NewsAPI."
            raise APIError(msg) from e
