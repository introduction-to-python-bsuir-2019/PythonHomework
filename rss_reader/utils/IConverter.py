from abc import ABCMeta, abstractmethod
import logging

from ..utils.data_structures import NewsItem, News, ConsoleArgs


class IConverter(metaclass=ABCMeta):
    """Interface for converters"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.logger.debug(f'Init Converter {self.__class__} completed')

    @abstractmethod
    def store_news(self, news: News, file_path: str) -> None:
        """Method to store news"""
