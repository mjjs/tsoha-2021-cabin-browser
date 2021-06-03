from psycopg2 import IntegrityError
from cabin import Cabin
from municipality import Municipality
from user import User

class CabinExistsError(Exception):
    def __init__(self, address):
        super().__init__(f"Cabin with address {address} already exists in the database")

class CabinNotFoundError(Exception):
    def __init__(self, id):
        super().__init__(f"Cabin with id {id} not found in the database")

class CabinRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, address, price, description, municipality_id, name, owner_id):
        cursor = self._connection_pool.cursor()

        sql = """
            INSERT INTO cabins
            (address, price, description, municipality_id, name, owner_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """

        try:
            cursor.execute(
                sql,
                (address, price, description, municipality_id, name, owner_id),
            )
            self._connection_pool.commit()
            id = cursor.fetchone()[0]
            return id
        except IntegrityError as i:
            raise CabinExistsError(address)
        finally:
            cursor.close()

    def delete(self, id):
        cursor = self._connection_pool.cursor()

        cursor.execute("DELETE FROM cabins WHERE id = %s", (id,))
        self._connection_pool.commit()
        cursor.close()

    def get_all(self):
        cursor = self._connection_pool.cursor()

        sql = """
            SELECT
                c.id, c.name, c.address, c.price, c.description,
                m.name municipality_name,
                (SELECT SUM(rating)/COUNT(rating) FROM reviews WHERE cabin_id = c.id) avg_rating,
                u.id
            FROM cabins c
            LEFT JOIN municipalities m ON m.id = c.municipality_id
            LEFT JOIN users u ON u.id = c.owner_id
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        cabins = []
        for (id, name, address, price, description,
                municipality_name, avg_rating, owner_id) in rows:
            cabins.append(Cabin(
                id = id,
                name = name,
                price = price / 1000000,
                description = description,
                address = address,
                municipality = municipality_name,
                avg_rating = avg_rating,
                owner_id = owner_id,
            ))

        return cabins

    def get_all_by_owner_id(self, owner_id):
        cursor = self._connection_pool.cursor()

        sql = """
            SELECT
                c.id, c.name, c.address, c.price, c.description,
                m.name municipality_name,
                (SELECT SUM(rating)/COUNT(rating) FROM reviews WHERE cabin_id = c.id) avg_rating,
                u.id
            FROM cabins c
            LEFT JOIN municipalities m ON m.id = c.municipality_id
            LEFT JOIN users u ON u.id = c.owner_id
            WHERE c.owner_id = %s
        """

        cursor.execute(sql, (owner_id,))
        rows = cursor.fetchall()

        return [
                Cabin(
                    id = cabin_id,
                    name = cabin_name,
                    price = cabin_price / 1000000,
                    description = cabin_description,
                    address = cabin_address,
                    municipality = municipality_name,
                    avg_rating = avg_rating,
                    owner_id = owner_id,
                )
                for (cabin_id, cabin_name, cabin_address, cabin_price, cabin_description,
                        municipality_name, avg_rating, owner_id) in rows
            ]

    def get(self, id):
        cursor = self._connection_pool.cursor()

        sql = """
            SELECT
                c.id, c.name, c.address, c.price, c.description,
                m.name municipality_name,
                (SELECT SUM(rating)/COUNT(rating) FROM reviews WHERE cabin_id = c.id) avg_rating,
                u.id
            FROM cabins c
            LEFT JOIN municipalities m ON m.id = c.municipality_id
            LEFT JOIN users u ON u.id = c.owner_id
            WHERE c.id = %s
        """

        cursor.execute(sql, (id,))

        row = cursor.fetchone()
        if not row:
            raise CabinNotFoundError(id)

        (cabin_id, cabin_name, cabin_address, cabin_price, cabin_description,
                        municipality_name, avg_rating, owner_id) = row

        return Cabin(
            id = cabin_id,
            name = cabin_name,
            price = cabin_price / 1000000,
            description = cabin_description,
            address = cabin_address,
            municipality = municipality_name,
            avg_rating = avg_rating,
            owner_id = owner_id,
        )
