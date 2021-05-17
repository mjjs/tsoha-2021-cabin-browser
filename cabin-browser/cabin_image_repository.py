class CabinImageRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, filename, cabin_id, is_default):
        cursor = self._connection_pool.cursor()
        sql = "INSERT INTO cabin_images(filename, cabin_id, is_default) VALUES (%s, %s, %s)"
        cursor.execute(sql, (filename, cabin_id, is_default))
        self._connection_pool.commit()
        cursor.close()

    def get_by_cabin_id(self, cabin_id):
        cursor = self._connection_pool.cursor()
        cursor.execute("SELECT filename FROM cabin_images WHERE cabin_id = %s", (cabin_id,))
        rows = cursor.fetchall()
        cursor.close()
        return [r[0] for r in rows] if rows else []

    def get_default_cabin_image(self, cabin_id):
        cursor = self._connection_pool.cursor()
        cursor.execute("SELECT filename FROM cabin_images WHERE cabin_id = %s AND is_default = true", (cabin_id,))
        row = cursor.fetchone()
        cursor.close()
        return row[0] if row else "not_found.png"
