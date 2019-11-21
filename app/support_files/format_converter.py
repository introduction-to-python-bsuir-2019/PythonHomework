"""
This module contains class for converting parsed data from RSS.
"""
import textwrap
import functools
import json
import dataclasses
from typing import List
from time import strftime, altzone, mktime, localtime

from app.support_files.dtos import Feed


class Converter:
    """
    This class represents format converter for parsed data from RSS.
    """

    def __init__(self, feeds: List[Feed]) -> None:
        """
        :param feeds: Parsed data from RSS.
        """
        self.__feeds = feeds

    def to_console_format(self, str_len: int = 80) -> str:
        """
        Convert data to console format.
        :param str_len: Length of output strings.
        :return: Converted data.
        """
        strings = []
        out_separator = "*" * str_len
        in_separator = "-" * str_len
        for feed in self.__feeds:
            strings.append(out_separator)
            strings.append(f"Feed: {feed.title}")
            for item in feed.items:
                strings.append(in_separator)
                strings.append(f"Author: {item.author}")
                published = localtime(mktime(tuple(item.published_parsed)) - altzone)
                strings.append(f"Published: {strftime('%a, %d %b %Y %X', published)} {-altzone / 3600}")
                strings.append("\n")
                strings.append(f"Title: {item.title}")
                strings.append(f"Description: {item.description}")
                strings.append("\n")
                strings.append(f"Link: {item.link}")
                strings.append("Image links:")
                for img_link in item.img_links:
                    strings.append(f"{img_link}")
                strings.append(in_separator)
            strings.append(out_separator)

        strings = map(lambda s: textwrap.fill(s, width=str_len) + "\n", strings)

        result_string = functools.reduce(lambda a, b: a + b, strings)

        return result_string

    def to_json_format(self, str_len: int = 80) -> str:
        """
        Convert data to json format.
        :param str_len: Length of output strings.
        :return: Converted data.
        """
        dicts_of_feeds = list(map(dataclasses.asdict, self.__feeds))
        return textwrap.fill(json.dumps(dicts_of_feeds), width=str_len)
