from municipality import Municipality

class MunicipalityRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def get_all(self):
        cursor = self._connection_pool.cursor()
        cursor.execute("SELECT id, name FROM municipalities")
        rows = cursor.fetchall()

        return [Municipality(id, name) for (id, name) in rows]
