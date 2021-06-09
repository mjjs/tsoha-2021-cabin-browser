from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import connection_pool
from cabin_repository import CabinNotFoundError, CabinRepository
from review_repository import ReviewRepository
from datetime import date
from user import UserRole

review_routes = Blueprint("review_routes", __name__, template_folder="templates")
review_repository = ReviewRepository(connection_pool)
cabin_repository = CabinRepository(connection_pool)


@review_routes.route("/cabins/<int:id>/review", methods=["GET"])
@login_required
def review_get(id):
    try:
        cabin = cabin_repository.get(id)
        return render_template("review.html", cabin=cabin)
    except CabinNotFoundError:
        return render_template("404.html")


@review_routes.route("/cabins/<int:id>/review", methods=["POST"])
@login_required
def review_post(id):
    rating = request.form["rating"]
    content = request.form["content"]

    review_repository.add(
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
    if current_user.role == UserRole.CUSTOMER:
        return "NOT OK", 403

    try:
        cabin = cabin_repository.get(cabin_id)
        review = review_repository.get(review_id)

        if cabin.owner_id == current_user.id or review.user_id == current_user.id:
            review_repository.delete_review(review_id)

            return "OK"

    except CabinNotFoundError:
        return render_template("404.html")

    return "NOT OK", 403
