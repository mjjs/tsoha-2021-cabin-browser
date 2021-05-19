from datetime import date
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import get_db
from cabin_repository import CabinNotFoundError
from user_repository import UserNotFoundError
from user import UserRole
from werkzeug.utils import secure_filename
from uuid import uuid4
from os import path
from config import UPLOAD_FOLDER

cabin_routes = Blueprint("cabin_routes", __name__, template_folder = "templates")

@cabin_routes.route("/cabins", methods = ["GET"])
def get_all_cabins():
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
        c.keywords = db.keyword_repository.get_by_cabin_id(c.id)

    all_keywords = db.keyword_repository.get_all()

    return render_template("cabins.html", cabins = cabins, keywords = all_keywords)

@cabin_routes.route("/cabins/<int:id>", methods = ["DELETE"])
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

@cabin_routes.route("/cabins/<int:id>", methods = ["GET"])
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
            cabin = cabin,
            owner = owner,
            reviews = reviews,
            reservations = reservations,
            keywords = keywords,
    )

@cabin_routes.route("/newcabin", methods = ["GET"])
@login_required
def new_cabin_page():
    if current_user.role != UserRole.CABIN_OWNER.value:
        flash("Only cabin owners can add new cabins", "error")
        return render_template("cabins.html"), 403

    db = get_db()
    municipalities = db.municipality_repository.get_all()
    keywords = db.keyword_repository.get_all()

    return render_template("addcabin.html", municipalities = municipalities, keywords = keywords)

@cabin_routes.route("/newcabin", methods = ["POST"])
@login_required
def create_new_cabin():
    if current_user.role != UserRole.CABIN_OWNER.value:
        flash("Only cabin owners can add new cabins", "error")
        return render_template("cabins.html"), 403

    db = get_db()

    # TODO: Validate all of these
    name = request.form["name"]
    address = request.form["address"]
    municipality_id = request.form["municipality"]
    price = request.form["price"]
    description = request.form["description"]
    keywords = request.form.getlist("keywords")
    images = request.files.getlist("images")

    # TODO: Do these in a transaction?
    cabin_id = db.cabin_repository.add(address, float(price) * 1000000, description, municipality_id, name, current_user.id)

    if keywords is not "NONE":
        for kw in keywords:
            db.keyword_repository.add_to_cabin(kw, cabin_id)

    if "default_image" in request.form:
        default_image = request.form["default_image"]

        for image in images:
            ext = path.splitext(image.filename)[1]
            filename = secure_filename(f"{str(uuid4())}.{ext}")
            image.save(path.join(UPLOAD_FOLDER, filename))
            default = default_image == image.filename
            db.cabin_image_repository.add(filename, cabin_id, default)


    return redirect(f"/cabins/{cabin_id}")
