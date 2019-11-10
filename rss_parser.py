import feedparser

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

    def parse_feed(self, items=-1):
        d = feedparser.parse(self.url)
        feed = d.get("feed", default={})
        feed_data = Parser.__apply_field_mapping(FEED_FIELD_MAPPING, feed)
        result_items = []
        for item in d.get("entries")[:items]:
            item_data = Parser.__apply_field_mapping(ITEM_FIELD_MAPPING, item)
            result_item = {}
            result_item.update(feed_data)
            result_item.update(item_data)
            result_items.append(result_item)
        return result_items

    @staticmethod
    def __apply_field_mapping(field_mapping, source):
        data = {}
        for key in field_mapping:
            data[field_mapping[key]] = source.get(key)
        return data


if __name__ == "__main__":
    parser = Parser("https://news.tut.by/rss/economics.rss")
    print(parser.parse_feed(2))
