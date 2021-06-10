from repository import Repository


class Review:
    def __init__(self, id, content, rating, user_id, cabin_id):
        self.id = id
        self.content = content
        self.rating = rating
        self.user_id = user_id
        self.cabin_id = cabin_id


class ReviewNotFoundError(Exception):
    def __init__(self, id):
        super().__init__(f"Review with id {id} not found in the database")


class ReviewRepository(Repository):
    def __init__(self, connection_pool):
        fields = ["id", "content", "rating", "user_id", "cabin_id"]
        Repository.__init__(
            self=self,
            connection_pool=connection_pool,
            fields=fields,
            insertable_fields=fields[1:],
            table_name="reviews",
        )

    def add(self, content, rating, user_id, cabin_id):
        Repository._add(self, [content, rating, user_id, cabin_id])

    def get(self, id):
        row = Repository._get(self, id)
        if not row:
            raise ReviewNotFoundError(id)

        (id, content, rating, user_id, cabin_id) = row
        return Review(id, content, rating, user_id, cabin_id)

    def get_by_cabin_id(self, id):
        rows = Repository._get_all(self=self, where_field="cabin_id", where_value=id)
        reviews = [
            Review(id, content, rating, user_id, cabin_id)
            for (id, content, rating, user_id, cabin_id) in rows
        ]

        return reviews

    def delete_review(self, id):
        Repository._delete(self, id)
