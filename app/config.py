import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-me"
    )


    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'news_curator.db')}"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    NEWS_API_KEY = os.environ.get(
        "NEWS_API_KEY"
    )



class TestConfig(Config):
    """Configuration used for running the test suite."""

    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"