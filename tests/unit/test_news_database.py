"""Tests for rssreader.db.news_database module"""
import unittest
from unittest.mock import patch

from rssreader.db import news_database as db

NAME_FUNCTION_MOCK = "_NewsDatabase__search_caching_news"


class NewsDatabaseTestCase(unittest.TestCase):
    """Test cases for NewsDatabase class"""
    def setUp(self):
        self.test_mongo = db.NewsDatabase("test_url", 1, 1)

    def test___template_news(self):
        """Function __template_news test"""
        self.assertEqual(
            self.test_mongo._NewsDatabase__template_news(1, {1: 1}),
            {"source": "test_url", "date": 1, "news": {1: 1}})

    def test___convert_date_format(self):
        """Function __convert_date_format test"""
        list_tests = [
            "Wed, 27 Nov 2018 09:56:11 GMT",
            "Wed, 7 Dec 2017 09:56:11 GMT",
            "Wed, 5 Apr 2016 09:56:11 +0300",
            "Wed, 7 Sep 2015 09:56:11 -0400",
            "Wed, 10 Nov 2014 09:56:11 +0000"
        ]
        list_answers = [
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S %z"
        ]

        for test, answer in zip(list_tests, list_answers):
            self.assertEqual(
                self.test_mongo._NewsDatabase__convert_date_format(test),
                answer)

    @patch(f"rssreader.db.news_database.NewsDatabase.{NAME_FUNCTION_MOCK}")
    def test_show_news(self, find_mock):
        """Function show_news test"""
        find_mock.return_value = [{"test": 1, "news": {"test": 777}}]

        self.assertEqual(self.test_mongo.show_news(), [{"test": 777}])


if __name__ == "__main__":
    unittest.main()
