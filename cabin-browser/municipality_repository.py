class Municipality:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class MunicipalityRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def get_all(self):
        cursor = self._connection_pool.cursor()
        cursor.execute("SELECT id, name FROM municipalities")
        rows = cursor.fetchall()

        return [Municipality(id, name) for (id, name) in rows]

    def get_all_used(self):
        cursor = self._connection_pool.cursor()
        sql = """
            SELECT id, name FROM municipalities WHERE id IN
            (SELECT municipality_id FROM cabins GROUP BY municipality_id)
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        return [Municipality(id, name) for (id, name) in rows]
