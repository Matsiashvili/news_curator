from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db
from app.models import User

from .forms import RegisterForm, LoginForm


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)