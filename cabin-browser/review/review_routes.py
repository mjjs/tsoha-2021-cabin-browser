from datetime import date
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from user import UserRole
from db import connection_pool
from cabin.cabin_repository import CabinNotFoundError, CabinRepository
from .review_repository import ReviewRepository
from .review_service import ReviewService

review_routes = Blueprint("review_routes", __name__, template_folder="templates")
cabin_repository = CabinRepository(connection_pool)

review_service = ReviewService(
    review_repository=ReviewRepository(connection_pool),
    cabin_repository=cabin_repository,
)


@review_routes.route("/cabins/<int:cabin_id>/review", methods=["GET"])
@login_required
def review_get(cabin_id):
    if current_user.role != UserRole.CUSTOMER.value:
        flash("Please log in as a customer to write reviews.", "error")
        return redirect(f"/cabins/{cabin_id}")

    try:
        cabin = cabin_repository.get(cabin_id)
        return render_template("review.html", cabin=cabin)
    except CabinNotFoundError:
        return render_template("404.html")


@review_routes.route("/cabins/<int:cabin_id>/review", methods=["POST"])
@login_required
def review_post(cabin_id):
    if current_user.role != UserRole.CUSTOMER.value:
        flash("Please log in as a customer to write reviews.", "error")
        return redirect(f"/cabins/{cabin_id}")

    rating = request.form["rating"]
    content = request.form["content"]

    review_service.add_review(
        rating=rating, content=content, user_id=current_user.id, cabin_id=cabin_id
    )

    flash("Review added.", "success")

    return redirect(f"/cabins/{cabin_id}")


@review_routes.route(
    "/cabins/<int:cabin_id>/review/<int:review_id>", methods=["DELETE"]
)
@login_required
def review_delete(cabin_id, review_id):
    if current_user.role == UserRole.CUSTOMER:
        return "NOT OK", 403

    try:
        if review_service.delete_review(cabin_id, review_id, current_user.id):
            return "OK"

        return "NOT OK", 403

    except CabinNotFoundError:
        return render_template("404.html")
