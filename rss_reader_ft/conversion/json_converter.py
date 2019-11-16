import json
import logging as log

from conversion.format_converter import FormatConverter


class JsonConverter(FormatConverter):
    def __init__(self, rss_feed_dict):
        self.convert_data = rss_feed_dict
        log.info(f'Init class JsonConverter')

    def convert_rss_to_format(self):
        print(json.dumps(self.convert_data, indent=4))
        log.info(f'The convert_rss_to_format method worked')
