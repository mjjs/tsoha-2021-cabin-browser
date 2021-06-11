from repository import Repository


class Municipality:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MunicipalityRepository(Repository):
    def __init__(self, connection_pool):
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=["id", "name"],
            insertable_fields=["name"],
            table_name="municipalities",
        )

    def get_all(self):
        rows = Repository._get_all(self)
        return [Municipality(id, name) for (id, name) in rows]

    def get_all_used(self):
        with self._connection_pool.cursor() as cursor:
            sql = """
                SELECT id, name FROM municipalities WHERE id IN
                (SELECT municipality_id FROM cabins GROUP BY municipality_id)
            """

            cursor.execute(sql)
            rows = cursor.fetchall()

            return [Municipality(id, name) for (id, name) in rows]
