from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, current_user
from db import get_db
from bcrypt import checkpw
from user_repository import UserNotFoundError

login_routes = Blueprint("login_routes", __name__, template_folder = "templates")

@login_routes.route("/login", methods = ["GET"])
def login_get():
    #if current_user.is_authenticated:
    #    return redirect("/")

    return render_template("login.html")

@login_routes.route("/login", methods = ["POST"])
def login_post():
    db = get_db()

    email = request.form["email"]
    password = request.form["password"]

    try:
        user = db.user_repository.get_user_by_email(email)
    except UserNotFoundError:
        return render_template("login.html", error_message = "Incorrect username or password")

    hashed_password = db.user_repository.get_password_hash_by_user_id(user.user_id)

    if authenticate_user(password.encode("utf-8"), hashed_password.encode("utf-8")):
        login_user(user)
        return redirect("/")

    return render_template("login.html", error_message = "Incorrect username or password")

def authenticate_user(password, hashed_password):
    return checkpw(password, hashed_password)
