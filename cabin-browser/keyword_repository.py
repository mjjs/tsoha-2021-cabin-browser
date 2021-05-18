from psycopg2 import IntegrityError

class Keyword:
    def __init__(self, id, keyword):
        self.id = id
        self.keyword = keyword

class KeywordExistsError(Exception):
    def __init__(self, keyword):
        super().__init__(f"The keyword {keyword} already exists in the database")

class KeywordRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool

    def add(self, keyword):
        try:
            cursor = self._connection_pool.cursor()
            sql = "INSERT INTO keywords(keyword) VALUES (%s) RETURNING id"
            cursor.execute(sql, (keyword,))
            self._connection_pool.commit()

            row = cursor.fetchone()
            cursor.close()

            return row[0]
        except IntegrityError:
            raise KeywordExistsError(keyword)

    def add_to_cabin(self, keyword_id, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = "INSERT INTO cabins_keywords(keyword_id, cabin_id) VALUES (%s, %s)"
        cursor.execute(sql, (keyword_id, cabin_id))
        self._connection_pool.commit()
        cursor.close()

    def get_all(self):
        cursor = self._connection_pool.cursor()
        sql = "SELECT id, keyword FROM keywords"
        cursor.execute(sql)
        rows = cursor.fetchall()

        return [Keyword(id, keyword) for (id, keyword) in rows]

    def get_by_cabin_id(self, cabin_id):
        cursor = self._connection_pool.cursor()
        sql = """
            SELECT kw.id, kw.keyword FROM keywords kw
            LEFT JOIN cabins_keywords ck ON (ck.keyword_id = kw.id)
            WHERE ck.cabin_id = %s
        """
        cursor.execute(sql, (cabin_id,))
        rows = cursor.fetchall()

        return [Keyword(id, keyword) for (id, keyword) in rows]
