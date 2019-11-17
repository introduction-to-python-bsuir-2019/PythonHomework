"""JSON converting module"""

import json
import codecs
import logging


class JsonFormat:
    logger = logging.getLogger('__main__.py')

    def __init__(self):
        pass

    def format(self, data):
        """Format file to JSON-format"""
        self.logger.info('Creation and filling JSON-file')

        json_data = {}
        json_data['feed'] = []

        for element in data:
            json_data['feed'].append(element)

        with codecs.open('data.json', 'w', encoding='utf-8') as outfile:
            json.dump(json_data, outfile, ensure_ascii=False, indent=4)
