"""
Tests for rssreader.feed module
"""
import unittest
from datetime import datetime
from pathlib import Path

import feedparser

from rssreader.news import News
from rssreader.feed import Feed


class FeedTestCase(unittest.TestCase):
    """
    Test cases for Feed class
    """
    def setUp(self) -> None:
        super().setUp()

        self.feed = Feed('https://dummy.xz/here.rss', 1)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        with open(Path(__file__).parent.joinpath('correct.rss'), 'r') as fd:
            self.correct_rss = fd.read()

    def test_request(self) -> None:
        """
        Test that rss data are correctly parsed
        """
        cache_dir = Path().cwd()
        self.feed.limit = 10
        self.feed.news = []
        self.feed.url = self.correct_rss
        self.feed.request(cache_dir)
        self.assertEqual(3, len(self.feed.news))
        cache_dir.joinpath('cache.db').unlink()

    def test__parse_all(self) -> None:
        """
        All news from the feed are parsed
        """
        self.feed.news = []
        self.feed.limit = None
        data = feedparser.parse(self.correct_rss)
        self.feed._parse(data)
        self.assertEqual(3, len(self.feed.news))

        self.assertEqual('Good news', self.feed.title)
        standards = [
            News(
                'Sun', 'Thu, 31 Oct 2019 14:42:00 +0300', datetime(2019, 10, 31, 14, 42, 0),
                'https://news.good.by/wild/1.html',
                'The sun is shining', [
                    {'type': 'text/html', 'href': 'https://news.good.by/wild/1.html'},
                    {'type': 'image/jpeg', 'href': 'https://img.good.by/n/reuters/0c/a/meksika_1.jpg'}]
            ),
            News(
                'Birds', 'Thu, 31 Oct 2019 18:42:00 +0300', datetime(2019, 10, 31, 18, 42, 0),
                'https://news.good.by/wild/2.html',
                'The birds are signing', [
                    {'type': 'text/html', 'href': 'https://news.good.by/wild/2.html'},
                    {'type': 'image/jpeg', 'href': 'https://img.good.by/n/reuters/0c/a/meksika_2.jpg'}]
            ),
            News(
                'Animals', 'Mon, 29 Oct 2019 14:42:00 +0300', datetime(2019, 10, 29, 14, 42),
                'https://news.good.by/wild/3.html',
                'The animals are jumping', [
                    {'type': 'text/html', 'href': 'https://news.good.by/wild/3.html'},
                    {'type': 'image/jpeg', 'href': 'https://img.good.by/n/reuters/0c/a/meksika_3.jpg'}]
            )
        ]

        # check parsed items
        for i in range(0, 3):
            with self.subTest(i=i):
                self.assertEqual(standards[i].get_json_dict(), self.feed.news[i].get_json_dict())

    def test__parse_one(self) -> None:
        """
        Limit argument does not impact on parsing - all news are parsed.
        """
        self.feed.news = []
        self.feed.limit = 1
        data = feedparser.parse(self.correct_rss)
        self.feed._parse(data)
        self.assertEqual(3, len(self.feed.news))

    def test__parse_err(self) -> None:
        """Test a situation when feed in incorrect"""
        with open(Path(__file__).parent.joinpath('incorrect.rss'), 'r') as fd:
            self.incorrect_rss = fd.read()

        # feed.bozo attribute is set to 1 in this case.
        data = feedparser.parse(self.incorrect_rss)
        with self.assertRaises(Exception):
            self.feed._parse(data)
