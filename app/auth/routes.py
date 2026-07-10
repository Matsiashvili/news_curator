from app.extensions import db
from app.models import User, SavedArticle
from .forms import RegisterForm, LoginForm
from app.decorators import login_required

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_email = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_email:
            flash("Email is already registered.", "danger")
            return redirect(url_for("auth.register"))

        existing_username = User.query.filter_by(
            username=form.username.data
        ).first()

        if existing_username:
            flash("Username is already taken.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(
                form.password.data
            ),
            preferred_categories="technology,business",
            country="us"
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password_hash,
            form.password.data
        ):

            session["user_id"] = user.id
            session["username"] = user.username

            flash("Logged in successfully.", "success")

            return redirect(url_for("news.index"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))


@auth_bp.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():

    user = User.query.get(
        session["user_id"]
    )

    categories = [
        "business",
        "technology",
        "sports",
        "science",
        "health",
        "entertainment"
    ]

    countries = [
        ("us", "United States"),
        ("gb", "United Kingdom"),
        ("ge", "Georgia"),
        ("de", "Germany"),
        ("fr", "France")
    ]

    if request.method == "POST":

        selected_categories = request.form.getlist(
            "categories"
        )

        selected_country = request.form.get(
            "country",
            "us"
        )

        user.preferred_categories = ",".join(
            selected_categories
        )

        user.country = selected_country

        db.session.commit()

        flash("Preferences updated successfully.", "success")

        return redirect(
            url_for("auth.preferences")
        )

    selected_categories = []

    if user.preferred_categories:
        selected_categories = user.preferred_categories.split(",")

    return render_template(
        "auth/preferences.html",
        user=user,
        categories=categories,
        countries=countries,
        selected_categories=selected_categories
    )

@auth_bp.route("/profile")
@login_required
def profile():

    user = User.query.get(
        session["user_id"]
    )

    selected_categories = []

    if user.preferred_categories:
        selected_categories = user.preferred_categories.split(",")

    saved_articles = SavedArticle.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        SavedArticle.saved_at.desc()
    ).limit(6).all()

    saved_count = SavedArticle.query.filter_by(
        user_id=session["user_id"]
    ).count()

    return render_template(
        "auth/profile.html",
        user=user,
        selected_categories=selected_categories,
        saved_articles=saved_articles,
        saved_count=saved_count
    )