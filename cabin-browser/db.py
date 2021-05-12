from psycopg2 import connect, extras
from flask import g
from config import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from user_repository import UserRepository

DATABASE_INIT_FILE = "create_tables.sql"

extras.register_uuid()

def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        connection_pool = connect(
                database = DATABASE_NAME,
                user = DATABASE_USERNAME,
                password = DATABASE_PASSWORD,
                host = DATABASE_HOST,
                port = DATABASE_PORT,
                )

        database = Database(connection_pool)

        db = g._database = database

    return db

class Database:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool
        self.user_repository = UserRepository(self._connection_pool)

    def close(self):
        self._connection_pool.close()

    #def initialize(self):
    #    print("Initializing database")
    #    create_tables_sql_file = open(DATABASE_INIT_FILE, "r")
    #    sql = create_tables_sql_file.read()
    #    create_tables_sql_file.close()

    #    cursor = self._db.cursor()
    #    cursor.executescript(sql)
    #    self._db.commit()
    #    cursor.close()
    #    print("Database initialized")
