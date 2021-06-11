from repository import Repository


class CabinImageRepository(Repository):
    def __init__(self, connection_pool):
        fields = ["id", "data", "cabin_id", "is_default"]
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=fields,
            insertable_fields=fields[1:],
            table_name="cabin_images",
        )

    def add(self, data, cabin_id, is_default):
        Repository._add(self=self, values=[data, cabin_id, is_default])

    def get(self, id):
        row = Repository._get(self, id)
        if not row:
            return None

        (_, data, _, _) = row
        return data

    def get_by_cabin_id(self, cabin_id):
        rows = Repository._get_all(
            self=self, where_field="cabin_id", where_value=cabin_id
        )
        return [data for (_, data, _, _) in rows] if rows else ["not_found.png"]

    def get_default_cabin_image(self, cabin_id):
        with self._connection_pool.cursor() as cursor:
            cursor.execute(
                "SELECT data FROM cabin_images WHERE cabin_id = %s AND is_default = true",
                (cabin_id,),
            )
            row = cursor.fetchone()
            return row[0] if row else "not_found.png"
