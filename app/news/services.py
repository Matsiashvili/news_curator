import requests

from flask import current_app


class BaseAPIService:
    """
    Base service class for external API requests.

    NewsService inherits from this class, demonstrating
    object-oriented inheritance.
    """

    def get(self, url, params=None):
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()


class NewsService(BaseAPIService):
    """
    Service responsible for communication with NewsAPI.
    """

    BASE_URL = "https://newsapi.org/v2"
    PAGE_SIZE = 15
    MAX_SOURCES = 20

    def __init__(self):
        self.api_key = current_app.config.get(
            "NEWS_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "NEWS_API_KEY is missing from the application configuration."
            )

    def get_sources(
        self,
        country="us",
        category=None
    ):
        """
        Retrieve available NewsAPI sources for a selected
        country and category.
        """

        url = f"{self.BASE_URL}/top-headlines/sources"

        params = {
            "apiKey": self.api_key,
            "language": "en"
        }

        if country:
            params["country"] = country

        if category:
            params["category"] = category

        return self.get(
            url,
            params=params
        )

    def get_headlines(
        self,
        country="us",
        category=None,
        source=None,
        page=1
    ):
        """
        Retrieve top headlines.

        This method satisfies the requirement to download news
        by country and category.
        """

        url = f"{self.BASE_URL}/top-headlines"

        params = {
            "apiKey": self.api_key,
            "page": page,
            "pageSize": self.PAGE_SIZE
        }

        if source:
            # NewsAPI does not allow sources to be combined
            # with country or category.
            params["sources"] = source

        else:
            params["country"] = country

            if category:
                params["category"] = category

        return self.get(
            url,
            params=params
        )

    def get_news_feed(
        self,
        country="us",
        category=None,
        source=None,
        page=1
    ):
        """
        Retrieve a longer paginated news feed through
        NewsAPI's /everything endpoint.

        If a source is selected, articles are retrieved directly
        from that source.

        Otherwise, matching sources are first discovered using
        the selected country and category.
        """

        url = f"{self.BASE_URL}/everything"

        params = {
            "apiKey": self.api_key,
            "page": page,
            "pageSize": self.PAGE_SIZE,
            "language": "en",
            "sortBy": "publishedAt"
        }

        if source:
            params["sources"] = source

        else:
            source_response = self.get_sources(
                country=country,
                category=category
            )

            source_ids = []

            for source_item in source_response.get(
                "sources",
                []
            ):
                source_id = source_item.get("id")

                if source_id:
                    source_ids.append(source_id)

            # NewsAPI allows up to 20 sources in one request.
            source_ids = source_ids[:self.MAX_SOURCES]

            if source_ids:
                params["sources"] = ",".join(
                    source_ids
                )

            else:
                # Fallback if no matching registered sources
                # were found for the selected filters.
                category_queries = {
                    "business": "business OR economy OR finance",
                    "entertainment": "entertainment OR movies OR music",
                    "general": "world OR politics OR current events",
                    "health": "health OR medicine OR healthcare",
                    "science": "science OR research OR space",
                    "sports": "sports OR football OR basketball",
                    "technology": "technology OR software OR artificial intelligence"
                }

                params["q"] = category_queries.get(
                    category,
                    (
                        "world OR business OR technology "
                        "OR science OR sports"
                    )
                )

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
        """
        Search articles using NewsAPI's /everything endpoint.
        """

        url = f"{self.BASE_URL}/everything"

        params = {
            "apiKey": self.api_key,
            "q": query,
            "page": page,
            "pageSize": self.PAGE_SIZE,
            "language": "en",
            "sortBy": "publishedAt"
        }

        if source:
            params["sources"] = source

        return self.get(
            url,
            params=params
        )