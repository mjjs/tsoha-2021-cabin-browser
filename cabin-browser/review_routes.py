from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import get_db
from cabin_repository import CabinNotFoundError
from datetime import date
from user import UserRole

review_routes = Blueprint("review_routes", __name__, template_folder="templates")


@review_routes.route("/cabins/<int:id>/review", methods=["GET"])
@login_required
def review_get(id):
    db = get_db()

    try:
        cabin = db.cabin_repository.get(id)
        return render_template("review.html", cabin=cabin)
    except CabinNotFoundError:
        return render_template("404.html")


@review_routes.route("/cabins/<int:id>/review", methods=["POST"])
@login_required
def review_post(id):
    db = get_db()

    rating = request.form["rating"]
    content = request.form["content"]

    db.review_repository.add(
        rating=rating,
        content=content,
        user_id=current_user.id,
        cabin_id=id,
    )

    flash("Review added.", "success")

    return redirect(f"/cabins/{id}")


@review_routes.route(
    "/cabins/<int:cabin_id>/review/<int:review_id>", methods=["DELETE"]
)
@login_required
def review_delete(cabin_id, review_id):
    db = get_db()

    if current_user.role == UserRole.CUSTOMER:
        return "NOT OK", 403

    try:
        cabin = db.cabin_repository.get(cabin_id)
        review = db.review_repository.get(review_id)

        if cabin.owner_id == current_user.id or review.user_id == current_user.id:
            db.review_repository.delete_review(review_id)

            return "OK"

    except CabinNotFoundError:
        return render_template("404.html")

    return "NOT OK", 403
