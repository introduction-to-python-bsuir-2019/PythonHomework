"""Tests for rssreader.parser.feed_parser module"""

import unittest
import feedparser
from unittest.mock import patch
from os import path

from rssreader.parser import feed_parser
from rssreader.exceptions import all_exceptions


class RssParserTestCase(unittest.TestCase):
    """Test cases for RssParser class"""
    def setUp(self):
        with open(
                path.join("tests", "unit", "data", "test_correct.rss"),
                "r") as rf:
            self.url = rf.read()

        self.test_feed = feed_parser.RssParser(self.url, 1)

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_result_of_parsing_rss.txt"), "r") as rf:
            self.test_result_rss = rf.read()

    def test__check_limit(self):
        """Function _check_limit test"""
        test_list = [1, 2, None, 9999999, -10]
        answer_list = [1, 2, 4, 4, 0]

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_entries.txt"), "r") as rf:
            enrtries = rf.readlines()

        for test_value, answer in zip(test_list, answer_list):
            test_feed = feed_parser.RssParser(self.url, test_value)
            self.assertEqual(test_feed._check_limit(enrtries), answer)

    def test__get_rss_from_url(self):
        """Function _get_rss_from_url test"""
        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_incorrect.rss"), "r") as rf:
            incorrect_rss = rf.read()

        self.assertEqual(
            str(self.test_feed._get_rss_from_url()),
            self.test_result_rss
            )

        self.assertRaises(
            all_exceptions.InvalidLinkOrInternetConnectionError,
            lambda: feed_parser.RssParser(incorrect_rss)._get_rss_from_url()
            )

    def test___find_type_link(self):
        """Function __find_type_link test"""
        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_links.txt"), "r") as rf_links:
            list_links = rf_links.readlines()

        list_answer = [
            "(image)", "(image)", "(image)",
            "(image)", "(image)", "(image)",
            "(video)", "(video)", "(video)"
        ]

        for link, answer in zip(list_links, list_answer):
            self.assertEqual(
                self.test_feed._RssParser__find_type_link(link),
                answer
                )

    @patch("rssreader.parser.feed_parser.RssParser._check_limit")
    @patch("rssreader.parser.feed_parser.RssParser._get_rss_from_url")
    def test_parse_news(self, rss_mock, limit_mock):
        """Function test_parse_news test

        self.limit = 1
        self.html_news = data/test_result_of_parsing_rss.txt

        """
        rss_mock.return_value = feedparser.parse(self.url)
        limit_mock.return_value = 1

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_parsing_news.txt"), "r") as rf:
            test_parsing_news = rf.read()

        self.assertEqual(str(self.test_feed.parse_news()), test_parsing_news)

    @patch("rssreader.parser.feed_parser.RssParser._RssParser__find_type_link")
    def test___make_pretty_links(self, type_link_mock):
        """Function __make_pretty_links test

        self.__find_type_link(element) = (test)

        """
        type_link_mock.return_value = "(test)"
        link = "https://news.tut.by/world/662695.html"

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_links.txt"), "r") as rf_links:
            links = rf_links.readlines()
        links = [link.rstrip() for link in links]

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_answer_links.txt"), "r") as rf_links:
            answer = rf_links.read()

        self.assertEqual(
            self.test_feed._RssParser__make_pretty_links(link, links),
            answer
        )

    @patch(
        "rssreader.parser.feed_parser.RssParser._RssParser__make_pretty_links")
    def test_make_pretty_rss(self, pretty_links):
        """Function test_make_pretty_rss test

        self.__make_pretty_links(link, links) =
        [1]: http://liftoff.msfc.nasa.gov/news/2003/news-starcity.asp(link)

        """
        link_part_1 = "[1]: http://liftoff.msfc.nasa.gov"
        link_part_2 = "/news/2003/news-starcity.asp(link)"
        pretty_links.return_value = link_part_1 + link_part_2

        with open(path.join(
                "tests",
                "unit",
                "data",
                "test_pretty_rss.txt"), "r") as rf:
            answer = rf.read()

        self.assertEqual(
            self.test_feed.make_pretty_rss(self.test_feed.parse_news()),
            answer
            )


if __name__ == "__main__":
    unittest.main()
