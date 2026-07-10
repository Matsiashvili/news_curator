from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from datetime import datetime, timedelta
from sqlalchemy import func

from app.extensions import db
from app.decorators import login_required

from app.models import (
    ReadingList,
    SavedArticle,
    Note,
    Tag
)


reading_lists_bp = Blueprint(
    "reading_lists",
    __name__,
    url_prefix="/reading-lists"
)


@reading_lists_bp.route("/")
@login_required
def lists():

    user_id = session["user_id"]

    reading_lists = ReadingList.query.filter_by(
        user_id=user_id
    ).order_by(
        ReadingList.created_at.desc()
    ).all()

    return render_template(
        "reading_lists/lists.html",
        reading_lists=reading_lists
    )


@reading_lists_bp.route("/create", methods=["POST"])
@login_required
def create_list():

    name = request.form.get(
        "name",
        ""
    ).strip()

    if not name:
        flash("Reading list name is required.", "danger")
        return redirect(url_for("reading_lists.lists"))

    reading_list = ReadingList(
        name=name,
        user_id=session["user_id"]
    )

    db.session.add(reading_list)
    db.session.commit()

    flash("Reading list created.", "success")

    return redirect(url_for("reading_lists.lists"))


@reading_lists_bp.route("/saved")
@login_required
def saved_articles():

    user_id = session["user_id"]

    articles = SavedArticle.query.filter_by(
        user_id=user_id
    ).order_by(
        SavedArticle.saved_at.desc()
    ).all()

    reading_lists = ReadingList.query.filter_by(
        user_id=user_id
    ).all()

    return render_template(
        "reading_lists/saved.html",
        articles=articles,
        reading_lists=reading_lists
    )


@reading_lists_bp.route("/save", methods=["POST"])
@login_required
def save_articles():

    user_id = session["user_id"]

    title = request.form.get("title")
    url = request.form.get("url")
    source = request.form.get("source")
    image_url = request.form.get("image_url")
    published_at = request.form.get("published_at")
    list_id = request.form.get("list_id")

    if not title or not url:
        flash("Article data is missing.", "danger")
        return redirect(url_for("news.index"))

    existing_article = SavedArticle.query.filter_by(
        user_id=user_id,
        url=url
    ).first()

    if existing_article:
        flash("Article is already saved.", "warning")
        return redirect(url_for("news.index"))

    if not list_id:
        default_list = ReadingList.query.filter_by(
            user_id=user_id,
            name="Saved Articles"
        ).first()

        if not default_list:
            default_list = ReadingList(
                name="Saved Articles",
                user_id=user_id
            )

            db.session.add(default_list)
            db.session.commit()

        list_id = default_list.id

    saved_article = SavedArticle(
        user_id=user_id,
        list_id=list_id,
        title=title,
        url=url,
        source=source,
        image_url=image_url,
        published_at=published_at
    )

    db.session.add(saved_article)
    db.session.commit()

    flash("Article saved.", "success")

    return redirect(url_for("news.index"))


@reading_lists_bp.route("/saved/<int:article_id>/read")
@login_required
def read_saved_article(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    article.is_read = True

    db.session.commit()

    return redirect(article.url)


@reading_lists_bp.route("/saved/<int:article_id>/toggle-read", methods=["POST"])
@login_required
def toggle_read_status(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    article.is_read = not article.is_read

    db.session.commit()

    flash("Read status updated.", "success")

    return redirect(
        url_for("reading_lists.saved_articles")
    )


@reading_lists_bp.route("/saved/<int:article_id>/note", methods=["POST"])
@login_required
def save_note(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    content = request.form.get(
        "content",
        ""
    ).strip()

    if len(content) > 500:

        flash(
            "Note cannot be longer than 500 characters.",
            "danger"
        )

        return redirect(
            url_for("reading_lists.saved_articles")
        )

    note = Note.query.filter_by(
        saved_article_id=article.id,
        user_id=session["user_id"]
    ).first()

    if note:
        note.content = content
    else:
        note = Note(
            saved_article_id=article.id,
            user_id=session["user_id"],
            content=content
        )

        db.session.add(note)

    db.session.commit()

    flash("Note saved.", "success")

    return redirect(
        url_for("reading_lists.saved_articles")
    )


@reading_lists_bp.route("/saved/<int:article_id>/note/delete", methods=["POST"])
@login_required
def delete_note(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    note = Note.query.filter_by(
        saved_article_id=article.id,
        user_id=session["user_id"]
    ).first()

    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted.", "info")
    else:
        flash("No note to delete.", "warning")

    return redirect(
        url_for("reading_lists.saved_articles")
    )


@reading_lists_bp.route("/saved/<int:article_id>/delete", methods=["POST"])
@login_required
def delete_saved_article(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    Note.query.filter_by(
        saved_article_id=article.id,
        user_id=session["user_id"]
    ).delete()

    db.session.delete(article)

    db.session.commit()

    flash("Saved article removed.", "info")

    return redirect(
        url_for("reading_lists.saved_articles")
    )

@reading_lists_bp.route("/saved/<int:article_id>/tag", methods=["POST"])
@login_required
def add_tag(article_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    tag_name = request.form.get(
        "tag_name",
        ""
    ).strip().lower()

    if not tag_name:

        flash("Tag name is required.", "danger")

        return redirect(
            url_for("reading_lists.saved_articles")
        )

    if len(tag_name) > 50:

        flash("Tag name cannot be longer than 50 characters.", "danger")

        return redirect(
            url_for("reading_lists.saved_articles")
        )

    tag = Tag.query.filter_by(
        name=tag_name
    ).first()

    if not tag:

        tag = Tag(
            name=tag_name
        )

        db.session.add(tag)
        db.session.commit()

    if tag not in article.tags:

        article.tags.append(tag)

        db.session.commit()

        flash("Tag added.", "success")

    else:

        flash("Article already has this tag.", "warning")

    return redirect(
        url_for("reading_lists.saved_articles")
    )


@reading_lists_bp.route("/saved/<int:article_id>/tag/<int:tag_id>/remove", methods=["POST"])
@login_required
def remove_tag(article_id, tag_id):

    article = SavedArticle.query.filter_by(
        id=article_id,
        user_id=session["user_id"]
    ).first_or_404()

    tag = Tag.query.get_or_404(
        tag_id
    )

    if tag in article.tags:

        article.tags.remove(tag)

        db.session.commit()

        flash("Tag removed.", "info")

    return redirect(
        url_for("reading_lists.saved_articles")
    )

@reading_lists_bp.route("/statistics")
@login_required
def statistics():

    user_id = session["user_id"]

    one_week_ago = datetime.utcnow() - timedelta(days=7)

    saved_this_week = SavedArticle.query.filter(
        SavedArticle.user_id == user_id,
        SavedArticle.saved_at >= one_week_ago
    ).count()

    total_saved = SavedArticle.query.filter_by(
        user_id=user_id
    ).count()

    read_count = SavedArticle.query.filter_by(
        user_id=user_id,
        is_read=True
    ).count()

    unread_count = SavedArticle.query.filter_by(
        user_id=user_id,
        is_read=False
    ).count()

    source_rows = db.session.query(
        SavedArticle.source,
        func.count(SavedArticle.id)
    ).filter(
        SavedArticle.user_id == user_id,
        SavedArticle.source.isnot(None),
        SavedArticle.source != ""
    ).group_by(
        SavedArticle.source
    ).order_by(
        func.count(SavedArticle.id).desc()
    ).all()

    top_source = None

    if source_rows:
        top_source = source_rows[0][0]

    tag_rows = db.session.query(
        Tag.name,
        func.count(Tag.id)
    ).join(
        SavedArticle.tags
    ).filter(
        SavedArticle.user_id == user_id
    ).group_by(
        Tag.name
    ).order_by(
        func.count(Tag.id).desc()
    ).limit(5).all()

    return render_template(
        "reading_lists/statistics.html",
        saved_this_week=saved_this_week,
        total_saved=total_saved,
        read_count=read_count,
        unread_count=unread_count,
        top_source=top_source,
        source_rows=source_rows,
        tag_rows=tag_rows
    )


@reading_lists_bp.route("/<int:list_id>")
@login_required
def view_list(list_id):

    reading_list = ReadingList.query.filter_by(
        id=list_id,
        user_id=session["user_id"]
    ).first_or_404()

    articles = SavedArticle.query.filter_by(
        list_id=reading_list.id,
        user_id=session["user_id"]
    ).order_by(
        SavedArticle.saved_at.desc()
    ).all()

    return render_template(
        "reading_lists/view_list.html",
        reading_list=reading_list,
        articles=articles
    )