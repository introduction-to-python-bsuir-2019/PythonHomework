import logging as log
from abc import ABC, abstractmethod


class FormatConverter(ABC):
    def __init__(self):
        log.info(f'Init class FormatConverter')

    @abstractmethod
    def convert_rss_to_format(self, news):
        pass
