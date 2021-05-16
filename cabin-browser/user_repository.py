from user import User
from uuid import uuid4

class UserNotFoundError(Exception):
    def __init__(self, key, value):
        super().__init__(f"A user with the {key} {value} was not found in the database")

class UserExistsError(Exception):
    def __init__(self, email):
        super().__init__(f"User with email {email} already exists in the database")

class UserRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, email, name, password_hash, role):
        try:
            self.get_by_email(email)
            raise UserExistsError(email)
        except UserNotFoundError:
            cursor = self._connection_pool.cursor()
            sql = """
                INSERT INTO users(id, email, name, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                    sql,
                    (uuid4(), email, name, password_hash.decode("utf-8"), role),
                    )

            self._connection_pool.commit()
            cursor.close()


    def get_by_email(self, email):
        cursor = self._connection_pool.cursor()
        cursor.execute(
                "SELECT id, email, name, role FROM users WHERE email = %s",
                (email,)
        )
        row = cursor.fetchone()

        if row is None:
            raise UserNotFoundError("email", email)

        (id, email, name, role) = row

        cursor.close()

        return User(id = id, email = email, name = name, role = role)


    def get_password_hash_by_user_id(self, id):
        cursor = self._connection_pool.cursor()
        cursor.execute("SELECT password FROM users WHERE id = %s", (id,))
        row = cursor.fetchone()

        if row is None:
            raise UserNotFoundError("ID", id)

        password_hash = row[0]

        cursor.close()

        return password_hash

    def get(self, id):
        cursor = self._connection_pool.cursor()
        cursor.execute(
                "SELECT id, email, name, role FROM users WHERE id = %s",
                (id,)
        )
        row = cursor.fetchone()

        if row is None:
            raise UserNotFoundError("id", id)

        (id, email, name, role) = row

        cursor.close()

        return User(id = id, email = email, name = name, role = role)
