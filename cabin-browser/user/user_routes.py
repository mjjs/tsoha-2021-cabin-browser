from urllib.parse import urlparse, urljoin
from flask import Blueprint, redirect, flash, request, render_template
from flask_login import login_required, current_user
from db import connection_pool
from validators import (
    validate_name,
    validate_email,
    passwords_match,
    validate_password_complexity,
    validate_role,
)

from .user_service import UserService
from .user_repository import UserRepository

user_routes = Blueprint("user_routes", __name__, template_folder="templates")

INCORRECT_USER_OR_PW_MSG = "Incorrect username or password"

user_service = UserService(UserRepository(connection_pool))


@user_routes.route("/login", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        flash("You must log out before logging in", "error")
        return redirect("/")

    next_page = request.args.get("next")
    if not is_safe_url(next_page):
        return render_template("login.html", **request.args)

    return render_template("login.html", next_page=next_page or "")


@user_routes.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    user = user_service.get_user_by_email(email)
    if not user:
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return redirect("/login")

    if not user_service.check_user_password(user.id, password):
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return redirect("/login")

    user_service.log_user_in(user)
    next_page = request.args.get("next")
    flash("Login successful", "success")

    if not is_safe_url(next_page):
        return redirect("/")

    return redirect(next_page or "/")


@user_routes.route("/register", methods=["GET"])
def render_register_page():
    if current_user.is_authenticated:
        return redirect("/")

    return render_template("register.html")


@user_routes.route("/register", methods=["POST"])
def register_user():
    error = False

    name = request.form["name"]
    if not validate_name(name):
        flash("Name cannot be empty.", "error")
        error = True

    email = request.form["email"]
    if not validate_email(email):
        flash("Please enter a valid email address.", "error")
        error = True

    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if not passwords_match(password, confirm_password):
        flash("Passwords did not match.", "error")
        error = True

    if not validate_password_complexity(password):
        flash("Your password is too common. Please choose a more unique password.")
        error = True

    role = request.form["role"]
    if not validate_role(role):
        flash("An invalid role was supplied.")
        error = True

    if error:
        return redirect("/register")

    if not user_service.add_user(email, name, password, role):
        flash("A user already exists with the given email.", "error")
        return redirect("/register")

    flash("Register successful. You can now log in.", "success")
    return redirect("/login")


@user_routes.route("/logout", methods=["GET"])
@login_required
def logout_get():
    user_service.log_user_out()
    flash("Logged out successfully.", "success")
    return redirect("/")


def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
