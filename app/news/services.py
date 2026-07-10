import requests

from flask import current_app


class BaseAPIService:
    """
    Base service class for external API requests.
    This demonstrates inheritance.
    """

    def get(self, url, params=None):

        response = requests.get(
            url,
            params=params
        )

        response.raise_for_status()

        return response.json()


class NewsService(BaseAPIService):
    """
    Service for communicating with NewsAPI.
    """

    BASE_URL = "https://newsapi.org/v2"

    def __init__(self):

        self.api_key = current_app.config.get(
            "NEWS_API_KEY"
        )

    def get_headlines(
        self,
        country="us",
        category=None,
        source=None,
        page=1
    ):

        url = f"{self.BASE_URL}/top-headlines"

        params = {
            "apiKey": self.api_key,
            "page": page,
            "pageSize": 15
        }

        if source:
            params["sources"] = source
        else:
            params["country"] = country

            if category:
                params["category"] = category

        return self.get(
            url,
            params=params
        )

    def search_articles(
        self,
        query,
        page=1,
        source=None
    ):

        url = f"{self.BASE_URL}/everything"

        params = {
            "apiKey": self.api_key,
            "q": query,
            "page": page,
            "pageSize": 15,
            "language": "en",
            "sortBy": "publishedAt"
        }

        if source:
            params["sources"] = source

        return self.get(
            url,
            params=params
        )