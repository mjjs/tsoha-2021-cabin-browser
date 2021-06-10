from repository import Repository


class Reservation:
    def __init__(self, id, start, end, user_id, cabin_id):
        self.id = id
        self.start = start
        self.end = end
        self.user_id = user_id
        self.cabin_id = cabin_id


class ReservationRepository(Repository):
    def __init__(self, connection_pool):
        fields = ["id", "start_date", "end_date", "user_id", "cabin_id"]
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=fields,
            insertable_fields=fields[1:],
            table_name="reservations",
        )

    def add(self, start, end, user_id, cabin_id):
        Repository._add(self=self, values=[start, end, user_id, cabin_id])

    def get_by_cabin_id(self, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = """
            SELECT id, start_date, end_date, user_id, cabin_id FROM reservations
            WHERE cabin_id = %s AND start_date > CURRENT_DATE
            ORDER BY start_date ASC
        """
        cursor.execute(sql, (cabin_id,))
        rows = cursor.fetchall()
        cursor.close()

        reservations = []
        for row in rows:
            (id, start, end, user_id, cabin_id) = row
            reservations.append(Reservation(id, start, end, user_id, cabin_id))

        return reservations
