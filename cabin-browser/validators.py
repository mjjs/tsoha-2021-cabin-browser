from re import match
from db import get_db
from imghdr import what


def validate_name(name):
    return not is_empty(name)


def validate_email(email):
    return match(r".+@.+\..+", email) is not None


def passwords_match(password, confirm_password):
    return password == confirm_password


def validate_role(role):
    return role in ("CUSTOMER", "OWNER")


def validate_password_complexity(password):
    # TODO: implement this
    return True


def is_empty(x):
    return x == ""


def is_valid_municipality(municipality_id):
    if not municipality_id.isnumeric():
        return False

    db = get_db()
    for municipality in db.municipality_repository.get_all():
        if municipality.id == int(municipality_id):
            return True

    return False


def is_valid_price_str(price):
    return price.isnumeric() and int(price) >= 0


def is_valid_image(img):
    is_valid = True
    if what(None, h=img.read()) not in ("jpeg", "png"):
        is_valid = False

    img.seek(0)

    return is_valid
