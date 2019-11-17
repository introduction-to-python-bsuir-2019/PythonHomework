"""Module contains objects related to converted"""
from abc import ABC, abstractmethod


class FormatConverter(ABC):
    """FormatConverter abstract class"""
    @abstractmethod
    def convert_to_format(self):
        pass
