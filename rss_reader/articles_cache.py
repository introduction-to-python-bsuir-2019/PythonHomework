"""News cacher module"""

import logging
import json

from datetime import datetime
from os.path import abspath, getsize

from .article import Article
from .json_format import Json


class NewsCacher:
    logger = logging.getLogger('__main__.py')

    def __init__(self, file_name, source):
        self.file = None
        self.file_name = file_name
        self.source = source
        self.date = str(datetime.date(datetime.now())).replace('-', '')
        self.data = None

    def get_cached_news(self, date, limit):
        """Get cached news from json file"""

        with open(self.file_name, 'r', encoding='utf-8') as json_file:
            self.data = json.load(json_file)

        try:
            return self.data[self.source][date][:limit]
        except (KeyError, TypeError):
            return []

    def cache(self, json_object):
        """Cache news to json file"""

        self.data = {}
        self.data[self.source] = {}
        self.data[self.source][self.date] = []
        
        try:
            file_size = getsize(abspath(self.file_name))
        except FileNotFoundError:
            file_size = 0
            open(self.file_name, 'w').close()

        if file_size != 0:
            with open(self.file_name, 'r', encoding='utf-8') as json_file:
                self.data = json.load(json_file)

        if self.source not in self.data.keys():
            self.data.update({self.source: dict()})
        if self.date not in self.data[self.source].keys():
            self.data[self.source].update({self.date: list()})

        for element in json_object:
            if element not in self.data[self.source][self.date]:
                self.data[self.source][self.date].append(element)

        with open(self.file_name, 'w', encoding='utf-8') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)
