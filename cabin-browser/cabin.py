class Cabin:
    def __init__(self, id, name, address, price,
            description, municipality, avg_rating,
            owner_id, images = []):
        self.id = id
        self.name = name
        self.address = address
        self.price = price
        self.description = description
        self.municipality = municipality
        self.avg_rating = avg_rating
        self.owner_id = owner_id
        self.images = images
