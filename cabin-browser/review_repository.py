from review import Review

class ReviewRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, content, rating, user_id, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = """
            INSERT INTO reviews(content, rating, user_id, cabin_id)
            VALUES (%s, %s, %s, %s)
            """

        cursor.execute(sql, (content, rating, user_id, cabin_id))
        self._connection_pool.commit()

        cursor.close()

    def get_by_cabin_id(self, id):
        cursor = self._connection_pool.cursor()
        sql = """
            SELECT id, content, rating, user_id, cabin_id
            FROM reviews
            WHERE cabin_id = %s
            """

        cursor.execute(sql, (id,))
        rows = cursor.fetchall()

        reviews = []
        for (id, content, rating, user_id, cabin_id) in rows:
            reviews.append(Review(id, content, rating, user_id, cabin_id))

        cursor.close()

        return reviews

    def delete_review(self, id):
        cursor = self._connection_pool.cursor()

        sql = "DELETE FROM reviews WHERE id = %s"
        cursor.execute(sql, (id,))

        self._connection_pool.commit()
        cursor.close()
