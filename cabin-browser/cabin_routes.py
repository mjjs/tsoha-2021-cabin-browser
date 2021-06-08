from base64 import b64encode
from imghdr import what
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import get_db
from cabin_repository import CabinNotFoundError
from user_repository import UserNotFoundError
from user import UserRole
from validators import (
    validate_name,
    is_empty,
    is_valid_municipality,
    is_valid_price_str,
)

cabin_routes = Blueprint("cabin_routes", __name__, template_folder="templates")


@cabin_routes.route("/cabins", methods=["GET"])
def get_all_cabins():
    user_id = request.args.get("owner")
    if user_id:
        if current_user.role == UserRole.CUSTOMER.value:
            return redirect("/cabins")

    db = get_db()

    cabins = []
    if user_id:
        cabins = db.cabin_repository.get_all_by_owner_id(user_id)
    else:
        cabins = db.cabin_repository.get_all()

    for cabin in cabins:
        cabin.images = [db.cabin_image_repository.get_default_cabin_image(cabin.id)]
        cabin.reservations = db.reservation_repository.get_by_cabin_id(cabin.id)
        cabin.keywords = db.keyword_repository.get_by_cabin_id(cabin.id)

    all_keywords = db.keyword_repository.get_all()
    municipalities = db.municipality_repository.get_all_used()

    return render_template(
        "cabins.html",
        cabins=cabins,
        keywords=all_keywords,
        municipalities=municipalities,
    )


@cabin_routes.route("/cabins/<int:id>", methods=["DELETE"])
@login_required
def delete_cabin(id):
    db = get_db()

    if current_user.role == UserRole.CUSTOMER.value:
        return "NOT OK", 403

    cabin = db.cabin_repository.get(id)

    if current_user.role == UserRole.CABIN_OWNER.value:
        if cabin.owner_id != current_user.id:
            return "NOT OK", 403

    db.cabin_repository.delete(id)

    return "OK"


@cabin_routes.route("/cabins/<int:id>", methods=["GET"])
def get_cabin(id):
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
    keywords = db.keyword_repository.get_by_cabin_id(id)

    return render_template(
        "cabin.html",
        cabin=cabin,
        owner=owner,
        reviews=reviews,
        reservations=reservations,
        keywords=keywords,
    )


@cabin_routes.route("/newcabin", methods=["GET"])
@login_required
def new_cabin_page():
    if current_user.role != UserRole.CABIN_OWNER.value:
        flash("Only cabin owners can add new cabins", "error")
        return render_template("cabins.html"), 403

    db = get_db()
    municipalities = db.municipality_repository.get_all()
    keywords = db.keyword_repository.get_all()

    return render_template(
        "addcabin.html", municipalities=municipalities, keywords=keywords
    )


@cabin_routes.route("/newcabin", methods=["POST"])
@login_required
def create_new_cabin():
    if current_user.role != UserRole.CABIN_OWNER.value:
        flash("Only cabin owners can add new cabins", "error")
        return render_template("cabins.html"), 403

    db = get_db()

    error = False

    name = request.form["name"]
    if not validate_name(name):
        flash(f"Name {name} is not valid", "error")
        error = True

    address = request.form["address"]
    if is_empty(address):
        flash("Address cannot be empty.", "error")
        error = True

    municipality_id = request.form["municipality"]
    if not is_valid_municipality(municipality_id):
        flash(
            "The selected municipality is not valid. This problem has been logged and will be investigated.",
            "error",
        )
        error = True

    price = request.form["price"]
    if not is_valid_price_str(price):
        flash("Price must be a non-negative number.", "error")
        error = True

    description = request.form["description"]
    keywords = request.form.getlist("keywords")
    images = request.files.getlist("images")

    # Stupid workaround we need to do because the client keeps sending an empty
    # file for some reason.
    images = [img for img in images if img.filename != ""]

    for image in images:
        if what(None, h=image.read()) not in ["jpeg", "png"]:
            flash("Only jpeg or png images are supported", "error")
            error = True
            break

        image.seek(0)

    if error:
        return redirect("/newcabin")

    # TODO: Do these in a transaction?
    cabin_id = db.cabin_repository.add(
        address,
        float(price) * 1000000,
        description,
        municipality_id,
        name,
        current_user.id,
    )

    for kw in keywords:
        db.keyword_repository.add_to_cabin(kw, cabin_id)

    if "default_image" in request.form:
        default_image = request.form["default_image"]

        for image in images:
            mimetype = image.mimetype
            b64 = b64encode(image.read()).decode()
            default = default_image == image.filename
            db.cabin_image_repository.add(f"{mimetype};base64,{b64}", cabin_id, default)

    flash("Cabin added.", "success")
    return redirect(f"/cabins/{cabin_id}")
