"""Module contains objects related to data loading"""
import logging

import feedparser


class DataLoader:
    """DataLoader class"""
    def __init__(self, url_source):
        """Init DataLoader class"""
        self.url_source: str = url_source

    def upload(self):
        """Method of loading data from a site by URL"""
        try:
            data = feedparser.parse(self.url_source)

            if data.bozo != 0:
                raise ConnectionError("Incorrect url")

        except Exception as ex:
            logging.error(f'Error connection {ex}', exc_info=False)
        logging.info('Get data by URL')
        return data
