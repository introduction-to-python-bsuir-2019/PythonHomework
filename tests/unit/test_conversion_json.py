"""Tests for rssreader.format_conversion.conversion_json module"""

import unittest
import feedparser
from os import path

from rssreader.format_conversion import conversion_json
from rssreader.parser import feed_parser


class JsonConversionTestCase(unittest.TestCase):
    """Test cases for JsonConversion class"""
    def setUp(self):
        with open(
                path.join("tests", "unit", "data", "test_correct.rss"),
                "r") as rf:
            self.url = rf.read()

        self.test_feed_json = conversion_json.JsonConversion(self.url, 1)
        self.test_feed = feed_parser.RssParser(self.url, 1)

    def test_convert_to_json(self):
        """Function test_convert_to_json test"""
        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_convert_to_json.txt"), "r") as rf:
            answer = rf.read()

        self.assertEqual(
            self.test_feed_json.convert_to_json(self.test_feed.parse_news()),
            answer
        )


if __name__ == "__main__":
    unittest.main()
