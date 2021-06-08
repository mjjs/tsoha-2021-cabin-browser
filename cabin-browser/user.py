from flask_login import UserMixin
from enum import Enum


class UserRole(Enum):
    CUSTOMER = "CUSTOMER"
    CABIN_OWNER = "OWNER"
    ADMIN = "ADMIN"


class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    def __str__(self):
        return self.name
