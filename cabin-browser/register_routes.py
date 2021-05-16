from flask import Blueprint, redirect, request, render_template
from flask_login import current_user
from db import get_db
from bcrypt import hashpw, gensalt
from user_repository import UserExistsError
from re import match

register_routes = Blueprint("register_routes", __name__, template_folder = "templates")

@register_routes.route("/register", methods = ["GET"])
def render_register_page():
    if current_user.is_authenticated:
        return redirect("/")

    return render_template("register.html")

@register_routes.route("/register", methods = ["POST"])
def register_user():
    db = get_db()

    name = request.form["name"]
    if not validate_name(name):
        return render_template("register.html", error_message = "Please enter a non-empty name")

    email = request.form["email"]
    if not validate_email(email):
        return render_template(
                "register.html", error_message = "Please enter a valid email address")

    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    if not validate_passwords(password, confirm_password):
        return render_template("register.html", error_message = "Passwords did not match")

    if not validate_password_complexity(password):
        return render_template("register.html", error_message = "Some problem with password")

    role = request.form["role"]
    # TODO: validate roles

    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    try:
        db.user_repository.add(email, name, hashed_password, role)
    except UserExistsError:
        raise NotImplementedError("Duplicate emails are not handled yet")

    return redirect("/login")

def validate_name(name):
    return name != ""

def validate_email(email):
    # TODO: Proper email validation(?)
    return match(r".+@.+\..+", email) is not None

def validate_passwords(password, confirm_password):
    return password == confirm_password

def validate_password_complexity(password):
    # TODO: implement this
    return True
