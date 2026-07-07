print("NEWS ROUTES LOADED")

from flask import (
    Blueprint,
    render_template,
    request
)

from .services import NewsService


news_bp = Blueprint(
    "news",
    __name__,
    url_prefix="/news"
)


@news_bp.route("/")
def index():

    category = request.args.get(
        "category"
    )

    country = request.args.get(
        "country",
        "us"
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )


    service = NewsService()


    news = service.get_headlines(
        country=country,
        category=category,
        page=page
    )

    articles = news.get(
        "articles",
        []
    )

    print("====================")
    print(news)
    print("ARTICLE COUNT:", len(articles))
    print("====================")

    return render_template(
        "news/index.html",
        articles=articles,
        category=category,
        country=country,
        page=page
    )