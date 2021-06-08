from flask import Blueprint, redirect, request, render_template, flash
from flask_login import current_user
from db import get_db
from bcrypt import hashpw, gensalt
from user_repository import UserExistsError
from re import match
from validators import validate_name, validate_email, passwords_match, validate_password_complexity, validate_role

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
        db.user_repository.add(email, name, hashed_password, role)
    except UserExistsError:
        flash("A user already exists with the given email.", "error")
        return render_template("register.html")

    flash("Register successful. You can now log in.", "success")
    return redirect("/login")
