"""
This module contains class for converting parsed data from RSS.
"""
import base64
import textwrap
import functools
import json
import dataclasses
from typing import List
from time import strftime, altzone, mktime, localtime, ctime, time, struct_time

import urllib3

from app.support_files.dtos import Feed
from app.support_files.rss_parser import Parser
from app.support_files.config import APP_NAME
from app.support_files.app_logger import get_logger


def convert_date(date: struct_time) -> str:
    """
    Converts date too human readable format.
    """
    published = localtime(mktime(tuple(date)) - altzone)
    return " ".join([strftime('%a, %d %b %Y %X', published), str(-altzone / 3600)])


def get_templates(template_type: str, template_names: List[str]) -> List[str]:
    """
    Reads templates from files.
    """
    templates = []
    for template_name in template_names:
        with open(f"app/support_files/templates/{template_type}/{template_name}", "r") as main_file:
            templates.append(main_file.read())
    return templates


def get_img_by_url(url: str) -> str:
    """
    Gets img in base64 format by url.
    """
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    return str(base64.b64encode(response.data), "utf-8")


class Converter:
    """
    This class represents format converter for parsed data from RSS.
    """

    def __init__(self, feeds: List[Feed]) -> None:
        """
        :param feeds: Parsed data from RSS.
        """
        self.__feeds = feeds
        self._logger = get_logger(APP_NAME)

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
        """
        Convert data to html format.
        :return: Converted data.
        """
        template_names = ["main", "feed", "item", "image"]
        main_template, feed_template, item_template, image_template = get_templates("html", template_names)
        feed_str_s = []
        for feed in self.__feeds:
            item_str_s = []
            for item in feed.items:
                item_img_links = ["http://view.dreamstalk.ca/breeze5/images/no-photo.png"]
                if item.img_links:
                    item_img_links = item.img_links
                img_str_s = []
                for item_img_link in item_img_links:
                    img_str_s.append(image_template.format(item_img_link=item_img_link))
                item_str_s.append(item_template.format(item_title=item.title,
                                                       item_link=item.link,
                                                       item_author=item.author,
                                                       item_published=convert_date(item.published_parsed),
                                                       item_description=item.description,
                                                       item_images="\n".join(img_str_s)))
            feed_str_s.append(feed_template.format(feed_title=feed.title,
                                                   feed_link=feed.link,
                                                   items="\n".join(item_str_s)))
        result_str = main_template.format(feeds="\n".join(feed_str_s),
                                          title="Feeds")
        return result_str

    def to_fb2_format(self) -> str:
        """
        Convert data to html format.
        :return: Converted data.
        """
        template_names = ["main", "feed", "item", "image", "binary"]
        main_template, feed_template, item_template, image_template, binary_template =\
            get_templates("fb2", template_names)
        feed_str_s = []
        img_content_str_s = []
        img_index = 0
        for feed in self.__feeds:
            item_str_s = []
            for item in feed.items:
                item_img_links = ["http://view.dreamstalk.ca/breeze5/images/no-photo.png"]
                if item.img_links:
                    item_img_links = item.img_links
                img_str_s = []
                for item_img_link in item_img_links[:1]:
                    img_str_s.append(image_template.format(img_index=img_index))
                    self._logger.info(f"Downloading and converting image from {item_img_link} to binary are started")
                    img_content_str_s.append(binary_template.format(img_index=img_index,
                                                                    img_content=get_img_by_url(item_img_link)))
                    self._logger.info(f"Downloading and converting image from {item_img_link} to binary are finished")
                    img_index += 1
                item_str_s.append(item_template.format(item_title=item.title,
                                                       item_link=item.link,
                                                       item_author=item.author,
                                                       item_published=convert_date(item.published_parsed),
                                                       item_description=item.description,
                                                       item_images="\n".join(img_str_s)))
            feed_str_s.append(feed_template.format(feed_title=feed.title,
                                                   feed_link=feed.link,
                                                   items="\n".join(item_str_s)))
        result_str = main_template.format(date=ctime(time()),
                                          feeds="\n".join(feed_str_s),
                                          img_contents="\n".join(img_content_str_s))
        return result_str


if __name__ == "__main__":
    print(Converter([Parser("https://news.yahoo.com/rss/").parse_feed(items_limit=3)]).to_html_format())
