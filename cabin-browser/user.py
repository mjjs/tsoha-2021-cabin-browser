from flask_login import UserMixin
from enum import Enum

class UserRole(Enum):
    CUSTOMER = "customer"
    CABIN_OWNER = "owner"
    ADMIN = "admin"

class User(UserMixin):
    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role

    def get_id(self):
        return self.user_id

    def __str__(self):
        return self.name
