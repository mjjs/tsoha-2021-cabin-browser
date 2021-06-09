from user import User
from uuid import uuid4
from repository import Repository


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
        (id, email, name, _, role) = row

        if not row:
            raise UserNotFoundError("ID", id)

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
        (id, email, name, _, role) = row

        if not row:
            raise UserNotFoundError("email", email)

        return User(id=id, email=email, name=name, role=role)

    def get_password_hash_by_user_id(self, id):
        row = Repository._get(self, id)
        (_, _, _, password_hash, _) = row

        if not row:
            raise UserNotFoundError("ID", id)

        return password_hash
