from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, current_user
from db import get_db
from bcrypt import checkpw
from user_repository import UserNotFoundError

login_routes = Blueprint("login_routes", __name__, template_folder = "templates")
INCORRECT_USER_OR_PW_MSG = "Incorrect username or password"

@login_routes.route("/login", methods = ["GET"])
def login_get():
    if current_user.is_authenticated:
        return redirect("/")

    return render_template("login.html")

@login_routes.route("/login", methods = ["POST"])
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

    if checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        login_user(user)
        return redirect("/")

    flash(INCORRECT_USER_OR_PW_MSG, "error")
    return render_template("login.html")
