from flask import Blueprint, request
from flask_login import login_required
from db import connection_pool
from keywords import KeywordRepository
from .keyword_service import KeywordService, EmptyKeywordError

keyword_routes = Blueprint("keyword_routes", __name__, template_folder="templates")
keyword_service = KeywordService(KeywordRepository(connection_pool))

ADD_FAILED = "-1"


@keyword_routes.route("/keywords", methods=["POST"])
@login_required
def keyword_post():
    keyword = request.json["keyword"]

    try:
        added_id = keyword_service.add_keyword(keyword)
        if not added_id:
            return ADD_FAILED, 400

        return added_id
    except EmptyKeywordError:
        return ADD_FAILED, 400
