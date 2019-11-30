from abc import ABC, abstractmethod


class ArgumentsAbstract(ABC):

    def __init__(self, parser):
        self._parser = parser

    @abstractmethod
    def add_argument(self):
        pass
