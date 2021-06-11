from psycopg2 import IntegrityError
from repository import Repository


class Keyword:
    def __init__(self, id, keyword):
        self.id = id
        self.keyword = keyword


class KeywordExistsError(Exception):
    def __init__(self, keyword):
        super().__init__(f"The keyword {keyword} already exists in the database")


class KeywordRepository(Repository):
    def __init__(self, connection_pool):
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=["id", "keyword"],
            insertable_fields=["keyword"],
            table_name="keywords",
        )

    def add(self, keyword):
        try:
            return Repository._add(self=self, values=[keyword], returned_field="id")
        except IntegrityError:
            raise KeywordExistsError(keyword)

    def get_all(self):
        rows = Repository._get_all(self)
        return [Keyword(id, keyword) for (id, keyword) in rows]

    def get_all_used(self):
        with self._connection_pool.cursor() as cursor:
            sql = """
                SELECT kw.id, kw.keyword FROM keywords kw
                WHERE kw.id IN (SELECT keyword_id FROM cabins_keywords)
                """
            cursor.execute(sql)
            rows = cursor.fetchall()

            return [Keyword(id, keyword) for (id, keyword) in rows]

    def get_by_cabin_id(self, cabin_id):
        with self._connection_pool.cursor() as cursor:
            sql = """
                SELECT kw.id, kw.keyword FROM keywords kw
                LEFT JOIN cabins_keywords ck ON (ck.keyword_id = kw.id)
                WHERE ck.cabin_id = %s
            """
            cursor.execute(sql, (cabin_id,))
            rows = cursor.fetchall()

            return [Keyword(id, keyword) for (id, keyword) in rows]

    def add_to_cabin(self, keyword_id, cabin_id):
        with self._connection_pool.cursor() as cursor:
            sql = "INSERT INTO cabins_keywords(keyword_id, cabin_id) VALUES (%s, %s)"
            cursor.execute(sql, (keyword_id, cabin_id))
