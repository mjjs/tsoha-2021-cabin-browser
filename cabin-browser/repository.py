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

    def _get_all(self):
        cursor = self._connection_pool.cursor()
        fields = ",".join(self._fields)
        sql = f"SELECT {fields} FROM {self._table_name}"
        cursor.execute(sql)

        rows = cursor.fetchall()
        cursor.close()

        return rows

    def _add(self, values):
        cursor = self._connection_pool.cursor()
        fields = ",".join(self._insertable_fields)
        placeholders = (len(values) * "%s, ")[:-2]

        sql = f"INSERT INTO {self._table_name} ({fields}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(values))

        cursor.close()
