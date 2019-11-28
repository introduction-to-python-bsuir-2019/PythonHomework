"""
This module contains class for parsing RSS.
"""
from typing import Dict, Any

from bs4 import BeautifulSoup
import feedparser

from app.support_files.dtos import Item, Feed
from app.support_files.config import APP_NAME
from app.support_files.app_logger import get_logger

FEED_FIELD_MAPPING = {"title": "title",
                      "link": "link"}

ITEM_FIELD_MAPPING = {"title": "title",
                      "link": "link",
                      "author": "author",
                      "description": "description",
                      "published_parsed": "published_parsed",
                      "media_content": "img_links"}


def apply_field_mapping(field_mapping: Dict[str, str], source: Dict[str, str]) -> Dict[str, Any]:
    return {v: source.get(k) for k, v in field_mapping.items() if source.get(k)}


class Parser:
    """
    This class provides methods to parse RSS.
    """

    def __init__(self, url: str):
        """
        :param url: Url of RSS.
        """
        self.url = url
        self._logger = get_logger(APP_NAME)

    def parse_feed(self, items_limit: int = -1) -> Feed:
        """
        Parse the RSS file.
        :param items_limit: Limit count of returned items.
        """
        self._logger.info(f"Reading {self.url} is started")
        data = feedparser.parse(self.url)
        if data.bozo != 0:
            raise ConnectionError("Some problems with connection")
        if data.status != 200:
            raise ConnectionError("Invalid url")
        self._logger.info(f"Reading {self.url} is finished")
        self._logger.info("Converting read data to standard form is started")
        feed = data.get("feed", {})
        feed_data = apply_field_mapping(FEED_FIELD_MAPPING, feed)
        feed_data["rss_link"] = self.url
        items_data = [apply_field_mapping(ITEM_FIELD_MAPPING, item)
                      for item in data.get("entries", [])[:items_limit]]
        for item_data in items_data:
            soup = BeautifulSoup(item_data.get("description", ""), 'html.parser')
            item_data["description"] = soup.text
            item_data["img_links"] = [item["url"] for item in item_data.get("img_links", [])]

        feed = Feed(**feed_data)
        feed.items = [Item(**item_data) for item_data in items_data]
        self._logger.info("Converting read data to standard form is finished")
        return feed


if __name__ == "__main__":
    parser = Parser("http://www.bbc.co.uk/music/genres/classical/reviews.rss")
    print(parser.parse_feed(2))
