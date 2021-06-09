from psycopg2 import connect, extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import DATABASE_URL

extras.register_uuid()

connection_pool = connect(DATABASE_URL)
connection_pool.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
