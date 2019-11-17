"""Module contains objects related to data loading"""
import feedparser
import logging


class DataLoader:
    """DataLoader class"""
    def __init__(self, url_source):
        """Init DataLoader class"""
        self.url_source = url_source

    def upload(self) -> dict:
        """Method of loading data from a site by URL"""
        try:
            data = feedparser.parse(self.url_source)

            if data.bozo != 0:
                raise ConnectionError("Incorrect url")

        except Exception as ex:
            logging.error('Error connection', exc_info=False)
        logging.info('Get data by URL')
        return data
