from enum import Enum
from db import commit_transaction
from cabin.cabin_repository import CabinNotFoundError


class ReviewService:
    def __init__(self, review_repository, cabin_repository):
        self._review_repository = review_repository
        self._cabin_repository = cabin_repository

    def add_review(self, rating, content, user_id, cabin_id):
        self._review_repository.add(
            content=content,
            rating=rating,
            user_id=user_id,
            cabin_id=cabin_id,
        )
        commit_transaction()

    def delete_review(self, cabin_id, review_id, current_user_id):
        try:
            cabin = self._cabin_repository.get(cabin_id)
            review = self._review_repository.get(review_id)

            if current_user_id in (cabin.owner_id, review.user_id):
                self._review_repository.delete_review(review_id)
                commit_transaction()

                return True

            return False
        except CabinNotFoundError:
            return False
