class MunicipalityRepository:
    def __init__(self, connection_pool):
        self._connection_pool = connection_pool
