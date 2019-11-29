import unittest
from datetime import datetime

from reader.NewsItem import NewsItem


class TestNewsItem(unittest.TestCase):
    def setUp(self) -> None:
        self.news_item = NewsItem('Title', 'Link', datetime.now(),
                                  None, 'link.com')

    def test_news_item_title(self):
        self.assertEqual(self.news_item.title, 'Title')

    def test_news_item_link(self):
        self.assertEqual(self.news_item.link, 'Link')

    def test_news_item_links(self):
        self.assertEqual(self.news_item.links, 'link.com')


if __name__ == '__main__':
    unittest.main()
