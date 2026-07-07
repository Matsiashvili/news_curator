from flask import Blueprint, jsonify


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api_bp.route("/test")
def test_api():

    return jsonify({
        "message": "API is working"
    })