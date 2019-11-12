"""
This module contains class for parsing RSS.
"""
import feedparser
from bs4 import BeautifulSoup

FEED_FIELD_MAPPING = {"title": "feed_title",
                      "link": "feed_link"}

ITEM_FIELD_MAPPING = {"title": "item_title",
                      "link": "item_link",
                      "author": "item_author",
                      "description": "item_description",
                      "published": "item_date"}


class Parser:
    """
    This class provides methods to parse RSS.
    """
    def __init__(self, url):
        """
        :param url: Url of RSS.
        """
        self.url = url

    def parse_feed(self, items_limit=-1):
        """
        Parse the RSS file.
        :param items_limit: Limit count of returned items
        :return: Dict with parsed data.
        """
        data = feedparser.parse(self.url)
        if data.bozo != 0 or data.status != 200:
            return None
        feed = data.get("feed", {})
        result_data = Parser.__apply_field_mapping(FEED_FIELD_MAPPING, feed)
        items = [Parser.__apply_field_mapping(ITEM_FIELD_MAPPING, item)
                 for item in data.get("entries", [])[:items_limit]]
        for item in items:
            soup = BeautifulSoup(item["item_description"], 'html.parser')
            item["item_img_links"] = [link.get("src") for link in soup.find_all("img") if link.get("src")]
            item["item_description"] = soup.text

        result_data["items"] = items
        return result_data

    @staticmethod
    def __apply_field_mapping(field_mapping, source):
        data = {}
        for key in field_mapping:
            data[field_mapping[key]] = source.get(key)
        return data


if __name__ == "__main__":
    parser = Parser("https://news.tut.by/rss/economics.rss")
    print(parser.parse_feed(2))
