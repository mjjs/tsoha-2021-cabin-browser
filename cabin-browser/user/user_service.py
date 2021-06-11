from bcrypt import checkpw, gensalt, hashpw
from .user_repository import UserNotFoundError, UserExistsError
from flask_login import login_user, logout_user


class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def get_user(self, id):
        try:
            return self._user_repository.get(id)
        except UserNotFoundError:
            return None

    def get_user_by_email(self, email):
        try:
            return self._user_repository.get_by_email(email)
        except UserNotFoundError:
            return None

    def add_user(self, email, name, password, role):
        hashed_password = hashpw(password.encode("utf-8"), gensalt())

        try:
            self._user_repository.add(email, name, hashed_password, role)
            return True
        except UserExistsError:
            return False

    def check_user_password(self, user_id, password):
        hashed_password = self._user_repository.get_password_hash_by_user_id(user_id)
        return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    @staticmethod
    def log_user_in(user):
        login_user(user)

    @staticmethod
    def log_user_out():
        logout_user()
