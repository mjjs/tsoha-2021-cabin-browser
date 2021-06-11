from uuid import uuid4
from enum import Enum
from flask_login import UserMixin
from repository import Repository


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


class UserNotFoundError(Exception):
    def __init__(self, key, value):
        super().__init__(f"A user with the {key} {value} was not found in the database")


class UserExistsError(Exception):
    def __init__(self, email):
        super().__init__(f"User with email {email} already exists in the database")


class UserRepository(Repository):
    def __init__(self, connection_pool):
        fields = ["id", "email", "name", "password", "role"]
        Repository.__init__(
            self,
            connection_pool=connection_pool,
            fields=fields,
            insertable_fields=fields,
            table_name="users",
        )

    def get(self, id):
        row = Repository._get(self, id)

        if not row:
            raise UserNotFoundError("ID", id)

        (id, email, name, _, role) = row

        return User(id=id, email=email, name=name, role=role)

    def add(self, email, name, password_hash, role):
        try:
            self.get_by_email(email)
            raise UserExistsError(email)
        except UserNotFoundError:
            Repository._add(
                self, [uuid4(), email, name, password_hash.decode("utf-8"), role]
            )

    def get_by_email(self, email):
        row = Repository._get_by_field(self, "email", email)

        if not row:
            raise UserNotFoundError("email", email)

        (id, email, name, _, role) = row

        return User(id=id, email=email, name=name, role=role)

    def get_password_hash_by_user_id(self, id):
        row = Repository._get(self, id)

        if not row:
            raise UserNotFoundError("ID", id)

        (_, _, _, password_hash, _) = row

        return password_hash
