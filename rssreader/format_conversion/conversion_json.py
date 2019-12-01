"""Conversion module to json"""

import json
import logging

from rssreader.parser import feed_parser


class JsonConversion(feed_parser.RssParser):
    """Class that converts rss to json"""
    def __init__(self, url: str, limit=None) -> None:
        """Сalls the parser constructor to process the limit"""
        super().__init__(url, limit)

    def convert_to_json(self, data_parsing) -> str:
        """Method that converts rss to json"""
        result = json.dumps(data_parsing, indent=4, ensure_ascii=False)
        logging.info("Show result of json conversion")
        return result if result != "[]" else ""
