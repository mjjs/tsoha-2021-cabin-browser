class EmptyKeywordError(Exception):
    pass


class KeywordService:
    def __init__(self, keyword_repository):
        self._keyword_repository = keyword_repository

    def add_keyword(self, keyword):
        if len(keyword) == 0:
            raise EmptyKeywordError()

        try:
            return str(self._keyword_repository.add(keyword))
        except:
            return None
