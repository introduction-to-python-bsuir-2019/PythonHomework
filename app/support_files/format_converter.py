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
from app.support_files.rss_parser import Parser


def convert_date(date):
    published = localtime(mktime(tuple(date)) - altzone)
    return " ".join([strftime('%a, %d %b %Y %X', published), str(-altzone / 3600)])


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
                strings.append(f"Published: {convert_date(item.published_parsed)}")
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

    def to_html_format(self) -> str:
        with open("templates/html/main", "r") as main_file:
            main_template = main_file.read()
        with open("templates/html/feed", "r") as feed_file:
            feed_template = feed_file.read()
        with open("templates/html/item", "r") as item_file:
            item_template = item_file.read()
        feed_str_s = []
        for feed in self.__feeds:
            item_str_s = []
            for item in feed.items:
                item_img = "http://view.dreamstalk.ca/breeze5/images/no-photo.png"
                try:
                    kek = item.img_links[0]
                except IndexError:
                    pass
                item_str_s.append(item_template.format(item_title=item.title,
                                                       item_link=item.link,
                                                       item_author=item.author,
                                                       item_published=convert_date(item.published_parsed),
                                                       item_description=item.description,
                                                       item_img=item_img))
            feed_str_s.append(feed_template.format(feed_title=feed.title,
                                                   feed_link=feed.link,
                                                   items="\n".join(item_str_s)))
        result_str = main_template.format(feeds="\n".join(feed_str_s))
        return result_str


if __name__ == "__main__":
    parser = Parser("https://news.yahoo.com/rss/")
    converter = Converter([parser.parse_feed(items_limit=3)])
    print(converter.to_html_format())
