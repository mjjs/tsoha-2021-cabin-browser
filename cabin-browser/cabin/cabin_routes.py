from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import connection_pool
from user import UserRepository, UserService, UserRole
from reservation import ReservationRepository
from keywords import KeywordService, KeywordRepository
from review import ReviewRepository
from municipality import MunicipalityRepository
from validators import (
    validate_name,
    is_empty,
    is_valid_municipality,
    is_valid_price_str,
    is_valid_image,
)
from .cabin_service import CabinService
from .cabin_repository import CabinRepository
from .cabin_image_repository import CabinImageRepository

cabin_routes = Blueprint("cabin_routes", __name__, template_folder="templates")

municipality_repository = MunicipalityRepository(connection_pool)
reservation_repository = ReservationRepository(connection_pool)
review_repository = ReviewRepository(connection_pool)

user_service = UserService(UserRepository(connection_pool))
keyword_service = KeywordService(KeywordRepository(connection_pool))
cabin_service = CabinService(
    cabin_repository=CabinRepository(connection_pool),
    cabin_image_repository=CabinImageRepository(connection_pool),
    reservation_repository=reservation_repository,
    keyword_repository=KeywordRepository(connection_pool),
)


@cabin_routes.route("/cabins", methods=["GET"])
def get_all_cabins():
    user_id = request.args.get("owner")
    if user_id:
        if current_user.role in (UserRole.ADMIN.value, UserRole.CUSTOMER.value):
            return redirect("/cabins")

    cabins = cabin_service.get_all_cabins(user_id)

    all_keywords = keyword_service.get_all_keywords()
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

    deleted = False

    if current_user.role == UserRole.ADMIN.value:
        deleted = cabin_service.delete_cabin(id)
    else:
        deleted = cabin_service.delete_cabin(id, current_user.id)

    if not deleted:
        return "NOT OK", 403

    return "OK"


@cabin_routes.route("/cabins/<int:id>", methods=["GET"])
def get_cabin(id):
    cabin = cabin_service.get_cabin(id)
    if not cabin:
        flash(f"No cabin found with id {id}", "error")
        return render_template("404.html")

    owner = user_service.get_user(cabin.owner_id)
    if not owner:
        return render_template("500.html")

    reviews = review_repository.get_by_cabin_id(id)
    reservations = reservation_repository.get_by_cabin_id(id)
    keywords = keyword_service.get_cabin_keywords(id)

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
        flash("Only cabin owners can add new cabins.", "error")
        return render_template("cabins.html"), 403

    municipalities = municipality_repository.get_all()
    keywords = keyword_service.get_all_keywords()

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

    default_image_name = request.form.get("default_image") or None
    added_cabin_id = cabin_service.add_cabin(
        address=address,
        price=float(price),
        description=description,
        municipality_id=municipality_id,
        name=name,
        owner_id=current_user.id,
        keywords=keywords,
        images=images,
        default_image_name=default_image_name,
    )

    if not added_cabin_id:
        flash("Cabin coult not be added. Please try again.", "error")
        return redirect("/newcabin")

    flash("Cabin added.", "success")
    return redirect(f"/cabins/{added_cabin_id}")
