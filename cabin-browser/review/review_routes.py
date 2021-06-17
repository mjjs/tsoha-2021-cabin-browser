from datetime import date
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from user import UserRole
from db import connection_pool
from cabin.cabin_repository import CabinNotFoundError, CabinRepository
from validators import (
    validate_review_content,
    validate_review_rating,
    REVIEW_CONTENT_MAX_LENGTH,
)
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
    if not validate_review_rating(int(rating)):
        flash(f"The review rating must be a value from the range 1-5.")
        return redirect(f"/cabins/{cabin_id}/review")

    content = request.form["content"]
    if not validate_review_content(content):
        flash(
            f"The review content must be at most {REVIEW_CONTENT_MAX_LENGTH} characters."
        )
        return redirect(f"/cabins/{cabin_id}/review")

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
