from datetime import date


class ReservationInPastError(Exception):
    pass


class ReservationConflictError(Exception):
    pass


class ReservationService:
    def __init__(self, reservation_repository, cabin_repository):
        self._reservation_repository = reservation_repository
        self._cabin_repository = cabin_repository

    def get_cabin_reservations(self, cabin_id):
        return self._reservation_repository.get_by_cabin_id(cabin_id)

    def add_reservation(
        self,
        start_date,
        end_date,
        user_id,
        cabin_id,
    ):
        # Check for existing cabin, raises exception if not found
        self._cabin_repository.get(cabin_id)

        current_reservations = self._reservation_repository.get_by_cabin_id(cabin_id)

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        today = date.today()
        if start < today or end < today:
            raise ReservationInPastError()

        for reservation in current_reservations:
            if reservation.start <= start <= reservation.end:
                raise ReservationConflictError()

            if reservation.start <= end <= reservation.end:
                raise ReservationConflictError()

        self._reservation_repository.add(
            start=start,
            end=end,
            user_id=user_id,
            cabin_id=cabin_id,
        )
