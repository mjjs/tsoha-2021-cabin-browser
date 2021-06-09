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
        cursor = self._connection_pool.cursor()
        fields = ",".join(self._fields)
        sql = f"SELECT {fields} FROM {self._table_name} WHERE {field} = %s"
        cursor.execute(sql, (value,))
        row = cursor.fetchone()
        cursor.close()

        return row

    def _get_all(self, where_field=None, where_value=None):
        if (where_field and not where_value) or (where_value and not where_field):
            raise ValueError("where_field and where_value both need to be set or None")

        cursor = self._connection_pool.cursor()
        fields = ",".join(self._fields)
        sql = f"SELECT {fields} FROM {self._table_name}"
        if where_field:
            sql += f" WHERE {where_field} = %s"
            cursor.execute(sql, (where_value,))
        else:
            cursor.execute(sql)

        rows = cursor.fetchall()
        cursor.close()

        return rows

    def _add(self, values, returned_field=None):
        ret_field = self._id_field if not returned_field else returned_field
        cursor = self._connection_pool.cursor()
        fields = ",".join(self._insertable_fields)
        placeholders = (len(values) * "%s, ")[:-2]

        sql = f"INSERT INTO {self._table_name} ({fields}) VALUES ({placeholders}) RETURNING {ret_field}"
        cursor.execute(sql, tuple(values))

        retval = cursor.fetchone()[0]

        cursor.close()

        return retval

    def _delete(self, id):
        cursor = self._connection_pool.cursor()
        sql = f"DELETE FROM {self._table_name} WHERE {self._id_field} = %s"
        cursor.execute(sql, (id,))
        cursor.close()
