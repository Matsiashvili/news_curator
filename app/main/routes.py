from flask import Blueprint, render_template, session

from app.models import User


main_bp = Blueprint(
    "main",
    __name__
)


@main_bp.route("/")
def home():

    user = None

    if session.get("user_id"):
        user = User.query.get(
            session["user_id"]
        )

    return render_template(
        "main/home.html",
        user=user
    )