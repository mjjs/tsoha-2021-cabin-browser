from flask import Blueprint, redirect, request, render_template, flash
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

    if not validate_passwords(password, confirm_password):
        flash("Passwords did not match.", "error")
        error = True

    if not validate_password_complexity(password):
        flash("To be written")
        error = True

    if error:
        return render_template("register.html")

    role = request.form["role"]
    # TODO: validate roles

    hashed_password = hashpw(password.encode("utf-8"), gensalt())

    try:
        db.user_repository.add(email, name, hashed_password, role)
    except UserExistsError:
        flash("A user already exists with the given email.", "error")
        return render_template("register.html")

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
