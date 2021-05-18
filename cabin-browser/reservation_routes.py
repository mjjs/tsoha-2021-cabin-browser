from flask import Blueprint, render_template, request, redirect
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

    # TODO: use flash instead of error_message
    if start_date is None or end_date is None:
        return render_template(
                "reservation.html",
                error_message = "Please pick a start and end date.",
                cabin = cabin)

    if start_date > end_date:
        return render_template(
                "reservation.html",
                error_message = "The start date must be before the end date.",
                cabin = cabin)

    today = date.today()
    if start_date < today or end_date < today:
        return render_template(
                "reservation.html",
                error_message = "The reservation must not be in the past.",
                cabin = cabin)


    for reservation in current_reservations:
        if reservation.start <= start_date <= reservation.end:
            return render_template(
                    "reservation.html",
                    error_message = "The selected dates have already been reserved.",
                    cabin = cabin)

        if reservation.start <= end_date <= reservation.end:
            return render_template(
                    "reservation.html",
                    error_message = "The selected dates have already been reserved.",
                    cabin = cabin)

    db.reservation_repository.add(start_date, end_date, current_user.id, cabin_id)

    return redirect(f"/cabins/{cabin_id}")

