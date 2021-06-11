from re import match
from imghdr import what
from db import connection_pool
from municipality import MunicipalityRepository

common_passwords = None


def validate_name(name):
    return not is_empty(name)


def validate_email(email):
    return match(r".+@.+\..+", email) is not None


def passwords_match(password, confirm_password):
    return password == confirm_password


def validate_role(role):
    return role in ("CUSTOMER", "OWNER")


def validate_password_complexity(password):
    global common_passwords

    if len(password) == 0:
        return False

    if not common_passwords:
        _populate_common_passwords()

    return password not in common_passwords


def is_empty(x):
    return x == ""


def is_valid_municipality(municipality_id):
    if not municipality_id.isnumeric():
        return False

    for municipality in MunicipalityRepository(connection_pool).get_all():
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


# Passwords are populated from https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt
def _populate_common_passwords():
    global common_passwords

    common_passwords = set()

    with open("10-million-password-list-top-100000.txt") as f:
        lines = f.readlines()

        for line in lines:
            common_passwords.add(line.rstrip())
