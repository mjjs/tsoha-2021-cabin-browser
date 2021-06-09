from re import match
from urllib.parse import urlparse, urljoin
from flask import Blueprint, redirect, flash, request, render_template
from flask_login import logout_user, login_required, login_user, current_user
from bcrypt import checkpw, hashpw, gensalt
from db import connection_pool
from user_repository import UserNotFoundError, UserExistsError, UserRepository
from validators import (
    validate_name,
    validate_email,
    passwords_match,
    validate_password_complexity,
    validate_role,
)

authentication_routes = Blueprint(
    "authentication_routes", __name__, template_folder="templates"
)

INCORRECT_USER_OR_PW_MSG = "Incorrect username or password"

user_repository = UserRepository(connection_pool)

@authentication_routes.route("/login", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        flash("You must log out before logging in", "error")
        return redirect("/")

    next_page = request.args.get("next")
    if not is_safe_url(next_page):
        return render_template("login.html", **request.args)

    return render_template("login.html", next_page=next_page or "")


@authentication_routes.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]

    try:
        user = user_repository.get_by_email(email)
    except UserNotFoundError:
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return render_template("login.html")

    hashed_password = user_repository.get_password_hash_by_user_id(user.id)

    if not checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return render_template("login.html")

    login_user(user)

    next_page = request.args.get("next")

    flash("Login successful", "success")

    if not is_safe_url(next_page):
        return redirect("/")

    return redirect(next_page or "/")


@authentication_routes.route("/register", methods=["GET"])
def render_register_page():
    if current_user.is_authenticated:
        return redirect("/")

    return render_template("register.html")


@authentication_routes.route("/register", methods=["POST"])
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
        flash("To be written")
        error = True

    role = request.form["role"]
    if not validate_role(role):
        flash("An invalid role was supplied.")
        error = True

    if error:
        return render_template("register.html")

    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    try:
        user_repository.add(email, name, hashed_password, role)
    except UserExistsError:
        flash("A user already exists with the given email.", "error")
        return render_template("register.html")

    flash("Register successful. You can now log in.", "success")
    return redirect("/login")


@authentication_routes.route("/logout", methods=["GET"])
@login_required
def logout_get():
    logout_user()

    flash("Logged out successfully.", "success")

    return redirect("/")


def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
