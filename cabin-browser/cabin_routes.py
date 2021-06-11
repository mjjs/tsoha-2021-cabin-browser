from base64 import b64encode
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import connection_pool
from cabin_repository import CabinNotFoundError, CabinRepository
from user import UserNotFoundError, UserRepository
from cabin_image_repository import CabinImageRepository
from reservation import ReservationRepository
from keywords import KeywordRepository
from review import ReviewRepository
from municipality import MunicipalityRepository
from user import UserRole
from validators import (
    validate_name,
    is_empty,
    is_valid_municipality,
    is_valid_price_str,
    is_valid_image,
)

cabin_routes = Blueprint("cabin_routes", __name__, template_folder="templates")

cabin_repository = CabinRepository(connection_pool)
cabin_image_repository = CabinImageRepository(connection_pool)
keyword_repository = KeywordRepository(connection_pool)
municipality_repository = MunicipalityRepository(connection_pool)
reservation_repository = ReservationRepository(connection_pool)
review_repository = ReviewRepository(connection_pool)
user_repository = UserRepository(connection_pool)


@cabin_routes.route("/cabins", methods=["GET"])
def get_all_cabins():
    user_id = request.args.get("owner")
    if user_id:
        if current_user.role == UserRole.CUSTOMER.value:
            return redirect("/cabins")

    cabins = []
    if user_id:
        cabins = cabin_repository.get_all_by_owner_id(user_id)
    else:
        cabins = cabin_repository.get_all()

    for cabin in cabins:
        cabin.images = [cabin_image_repository.get_default_cabin_image(cabin.id)]
        cabin.reservations = reservation_repository.get_by_cabin_id(cabin.id)
        cabin.keywords = keyword_repository.get_by_cabin_id(cabin.id)

    all_keywords = keyword_repository.get_all()
    municipalities = municipality_repository.get_all_used()

    return render_template(
        "cabins.html",
        cabins=cabins,
        keywords=all_keywords,
        municipalities=municipalities,
    )


@cabin_routes.route("/cabins/<int:id>", methods=["DELETE"])
@login_required
def delete_cabin(id):
    if current_user.role == UserRole.CUSTOMER.value:
        return "NOT OK", 403

    cabin = cabin_repository.get(id)

    if current_user.role == UserRole.CABIN_OWNER.value:
        if cabin.owner_id != current_user.id:
            return "NOT OK", 403

    cabin_repository.delete(id)

    return "OK"


@cabin_routes.route("/cabins/<int:id>", methods=["GET"])
def get_cabin(id):
    cabin = None

    try:
        cabin = cabin_repository.get(id)
    except CabinNotFoundError:
        return render_template("404.html")

    owner = None

    try:
        owner = user_repository.get(cabin.owner_id)
    except UserNotFoundError:
        return render_template("500.html")

    reviews = review_repository.get_by_cabin_id(id)
    cabin.images = cabin_image_repository.get_by_cabin_id(id)
    reservations = reservation_repository.get_by_cabin_id(id)
    keywords = keyword_repository.get_by_cabin_id(id)

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

    municipalities = municipality_repository.get_all()
    keywords = keyword_repository.get_all()

    return render_template(
        "addcabin.html", municipalities=municipalities, keywords=keywords
    )


@cabin_routes.route("/newcabin", methods=["POST"])
@login_required
def create_new_cabin():
    if current_user.role != UserRole.CABIN_OWNER.value:
        flash("Only cabin owners can add new cabins", "error")
        return render_template("cabins.html"), 403

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
        if not is_valid_image(image):
            flash("Only jpeg or png images are supported", "error")
            error = True
            break

    if error:
        return redirect("/newcabin")

    # TODO: Do these in a transaction?
    cabin_id = cabin_repository.add(
        address,
        float(price) * 1000000,
        description,
        municipality_id,
        name,
        current_user.id,
    )

    for kw in keywords:
        keyword_repository.add_to_cabin(kw, cabin_id)

    if "default_image" in request.form:
        default_image = request.form["default_image"]

        for image in images:
            mimetype = image.mimetype
            b64 = b64encode(image.read()).decode()
            default = default_image == image.filename
            cabin_image_repository.add(f"{mimetype};base64,{b64}", cabin_id, default)

    flash("Cabin added.", "success")
    return redirect(f"/cabins/{cabin_id}")
