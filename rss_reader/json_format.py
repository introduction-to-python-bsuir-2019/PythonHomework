"""Module with tools for working with Json"""

import json
import codecs
import logging


class Json:
    logger = logging.getLogger('__main__.py')

    def __init__(self):
        self.data = {}
    
    def __str__(self):
        """Print JSON-file to console"""
        self.logger.info('Print JSON-data to console')

        return json.dumps(self.data, ensure_ascii=False, indent=4)

    # def print(self):
    #     """Print JSON-file to console"""
    #     self.logger.info('Print JSON-data to file')

        print(json.dumps(self.data, ensure_ascii=False, indent=4))

    def write_to_file(self):
        """Write JSON-data to file"""
        self.logger.info('Write JSON-data to file')

        with codecs.open('data.json', 'w', encoding='utf-8') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)

    def format(self, data):
        """Format file to JSON-format"""
        self.logger.info('Format data to JSON appereance')

        self.data = {}
        self.data['feed'] = []

        for element in data:
            self.data['feed'].append(element)
