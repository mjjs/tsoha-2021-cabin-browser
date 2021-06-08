from urllib.parse import urlparse, urljoin
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user
from bcrypt import checkpw
from db import get_db
from user_repository import UserNotFoundError

login_routes = Blueprint("login_routes", __name__, template_folder="templates")
INCORRECT_USER_OR_PW_MSG = "Incorrect username or password"


@login_routes.route("/login", methods=["GET"])
def login_get():
    if current_user.is_authenticated:
        flash("You must log out before logging in", "error")
        return redirect("/")

    next_page = request.args.get("next")
    if not is_safe_url(next_page):
        return render_template("login.html", **request.args)

    return render_template("login.html", next_page=next_page or "")


@login_routes.route("/login", methods=["POST"])
def login_post():
    db = get_db()

    email = request.form["email"]
    password = request.form["password"]

    try:
        user = db.user_repository.get_by_email(email)
    except UserNotFoundError:
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return render_template("login.html")

    hashed_password = db.user_repository.get_password_hash_by_user_id(user.id)

    if not checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        flash(INCORRECT_USER_OR_PW_MSG, "error")
        return render_template("login.html")

    login_user(user)

    next_page = request.args.get("next")

    flash("Login successful", "success")

    if not is_safe_url(next_page):
        return redirect("/")

    return redirect(next_page or "/")


def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, url))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
