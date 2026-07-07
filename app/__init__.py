from flask import Flask

from .extensions import db, csrf
from .config import Config
from . import models


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    csrf.init_app(app)


    from .auth.routes import auth_bp
    from .news.routes import news_bp
    from .api.routes import api_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(api_bp)


    return app