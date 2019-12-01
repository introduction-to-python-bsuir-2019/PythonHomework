"""Tests for rssreader.format_conversion.conversion_html module"""

import unittest
from os import path

from rssreader.parser import feed_parser
from rssreader.format_conversion import conversion_html as cv_html


class HtmlConversionTestCase(unittest.TestCase):
    """Test cases for HtmlConversion class"""
    def setUp(self):
        with open(
                path.join("tests", "unit", "data", "test_correct.rss"),
                "r") as rf:
            self.url = rf.read()

        self.test_feed = feed_parser.RssParser(self.url, 1)
        self.test_news = self.test_feed.parse_news()
        self.test_html = cv_html.HtmlConversion(self.test_news)

    def test_conversion_to_html(self):
        """Function conversion_to_html test"""
        with open(
                path.join("tests", "unit", "data", "test_html.html"),
                "r") as rf:
            answer = rf.read()
        self.assertEqual(self.test_html.conversion_to_html(), answer)


if __name__ == "__main__":
    unittest.main()
