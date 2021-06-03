from reservation import Reservation

class ReservationRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, start, end, user_id, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = """
            INSERT INTO reservations(start_date, end_date, user_id, cabin_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (start, end, user_id, cabin_id))
        self._connection_pool.commit()
        cursor.close()

    def get_by_cabin_id(self, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = """
            SELECT id, start_date, end_date, user_id, cabin_id FROM reservations
            WHERE cabin_id = %s
        """
        cursor.execute(sql, (cabin_id,))
        rows = cursor.fetchall()
        cursor.close()

        reservations = []
        for row in rows:
            (id, start, end, user_id, cabin_id) = row
            reservations.append(Reservation(id, start, end, user_id, cabin_id))

        return reservations
