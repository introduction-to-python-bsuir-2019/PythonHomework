import unittest
import feedparser
from unittest.mock import patch
from os import path
from app.rssConverter.NewsPrinter import NewsPinter


class RssNewsPrinterTests(unittest.TestCase):

    def setUp(self):
        self.newsPrinter = NewsPinter()

    def get_limited_news_test(self):
        """Function  test getting limited news"""
        check_dict = {'a': 1, 'b': 2}
        self.assertCountEqual({'a': 1}, self.newsPrinter.get_limited_news(check_dict, 1))


if __name__ == '__main__':
    unittest.main()
