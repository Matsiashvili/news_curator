from flask import (
    Blueprint,
    render_template,
    request,
    session
)

from .services import NewsService
from app.models import User, ReadingList


news_bp = Blueprint(
    "news",
    __name__,
    url_prefix="/news"
)


@news_bp.route("/")
def index():

    user = None
    reading_lists = []

    if session.get("user_id"):
        user = User.query.get(session["user_id"])

    reading_lists = ReadingList.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        ReadingList.created_at.desc()
    ).all()
    category = request.args.get(
        "category"
    )

    country = request.args.get(
        "country"
    )

    source = request.args.get(
        "source"
    )

    query = request.args.get(
        "q"
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if user:

        if not country:
            country = user.country or "us"

        if not category and user.preferred_categories and not query and not source:

            preferred_categories = user.preferred_categories.split(",")

            if preferred_categories:
                category = preferred_categories[0]

    if not country:
        country = "us"

    service = NewsService()

    if query:
        news = service.search_articles(
            query=query,
            page=page,
            source=source
        )
    else:
        news = service.get_headlines(
            country=country,
            category=category,
            source=source,
            page=page
        )

    articles = news.get(
        "articles",
        []
    )

    total_results = news.get(
        "totalResults",
        0
    )

    sources = [
        ("", "All Sources"),
        ("bbc-news", "BBC News"),
        ("cnn", "CNN"),
        ("reuters", "Reuters"),
        ("the-verge", "The Verge"),
        ("techcrunch", "TechCrunch"),
        ("espn", "ESPN")
    ]

    return render_template(
        "news/index.html",
        articles=articles,
        category=category,
        country=country,
        source=source,
        query=query,
        page=page,
        total_results=total_results,
        sources=sources,
        reading_lists=reading_lists
    )