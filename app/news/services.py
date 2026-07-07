import requests

from flask import current_app


class BaseAPIService:
    """
    Base class for API services.
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
    NewsAPI service.
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
        page=1
    ):

        url = f"{self.BASE_URL}/top-headlines"


        params = {
            "apiKey": self.api_key,
            "country": country,
            "category": category,
            "page": page,
        }

        params = {k: v for k, v in params.items() if v is not None}

        return self.get(url, params=params)