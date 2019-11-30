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
from colored import fg, bg, attr

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


def set_length(str_len: str):
    """
    Makes text the same length wide,
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            text = textwrap.fill(args[0], width=str_len)
            result = func(text, *args[1:], **kwargs)
            return result
        return wrapper
    return decorator


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

    def to_console_format(self, str_len: int = 80, col_en: bool = False) -> str:
        """
        Convert data to console format.
        :param col_en: Enable colorizing, if true.
        :param str_len: Length of output strings.
        :return: Converted data.
        """
        @set_length(str_len)
        def set_color(text: str, text_color: str, enabled: bool) -> str:
            """
            Changes the text_color of the text if enabled is true.
            :return: Colorized text.
            """
            color_str = ""
            reset = ""
            if enabled:
                color_str = f"{fg(text_color)}"
                reset = f" {attr('reset')}"
            return color_str + text + reset
        strings = []
        out_separator = set_color(f"{'*' * str_len}", "green_4", col_en)
        in_separator = set_color(f"{'-' * str_len}", "chartreuse_3b", col_en)
        for feed in self.__feeds:
            strings.append(out_separator)
            strings.append(set_color(f"Feed: {feed.title}", "gold_1", col_en))
            for item in feed.items:
                strings.append(in_separator)
                strings.append(set_color(f"Author: {item.author}", "light_green_3", col_en))
                strings.append(set_color(f"Published: {convert_date(item.published_parsed)}", "light_cyan_1", col_en))
                strings.append("\n")
                strings.append(set_color("Title:", "yellow_3a", col_en))
                strings.append(set_color(f"\t{item.title}", "gold_1", col_en))
                strings.append("\n")
                strings.append(set_color("Description:", "yellow_3a", col_en))
                strings.append(set_color(f"\t{item.description}", "light_green_3", col_en))
                strings.append("\n")
                strings.append(set_color("Link:", "yellow_3a", col_en))
                strings.append(set_color(f"\t{item.link}", "wheat_1", col_en))
                strings.append(set_color("Image links:", "yellow_3a", col_en))
                for img_link in item.img_links:
                    strings.append(set_color(f"\t{img_link}", "light_cyan_1", col_en))
                strings.append(in_separator)
            strings.append(out_separator)

        strings = map(lambda s: s + "\n", strings)

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
    print(Converter([Parser("https://news.yahoo.com/rss/").parse_feed(items_limit=1)]).
          to_console_format(col_en=True, str_len=120))
