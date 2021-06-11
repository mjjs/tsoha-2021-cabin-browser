from base64 import b64encode
from .cabin_repository import CabinNotFoundError


class CabinService:
    def __init__(
        self,
        cabin_repository,
        cabin_image_repository,
        reservation_repository,
        keyword_repository,
    ):
        self._cabin_repository = cabin_repository
        self._cabin_image_repository = cabin_image_repository
        self._reservation_repository = reservation_repository
        self._keyword_repository = keyword_repository

    def get_cabin(self, cabin_id):
        try:
            cabin = self._cabin_repository.get(cabin_id)
            cabin.images = self._cabin_image_repository.get_by_cabin_id(cabin.id)
            return cabin
        except CabinNotFoundError:
            return None

    def get_all_cabins(self, for_user=None):
        cabins = []

        if for_user:
            cabins = self._cabin_repository.get_all_by_owner_id(for_user)
        else:
            cabins = self._cabin_repository.get_all()

        for cabin in cabins:
            cabin.images = [
                self._cabin_image_repository.get_default_cabin_image(cabin.id)
            ]
            cabin.reservations = self._reservation_repository.get_by_cabin_id(cabin.id)
            cabin.keywords = self._keyword_repository.get_by_cabin_id(cabin.id)

        return cabins

    def delete_cabin(self, cabin_id, user_id=None):
        cabin = self._cabin_repository.get(cabin_id)

        if not user_id:
            self._cabin_repository.delete(cabin_id)
            return True

        if cabin.owner_id != user_id:
            return False

        self._cabin_repository.delete(cabin_id)
        return True

    def add_cabin(
        self,
        address,
        price,
        description,
        municipality_id,
        name,
        owner_id,
        keywords,
        images,
        default_image_name,
    ):
        # TODO: START TRANSACTION
        price_microcurrency = price * 1_000_000

        try:
            cabin_id = self._cabin_repository.add(
                address,
                price_microcurrency,
                description,
                municipality_id,
                name,
                owner_id,
            )

            for keyword in keywords:
                self._keyword_repository.add_to_cabin(keyword, cabin_id)

            for image in images:
                mimetype = image.mimetype
                b64 = b64encode(image.read()).decode()
                default = default_image_name == image.filename
                self._cabin_image_repository.add(
                    f"{mimetype};base64,{b64}", cabin_id, default
                )

            # TODO: COMMIT TRANSACTION
            return cabin_id
        except:
            # TODO: ROLLBACK TRANSACTION
            return None
