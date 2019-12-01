"""Module contains objects related to JSON"""
import json
import logging
from typing import Dict, Any

from rss_reader_ft.conversion.format_converter import FormatConverter


class JsonConverter(FormatConverter):
    """
    JsonConverter class
    inherited from FormatConverter abstract class.
    """
    def __init__(self, rss_feed_dict: Dict[str, Any]):
        """Init JsonConverter class"""
        self.convert_data = rss_feed_dict

    def convert_to_format(self) -> str:
        """Сonversion method to JSON format"""
        logging.info('Convert data to JSON and return it')

        return json.dumps(self.convert_data, indent=4, ensure_ascii=False)
