from flask import Blueprint, redirect
from flask_login import logout_user, login_required

logout_routes = Blueprint("logout", __name__, template_folder = "templates")

@logout_routes.route("/logout", methods = ["GET"])
@login_required
def logout_get():
    logout_user()

    return redirect("/")
