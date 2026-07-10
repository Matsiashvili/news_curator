from math import ceil

from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    session
)

from .services import NewsService
from app.models import User, ReadingList
from app.reading_lists.services import ReadingListService


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
        user = User.query.get(
            session["user_id"]
        )

        ReadingListService.get_or_create_default_list(
            session["user_id"]
        )

        all_lists = ReadingList.query.filter_by(
            user_id=session["user_id"]
        ).order_by(
            ReadingList.created_at.asc()
        ).all()

        seen_names = set()

        for reading_list in all_lists:
            clean_name = (
                reading_list.name
                .strip()
                .lower()
            )

            if clean_name not in seen_names:
                reading_lists.append(
                    reading_list
                )

                seen_names.add(
                    clean_name
                )

    category = request.args.get(
        "category",
        ""
    ).strip()

    country = request.args.get(
        "country",
        ""
    ).strip()

    source = request.args.get(
        "source",
        ""
    ).strip()

    query = request.args.get(
        "q",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    if user:
        if not country:
            country = user.country or "us"

        # Use the first preferred category only when the user
        # has not manually selected a category or search.
        if (
            not category
            and user.preferred_categories
            and not query
            and not source
        ):
            preferred_categories = [
                item.strip()
                for item in (
                    user.preferred_categories.split(",")
                )
                if item.strip()
            ]

            if preferred_categories:
                category = preferred_categories[0]

    if not country:
        country = "us"

    service = NewsService()

    try:
        if query:
            news = service.search_articles(
                query=query,
                page=page,
                source=source or None
            )

        else:
            # This produces a much longer feed than
            # /top-headlines alone.
            news = service.get_news_feed(
                country=country,
                category=category or None,
                source=source or None,
                page=page
            )

    except Exception as error:
        flash(
            f"News could not be loaded: {error}",
            "danger"
        )

        news = {
            "articles": [],
            "totalResults": 0
        }

    articles = news.get(
        "articles",
        []
    )

    total_results = news.get(
        "totalResults",
        0
    )

    try:
        total_results = int(
            total_results
        )

    except (TypeError, ValueError):
        total_results = 0

    if total_results > 0:
        total_pages = ceil(
            total_results / service.PAGE_SIZE
        )

    else:
        total_pages = 1

    # Prevent showing invalid page numbers.
    if total_pages < 1:
        total_pages = 1

    start_page = max(
        1,
        page - 2
    )

    end_page = min(
        total_pages,
        page + 2
    )

    page_numbers = list(
        range(
            start_page,
            end_page + 1
        )
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
        total_pages=total_pages,
        page_numbers=page_numbers,
        total_results=total_results,
        sources=sources,
        reading_lists=reading_lists
    )