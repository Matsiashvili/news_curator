from typing import Optional, List

from .base_service import BaseService
from ..extensions import db
from ..models import SavedArticle, Tag


class NewsService(BaseService):
    """
    Handles fetching news articles and saving them to a user's reading list.

    Inherits get_by_id / get_all / create / delete from BaseService and
    adds news-specific behaviour on top.
    """

    model = SavedArticle

    # In a real deployment this would call an external News API
    # (e.g. NewsAPI.org, GNews). Mocked here so the finals project runs
    # without needing an API key.
    _MOCK_ARTICLES = [
        {
            "title": "AI Research Hits New Milestone",
            "url": "https://example.com/articles/ai-milestone",
            "source": "TechDaily",
            "summary": "Researchers announce a new breakthrough in model efficiency.",
            "category": "technology",
        },
        {
            "title": "Global Markets Rally on Rate Decision",
            "url": "https://example.com/articles/markets-rally",
            "source": "FinanceWire",
            "summary": "Stocks rose after the central bank held interest rates steady.",
            "category": "business",
        },
        {
            "title": "New Study Links Sleep to Memory Retention",
            "url": "https://example.com/articles/sleep-memory-study",
            "source": "ScienceToday",
            "summary": "A new study finds a strong correlation between deep sleep and recall.",
            "category": "science",
        },
    ]

    @classmethod
    def fetch_latest(cls, category: Optional[str] = None, limit: int = 10) -> List[dict]:
        """Return the latest news articles, optionally filtered by category."""
        articles = cls._MOCK_ARTICLES
        if category:
            articles = [a for a in articles if a["category"] == category]
        return articles[:limit]

    @classmethod
    def save_article_for_user(
        cls,
        user_id: int,
        title: str,
        url: str,
        source: Optional[str] = None,
        summary: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
    ) -> SavedArticle:
        """Create a SavedArticle for a user, reusing existing tags where possible."""
        article = cls.model(
            title=title,
            url=url,
            source=source,
            summary=summary,
            user_id=user_id,
        )

        for name in tag_names or []:
            tag = Tag.query.filter_by(name=name).first()
            if tag is None:
                tag = Tag(name=name)
                db.session.add(tag)
            article.tags.append(tag)

        db.session.add(article)
        db.session.commit()
        return article
