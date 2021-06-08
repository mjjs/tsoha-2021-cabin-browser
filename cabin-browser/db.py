from psycopg2 import connect, extras
from flask import g
from config import DATABASE_URL
from user_repository import UserRepository
from cabin_repository import CabinRepository
from review_repository import ReviewRepository
from cabin_image_repository import CabinImageRepository
from reservation_repository import ReservationRepository
from municipality_repository import MunicipalityRepository
from keyword_repository import KeywordRepository

DATABASE_INIT_FILE = "create_tables.sql"

extras.register_uuid()


def get_db():
    db = getattr(g, "_database", None)

    if not db:
        connection_pool = connect(DATABASE_URL)

        database = Database(connection_pool)

        db = g._database = database

    return db


class Database:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool
        self.user_repository = UserRepository(self._connection_pool)
        self.cabin_repository = CabinRepository(self._connection_pool)
        self.review_repository = ReviewRepository(self._connection_pool)
        self.cabin_image_repository = CabinImageRepository(self._connection_pool)
        self.reservation_repository = ReservationRepository(self._connection_pool)
        self.municipality_repository = MunicipalityRepository(self._connection_pool)
        self.keyword_repository = KeywordRepository(self._connection_pool)

    def close(self):
        self._connection_pool.close()
