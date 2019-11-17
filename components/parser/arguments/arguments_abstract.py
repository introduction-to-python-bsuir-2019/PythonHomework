from abc import ABC, abstractmethod


class ArgumentsAbstract(ABC):

    # @property
    # def _parser(self):
    #     return self._parser

    def __init__(self, parser):
        self._parser = parser

    @abstractmethod
    def add_argument(self):
        pass
