class Repository:
    def __init__(
        self, connection_pool, fields, insertable_fields, table_name, id_field="id"
    ):
        self._connection_pool = connection_pool
        self._fields = fields
        self._insertable_fields = insertable_fields
        self._table_name = table_name
        self._id_field = id_field

    def _get(self, id):
        return self._get_by_field(self._id_field, id)

    def _get_by_field(self, field, value):
        with self._connection_pool.cursor() as cursor:
            fields = ",".join(self._fields)
            sql = f"SELECT {fields} FROM {self._table_name} WHERE {field} = %s"
            cursor.execute(sql, (value,))
            row = cursor.fetchone()

            return row

    def _get_all(self, where_field=None, where_value=None):
        if (where_field and not where_value) or (where_value and not where_field):
            raise ValueError("where_field and where_value both need to be set or None")

        with self._connection_pool.cursor() as cursor:
            fields = ",".join(self._fields)
            sql = f"SELECT {fields} FROM {self._table_name}"
            if where_field:
                sql += f" WHERE {where_field} = %s"
                cursor.execute(sql, (where_value,))
            else:
                cursor.execute(sql)

            rows = cursor.fetchall()

            return rows

    def _add(self, values, returned_field=None):
        with self._connection_pool.cursor() as cursor:
            fields = ",".join(self._insertable_fields)
            placeholders = (len(values) * "%s, ")[:-2]

            sql = f"""
                INSERT INTO {self._table_name} ({fields})
                VALUES ({placeholders})
            """
            if returned_field:
                sql += f" RETURNING {returned_field}"

            cursor.execute(sql, tuple(values))

            if returned_field:
                return cursor.fetchone()[0]

    def _delete(self, id):
        with self._connection_pool.cursor() as cursor:
            sql = f"DELETE FROM {self._table_name} WHERE {self._id_field} = %s"
            cursor.execute(sql, (id,))
