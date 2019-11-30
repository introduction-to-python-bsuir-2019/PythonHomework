"""Articles cache module"""

import logging
import json

from os.path import abspath, getsize

from .article import Article
from .json_format import Json


class ArticlesCacher:
    logger = logging.getLogger('__main__.py')

    def __init__(self, file_name, source, date):
        self.file = None
        self.file_name = file_name
        self.source = source
        self.date = date

    def cache(self, json_object):
        data = {}
        data[self.source] = {}
        data[self.source][self.date] = []
        
        try:
            file_size = getsize(abspath(self.file_name))
        except FileNotFoundError:
            file_size = 0
            with open(self.file_name, 'w+', encoding='utf-8'):
                pass

        if file_size != 0:
            with open(self.file_name, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

        if self.source not in data.keys():
            data.update({self.source: dict()})
        if self.date not in data[self.source].keys():
            data[self.source].update({self.date: list()})

        for element in json_object:
            if element not in data[self.source][self.date]:
            # element_exist = False
            # for _, value in data[self.source].items():
            #     if element in value:
            #         element_exist = True
            #         break
            # if element_exist == False:
                data[self.source][self.date].append(element)

        with open(self.file_name, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
