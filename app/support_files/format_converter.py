"""
This module contains class for converting parsed data from RSS.
"""
import textwrap
import functools
import json


class Converter:
    """
    This class represents format converter for parsed data from RSS.
    """
    def __init__(self, feeds):
        """
        :param feeds: Parsed data from RSS.
        """
        self.__feeds = feeds

    def to_console_format(self, str_len=80):
        """
        Convert data to console format.
        :param str_len: Length of output strings.
        :return: Converted data.
        """
        strings = []
        for feed in self.__feeds:
            strings.append(f"Feed: {feed.get('feed_title')}")
            for item in feed.get("items", []):
                strings.append("-" * str_len)
                strings.append(f"Author: {item.get('item_author')}")
                strings.append(f"Date: {item.get('item_date')}")
                strings.append("\n")
                strings.append(f"Title: {item.get('item_title')}")
                strings.append(f"Description: {item.get('item_description')}")
                strings.append("\n")
                strings.append(f"Link: {item.get('item_link')}")
                strings.append("Image links:")
                for img_link in item.get('item_img_links'):
                    strings.append(f"{img_link}")
                strings.append("-" * str_len)
                strings.append("\n")
        strings.pop()

        strings = map(lambda s: textwrap.fill(s, width=str_len) + "\n", strings)

        result_string = "-" * str_len + "\n"
        result_string += functools.reduce(lambda a, b: a + b, strings)

        return result_string

    def to_json_format(self, str_len=80):
        """
        Convert data to json format.
        :param str_len: Length of output strings.
        :return: Converted data.
        """
        return textwrap.fill(json.dumps(self.__feeds, ensure_ascii=False), width=str_len)
