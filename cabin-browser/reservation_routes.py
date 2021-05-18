from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import get_db
from cabin_repository import CabinNotFoundError
from datetime import date

reservation_routes = Blueprint("reservation_routes", __name__, template_folder = "templates")

@reservation_routes.route("/reservations/<int:cabin_id>", methods = ["GET"])
@login_required
def reservation_get(cabin_id):
    db = get_db()

    try:
        cabin = db.cabin_repository.get(cabin_id)
        current_reservations = db.reservation_repository.get_by_cabin_id(cabin_id)
        return render_template(
                "reservation.html",
                cabin = cabin,
                current_reservations = current_reservations)

    except CabinNotFoundError:
        return render_template("404.html"), 404

@reservation_routes.route("/reservations/<int:cabin_id>", methods = ["POST"])
@login_required
def reservation_post(cabin_id):
    db = get_db()

    cabin = None
    try:
        cabin = db.cabin_repository.get(cabin_id)
    except CabinNotFoundError:
        return render_template("404.html"), 404

    current_reservations = db.reservation_repository.get_by_cabin_id(cabin_id)

    start_date = date.fromisoformat(request.form["start_date"])
    end_date = date.fromisoformat(request.form["end_date"])

    error = False
    if start_date is None:
        flash("Please pick a start date", "error")
        error = True
    if end_date is None:
        flash("Please pick an end date", "error")
        error = True

    if start_date > end_date:
        flash("The start date must be before the end date", "error")
        error = True

    today = date.today()
    if start_date < today or end_date < today:
        flash("The reservation must not be in the past", "error")
        error = True

    for reservation in current_reservations:
        if reservation.start <= start_date <= reservation.end:
            flash("The selected dates have already been reserved", "error")
            error = True
        elif reservation.start <= end_date <= reservation.end:
            flash("The selected dates have already been reserved", "error")
            error = True


    if error:
        return render_template("reservation.html", cabin = cabin)

    db.reservation_repository.add(start_date, end_date, current_user.id, cabin_id)

    return redirect(f"/cabins/{cabin_id}")

