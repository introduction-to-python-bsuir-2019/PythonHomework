class FatalError(Exception):
    """An error in which we forcefully terminate the program"""
    def __init__(self, text):
        self.__str__ = text
