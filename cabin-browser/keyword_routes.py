from flask import Blueprint, render_template, request
from flask_login import login_required
from db import connection_pool
from keyword_repository import KeywordRepository

keyword_routes = Blueprint("keyword_routes", __name__, template_folder="templates")
keyword_repository = KeywordRepository(connection_pool)

ADD_FAILED = "-1"


@keyword_routes.route("/keywords", methods=["POST"])
def keyword_post():
    keyword = request.json["keyword"]

    if len(keyword) == 0:
        return ADD_FAILED, 400

    added_id = ADD_FAILED
    try:
        added_id = str(keyword_repository.add(keyword))
    except:
        return added_id, 400

    return added_id
