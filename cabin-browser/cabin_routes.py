from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from db import get_db
from cabin_repository import CabinNotFoundError
from user_repository import UserNotFoundError
from user import UserRole

cabin_routes = Blueprint("cabin_routes", __name__, template_folder = "templates")

@cabin_routes.route("/cabins", methods = ["GET"])
def cabins_get():
    user_id = request.args.get("owner")
    if user_id is not None:
        if current_user.role == UserRole.CUSTOMER.value:
            return redirect("/cabins")

    db = get_db()

    cabins = []
    if user_id:
        cabins = db.cabin_repository.get_all_by_owner_id(user_id)
    else:
        cabins = db.cabin_repository.get_all()

    for c in cabins:
        c.images = [db.cabin_image_repository.get_default_cabin_image(c.id)]
        c.reservations = db.reservation_repository.get_by_cabin_id(c.id)

    return render_template("cabins.html", cabins = cabins)

@cabin_routes.route("/cabin/<int:id>", methods = ["DELETE"])
@login_required
def cabin_delete(id):
    db = get_db()

    if current_user.role == UserRole.CUSTOMER.value:
        return "NOT OK", 403

    cabin = db.cabin_repository.get(id)

    if current_user.role == UserRole.CABIN_OWNER.value:
        if cabin.owner_id != current_user.id:
            return "NOT OK"

    # TODO: Verify user to be cabin's owner/admin
    db.cabin_repository.delete(id)

    return "OK"

@cabin_routes.route("/cabin/<int:id>", methods = ["GET"])
def cabin_get(id):
    db = get_db()

    cabin = None

    try:
        cabin = db.cabin_repository.get(id)
    except CabinNotFoundError:
        return render_template("404.html")

    owner = None

    try:
        owner = db.user_repository.get(cabin.owner_id)
    except UserNotFoundError:
        return render_template("500.html")

    reviews = db.review_repository.get_by_cabin_id(id)
    cabin.images = db.cabin_image_repository.get_by_cabin_id(id)
    reservations = db.reservation_repository.get_by_cabin_id(id)

    return render_template(
            "cabin.html",
            cabin = cabin,
            owner = owner,
            reviews = reviews,
            reservations = reservations,
    )

@cabin_routes.route("/cabin/<int:id>/review", methods = ["GET"])
@login_required
def review_get(id):
    db = get_db()

    try:
        cabin = db.cabin_repository.get(id)
        return render_template("review.html", cabin = cabin)
    except CabinNotFoundError:
        return render_template("404.html")

@cabin_routes.route("/cabin/<int:id>/review", methods = ["POST"])
@login_required
def review_post(id):
    db = get_db()

    rating = request.form["rating"]
    content = request.form["content"]

    db.review_repository.add(
            rating = rating,
            content = content,
            user_id = current_user.id,
            cabin_id = id,
    )

    return redirect(f"/cabin/{id}")

@cabin_routes.route("/cabin/<int:cabin_id>/review/<int:review_id>", methods = ["DELETE"])
@login_required
def review_delete(cabin_id, review_id):
    db = get_db()

    if current_user.role == UserRole.CUSTOMER:
        return "NOT OK"

    try:
        cabin = db.cabin_repository.get(cabin_id)
        if cabin.owner_id == current_user.id:
            db.review_repository.delete_review(review_id)

            return "OK"

    except CabinNotFoundError:
        return render_template("404.html")

    return "NOT OK", 403
