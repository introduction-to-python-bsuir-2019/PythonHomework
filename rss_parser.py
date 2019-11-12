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

    def __init__(self, url):
        self.url = url

    def parse_feed(self, items_count=-1):
        d = feedparser.parse(self.url)
        if d.status != 200:
            return None
        feed = d.get("feed", {})
        result_data = Parser.__apply_field_mapping(FEED_FIELD_MAPPING, feed)
        items = [Parser.__apply_field_mapping(ITEM_FIELD_MAPPING, item)
                 for item in d.get("entries", [])[:items_count]]
        for item in items:
            soup = BeautifulSoup(item["item_description"], 'html.parser')
            item_img_link = soup.find("img").get("src")
            if not item_img_link:
                item_img_link = None
            item["item_img_link"] = item_img_link
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
