from flask import Blueprint, render_template, request
from flask_login import login_required
from db import get_db

keyword_routes = Blueprint("keyword_routes", __name__, template_folder = "templates")

@keyword_routes.route("/keywords", methods = ["POST"])
def keyword_post():
    db = get_db()

    keyword = request.json["keyword"]

    if len(keyword) == 0:
        return "-1", 400

    added_id = "-1"
    try:
        added_id = str(db.keyword_repository.add(keyword))
    except:
        return added_id, 400

    return added_id
