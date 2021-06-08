from re import match
from db import get_db

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
    db = get_db()
    for municipality in db.municipality_repository.get_all():
        if municipality.id == municipality_id:
            return True

    return False

def is_valid_price_str(price):
    return price.isnumeric() and int(price) >= 0
