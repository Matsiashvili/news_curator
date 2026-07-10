from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from app.extensions import db
from app.models import SavedArticle, ReadingList
from app.news.services import NewsService
from app.reading_lists.services import ReadingListService


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


def api_login_required():
    """
    Return a JSON authentication error when the user is not logged in.
    Return None when the user is authenticated.
    """

    if "user_id" not in session:
        return jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401

    return None


@api_bp.route("/news", methods=["GET"])
def api_news():
    category = request.args.get("category")
    country = request.args.get("country", "us")
    source = request.args.get("source")
    page = request.args.get("page", 1, type=int)

    if page < 1:
        return jsonify({
            "status": "error",
            "message": "Page must be greater than zero"
        }), 400

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
            "page": page,
            "page_size": 15,
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
            "saved_at": (
                article.saved_at.isoformat()
                if article.saved_at
                else None
            ),
            "reading_list_id": article.list_id,
            "tags": [
                tag.name
                for tag in article.tags
            ],
            "notes": [
                note.content
                for note in article.notes
            ]
        })

    return jsonify({
        "status": "success",
        "count": len(result),
        "saved_articles": result
    }), 200


@api_bp.route("/saved", methods=["POST"])
def api_save_article():
    auth_error = api_login_required()

    if auth_error:
        return auth_error

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "A valid JSON body is required"
        }), 400

    title = str(data.get("title", "")).strip()
    url = str(data.get("url", "")).strip()
    source = data.get("source")
    image_url = data.get("image_url")
    published_at = data.get("published_at")
    raw_list_id = data.get("list_id")

    if isinstance(source, dict):
        source = source.get("name")

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

    if raw_list_id in (None, ""):
        reading_list = (
            ReadingListService.get_or_create_default_list(
                session["user_id"]
            )
        )

    else:
        try:
            list_id = int(raw_list_id)

        except (TypeError, ValueError):
            return jsonify({
                "status": "error",
                "message": "Reading list ID must be an integer"
            }), 400

        reading_list = ReadingListService.get_user_list(
            session["user_id"],
            list_id
        )

        if reading_list is None:
            return jsonify({
                "status": "error",
                "message": "Reading list not found"
            }), 404

    saved_article = SavedArticle(
        user_id=session["user_id"],
        list_id=reading_list.id,
        title=title,
        url=url,
        source=source,
        image_url=image_url,
        published_at=published_at
    )

    try:
        db.session.add(saved_article)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": "The article could not be saved"
        }), 500

    return jsonify({
        "status": "success",
        "message": "Article saved",
        "article": {
            "id": saved_article.id,
            "title": saved_article.title,
            "url": saved_article.url,
            "reading_list_id": saved_article.list_id
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

    if article is None:
        return jsonify({
            "status": "error",
            "message": "Saved article not found"
        }), 404

    try:
        db.session.delete(article)
        db.session.commit()

    except Exception:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": "The article could not be deleted"
        }), 500

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
            "created_at": (
                reading_list.created_at.isoformat()
                if reading_list.created_at
                else None
            ),
            "article_count": SavedArticle.query.filter_by(
                list_id=reading_list.id,
                user_id=session["user_id"]
            ).count()
        })

    return jsonify({
        "status": "success",
        "count": len(result),
        "reading_lists": result
    }), 200