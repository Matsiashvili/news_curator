from datetime import datetime

from .extensions import db


article_tags = db.Table(
    "article_tags",

    db.Column(
        "saved_article_id",
        db.Integer,
        db.ForeignKey("saved_articles.id"),
        primary_key=True
    ),

    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )
)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    preferred_categories = db.Column(
        db.String(255)
    )

    country = db.Column(
        db.String(10),
        default="us"
    )


    reading_lists = db.relationship(
        "ReadingList",
        backref="user",
        lazy=True
    )


    saved_articles = db.relationship(
        "SavedArticle",
        backref="user",
        lazy=True
    )



class ReadingList(db.Model):

    __tablename__ = "reading_lists"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


class SavedArticle(db.Model):

    __tablename__ = "saved_articles"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(255),
        nullable=False
    )


    url = db.Column(
        db.String(500),
        nullable=False
    )


    source = db.Column(
        db.String(100)
    )


    image_url = db.Column(
        db.String(500)
    )


    published_at = db.Column(
        db.String(100)
    )


    is_read = db.Column(
        db.Boolean,
        default=False
    )


    saved_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    list_id = db.Column(
        db.Integer,
        db.ForeignKey("reading_lists.id")
    )


    notes = db.relationship(
        "Note",
        backref="article",
        lazy=True,
        cascade="all, delete-orphan"
    )


    tags = db.relationship(
        "Tag",
        secondary=article_tags,
        backref="articles"
    )



class Note(db.Model):

    __tablename__ = "notes"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    content = db.Column(
        db.String(500),
        nullable=False
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    saved_article_id = db.Column(
        db.Integer,
        db.ForeignKey("saved_articles.id"),
        nullable=False
    )



class Tag(db.Model):

    __tablename__ = "tags"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )