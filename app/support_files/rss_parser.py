"""
This module contains class for parsing RSS.
"""
from typing import Dict, Any

from bs4 import BeautifulSoup
import feedparser

from app.support_files.dtos import Item, Feed

FEED_FIELD_MAPPING = {"title": "title",
                      "link": "link"}

ITEM_FIELD_MAPPING = {"title": "title",
                      "link": "link",
                      "author": "author",
                      "description": "description",
                      "published_parsed": "published_parsed"}


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

    def parse_feed(self, items_limit: int = -1) -> Feed:
        """
        Parse the RSS file.
        :param items_limit: Limit count of returned items.
        """
        data = feedparser.parse(self.url)
        if data.bozo != 0:
            raise ConnectionError("Some problems with connection")
        if data.status != 200:
            raise ConnectionError("Invalid url")
        feed = data.get("feed", {})
        feed_data = apply_field_mapping(FEED_FIELD_MAPPING, feed)
        feed_data["rss_link"] = self.url
        items_data = [apply_field_mapping(ITEM_FIELD_MAPPING, item)
                      for item in data.get("entries", [])[:items_limit]]
        for item_data in items_data:
            soup = BeautifulSoup(item_data["description"], 'html.parser')
            item_data["img_links"] = [link.get("src") for link in soup.find_all("img") if link.get("src")]
            item_data["description"] = soup.text

        feed = Feed(**feed_data)
        feed.items = [Item(**item_data) for item_data in items_data]
        return feed


if __name__ == "__main__":
    parser = Parser("https://news.tut.by/rss/economics.rss")
    print(parser.parse_feed(2))
