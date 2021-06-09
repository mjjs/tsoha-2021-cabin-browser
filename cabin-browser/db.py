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

extras.register_uuid()

connection_pool = connect(DATABASE_URL)
