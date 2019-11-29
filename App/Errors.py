class FatalError(Exception):
    def __init__(self, text):
        self.__str__ = text