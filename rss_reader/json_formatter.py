"""Module with tools for working with Json"""

import json
import logging


class NewsJsonFormatter:
    def __init__(self):
        self.data = {}

    def __str__(self):
        """Compute json-file for print news to console in json-format"""
        logging.info('Compute json-file for print news to console in json-format')

        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def write_to_file(self):
        """Write json-data to file"""
        logging.info('Write json-data to file')

        with open('data.json', 'w', encoding='utf-8') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)

    def format(self, news):
        """Format data to json appereance"""
        logging.info('Format data to json appereance')

        self.data = {
            'feed': []
        }

        for element in news:
            self.data['feed'].append(element)
