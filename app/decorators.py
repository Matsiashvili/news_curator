from functools import wraps

from flask import session, redirect, url_for, flash


def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("auth.login")
            )

        return function(*args, **kwargs)

    return wrapper