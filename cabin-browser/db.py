from psycopg2 import connect, extras
from config import DATABASE_URL

extras.register_uuid()

connection_pool = connect(DATABASE_URL)


def commit_transaction():
    connection_pool.commit()


def rollback_transaction():
    connection_pool.rollback()
