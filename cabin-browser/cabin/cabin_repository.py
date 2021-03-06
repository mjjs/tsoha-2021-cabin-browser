from psycopg2 import IntegrityError
from repository import Repository


class Cabin:
    def __init__(
        self,
        id,
        name,
        address,
        price,
        description,
        municipality,
        avg_rating,
        owner_id,
        images=[],
    ):
        self.id = id
        self.name = name
        self.address = address
        self.price = price
        self.description = description
        self.municipality = municipality
        self.avg_rating = avg_rating
        self.owner_id = owner_id
        self.images = images


class CabinExistsError(Exception):
    def __init__(self, address):
        super().__init__(f"Cabin with address {address} already exists in the database")


class CabinNotFoundError(Exception):
    def __init__(self, id):
        super().__init__(f"Cabin with id {id} not found in the database")


class CabinRepository(Repository):
    def __init__(self, connection_pool):
        fields = [
            "id",
            "name",
            "address",
            "price",
            "description",
            "municipality_id",
            "owner_id",
        ]
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=fields,
            insertable_fields=fields[1:],
            table_name="cabins",
        )

    def add(self, address, price, description, municipality_id, name, owner_id):
        try:
            return Repository._add(
                self=self,
                values=[name, address, price, description, municipality_id, owner_id],
                returned_field="id",
            )
        except IntegrityError:
            raise CabinExistsError(address)

    def delete(self, id):
        Repository._delete(self, id)

    def get_all(self):
        with self._connection_pool.cursor() as cursor:
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
            for (
                id,
                name,
                address,
                price,
                description,
                municipality_name,
                avg_rating,
                owner_id,
            ) in rows:
                cabins.append(
                    Cabin(
                        id=id,
                        name=name,
                        price=price / 1000000,
                        description=description,
                        address=address,
                        municipality=municipality_name,
                        avg_rating=avg_rating,
                        owner_id=owner_id,
                    )
                )

            return cabins

    def get_all_by_owner_id(self, owner_id):
        with self._connection_pool.cursor() as cursor:
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
                    id=cabin_id,
                    name=cabin_name,
                    price=cabin_price / 1000000,
                    description=cabin_description,
                    address=cabin_address,
                    municipality=municipality_name,
                    avg_rating=avg_rating,
                    owner_id=owner_id,
                )
                for (
                    cabin_id,
                    cabin_name,
                    cabin_address,
                    cabin_price,
                    cabin_description,
                    municipality_name,
                    avg_rating,
                    owner_id,
                ) in rows
            ]

    def get(self, id):
        with self._connection_pool.cursor() as cursor:
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

            (
                cabin_id,
                cabin_name,
                cabin_address,
                cabin_price,
                cabin_description,
                municipality_name,
                avg_rating,
                owner_id,
            ) = row

            return Cabin(
                id=cabin_id,
                name=cabin_name,
                price=cabin_price / 1000000,
                description=cabin_description,
                address=cabin_address,
                municipality=municipality_name,
                avg_rating=avg_rating,
                owner_id=owner_id,
            )
