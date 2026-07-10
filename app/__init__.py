from flask import Flask

from .extensions import db, csrf
from .config import Config
from . import models


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .news.routes import news_bp
    from .api.routes import api_bp
    from .reading_lists.routes import reading_lists_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(reading_lists_bp)

    from .errors import register_errors
    register_errors(app)

    from .filters import register_filters
    register_filters(app)

    return app