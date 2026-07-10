from datetime import datetime


def register_filters(app):

    @app.template_filter("format_date")
    def format_date(value):

        if not value:
            return ""

        if isinstance(value, str):
            return value[:10]

        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")

        return value