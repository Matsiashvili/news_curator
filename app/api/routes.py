from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from app.extensions import db
from app.models import (
    SavedArticle,
    ReadingList
)
from app.news.services import NewsService


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


def api_login_required():

    if "user_id" not in session:

        return jsonify({
            "error": "Authentication required"
        }), 401

    return None


@api_bp.route("/news", methods=["GET"])
def api_news():

    category = request.args.get("category")
    country = request.args.get("country", "us")
    source = request.args.get("source")
    page = request.args.get("page", 1, type=int)

    service = NewsService()

    try:

        news = service.get_headlines(
            country=country,
            category=category,
            source=source,
            page=page
        )

        return jsonify({
            "status": "success",
            "totalResults": news.get("totalResults", 0),
            "articles": news.get("articles", [])
        }), 200

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@api_bp.route("/saved", methods=["GET"])
def api_saved_articles():

    auth_error = api_login_required()

    if auth_error:
        return auth_error

    articles = SavedArticle.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        SavedArticle.saved_at.desc()
    ).all()

    result = []

    for article in articles:

        result.append({
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "source": article.source,
            "image_url": article.image_url,
            "published_at": article.published_at,
            "is_read": article.is_read,
            "saved_at": article.saved_at.isoformat() if article.saved_at else None,
            "reading_list_id": article.list_id,
            "tags": [
                tag.name for tag in article.tags
            ],
            "notes": [
                note.content for note in article.notes
            ]
        })

    return jsonify({
        "status": "success",
        "saved_articles": result
    }), 200


@api_bp.route("/saved", methods=["POST"])
def api_save_article():

    auth_error = api_login_required()

    if auth_error:
        return auth_error

    data = request.get_json()

    if not data:

        return jsonify({
            "status": "error",
            "message": "JSON body is required"
        }), 400

    title = data.get("title")
    url = data.get("url")
    source = data.get("source")
    image_url = data.get("image_url")
    published_at = data.get("published_at")
    list_id = data.get("list_id")

    if not title or not url:

        return jsonify({
            "status": "error",
            "message": "Title and URL are required"
        }), 400

    existing_article = SavedArticle.query.filter_by(
        user_id=session["user_id"],
        url=url
    ).first()

    if existing_article:

        return jsonify({
            "status": "error",
            "message": "Article is already saved"
        }), 409

    if not list_id:

        default_list = ReadingList.query.filter_by(
            user_id=session["user_id"],
            name="Saved Articles"
        ).first()

        if not default_list:

            default_list = ReadingList(
                name="Saved Articles",
                user_id=session["user_id"]
            )

            db.session.add(default_list)
            db.session.commit()

        list_id = default_list.id

    saved_article = SavedArticle(
        user_id=session["user_id"],
        list_id=list_id,
        title=title,
        url=url,
        source=source,
        image_url=image_url,
        published_at=published_at
    )

    db.session.add(saved_article)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Article saved",
        "article": {
            "id": saved_article.id,
            "title": saved_article.title,
            "url": saved_article.url
        }
    }), 201


@api_bp.route("/saved/<int:article_id>", methods=["DELETE"])
def api_delete_saved_article(article_id):

    auth_error = api_login_required()

    if auth_error:
        return auth_error

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first()

    if not article:

        return jsonify({
            "status": "error",
            "message": "Saved article not found"
        }), 404

    for note in article.notes:
        db.session.delete(note)

    db.session.delete(article)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Saved article deleted"
    }), 200


@api_bp.route("/reading-lists", methods=["GET"])
def api_reading_lists():

    auth_error = api_login_required()

    if auth_error:
        return auth_error

    reading_lists = ReadingList.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        ReadingList.created_at.desc()
    ).all()

    result = []

    for reading_list in reading_lists:

        result.append({
            "id": reading_list.id,
            "name": reading_list.name,
            "created_at": reading_list.created_at.isoformat() if reading_list.created_at else None,
            "article_count": SavedArticle.query.filter_by(
                list_id=reading_list.id,
                user_id=session["user_id"]
            ).count()
        })

    return jsonify({
        "status": "success",
        "reading_lists": result
    }), 200


