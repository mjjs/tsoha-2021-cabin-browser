from datetime import date
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from db import connection_pool
from cabin_repository import CabinNotFoundError, CabinRepository
from .reservation_service import (
    ReservationService,
    ReservationConflictError,
    ReservationInPastError,
)
from reservation import ReservationRepository

reservation_routes = Blueprint(
    "reservation_routes", __name__, template_folder="templates"
)

cabin_repository = CabinRepository(connection_pool)

reservation_service = ReservationService(
    ReservationRepository(connection_pool),
    cabin_repository,
)


@reservation_routes.route("/reservations/<int:cabin_id>", methods=["GET"])
@login_required
def reservation_get(cabin_id):
    try:
        cabin = cabin_repository.get(cabin_id)
        current_reservations = reservation_service.get_cabin_reservations(cabin_id)
        return render_template(
            "reservation.html", cabin=cabin, current_reservations=current_reservations
        )

    except CabinNotFoundError:
        return render_template("404.html"), 404


@reservation_routes.route("/reservations/<int:cabin_id>", methods=["POST"])
@login_required
def reservation_post(cabin_id):
    error = False

    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    if not start_date:
        flash("Please pick a start date", "error")
        error = True

    if not end_date:
        flash("Please pick an end date", "error")
        error = True

    try:
        reservation_service.add_reservation(
            start_date=start_date,
            end_date=end_date,
            user_id=current_user.id,
            cabin_id=cabin_id,
        )
    except CabinNotFoundError:
        return render_template("404.html"), 404
    except ReservationInPastError:
        flash("The reservation must not be in the past", "error")
        error = True
    except ReservationConflictError:
        flash("The selected dates have already been reserved", "error")
        error = True

    if error:
        return redirect(f"/reservations/{cabin_id}")

    return redirect(f"/cabins/{cabin_id}")
