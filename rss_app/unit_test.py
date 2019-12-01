"""Unittests are performed in this module."""


import unittest
import logging
import json

from rss_app.RSS import RssAggregator
from rss_app.converter import Converter


class TestRSS(unittest.TestCase):

    def setUp(self):
        logger = logging.getLogger()
        logger.level = logging.DEBUG
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

        self.url = "http://news.com/rss"
        self.to_pdf = "d:/test_html.pdf"
        self.to_html = "d:/test_html.html"
        self.converter = Converter(self.url, 1, self.to_pdf, self.to_html, logger)
        self.test_date = RssAggregator(self.url, 1, 1, logger)

        with open("test_json.json", "r") as read_file:
            self.news = json.load(read_file)

    def test_get_file_name(self):
        test_url = "news.comrss.json"
        self.assertEqual(self.test_date.get_file_name(), test_url)

    def test_html_converter(self):
        with open("test_date_html.txt", "r") as rf:
            test_html_date = rf.read()

        self.converter.html_converter(self.news)

        with open(self.to_html, "r") as rf:
            new_html_date = rf.read()

        self.assertEqual(str(new_html_date), test_html_date)

    if __name__ == "__main__":
        unittest.main()
