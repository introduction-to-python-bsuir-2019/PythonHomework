"""
Tests for rssreader.feed module
"""
import unittest
from datetime import datetime
import io
from contextlib import redirect_stdout
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

        self.first_news = News(
            'First news', 'Thu, 30 Oct 2019 10:22:00 +0300', datetime(2019, 10, 30, 10, 22), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]
        )

        self.feed.news.append(self.first_news)

        with open('tests/correct.rss', 'r') as fd:
            self.correct_rss = fd.read()

    def test_request(self) -> None:
        """
        Test that rss file is parsed
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
        """feed.bozo attribute is set to 1. That means that feed is not well-formed."""
        with open('tests/incorrect.rss', 'r') as fd:
            self.incorrect_rss = fd.read()

        data = feedparser.parse(self.incorrect_rss)
        with self.assertRaises(Exception) as cm:
            self.feed._parse(data)

    def test_get_json(self) -> None:
        """
        Feed is converted into json
        """
        standard = '{\n    "feed": "Dummy news",\n    ' \
                   '"news": [\n        {\n            "title": "First news",\n            ' \
                   '"published": "Thu, 30 Oct 2019 10:22:00 +0300",\n            "link": "https://dummy.xz/1",\n  ' \
                   '          "description": "Everything is ok",\n            "hrefs": [\n                {\n     ' \
                   '               "type": "image/jpeg)",\n                    "href": "https://img.dummy.xz/pic1.' \
                   'jpg"\n                }\n            ]\n        }\n    ]\n}'
        self.assertEqual(standard, self.feed.get_json())

    def test_get_text(self) -> None:
        """
        Feed is converted into text. This text is displayed into console.
        """
        standard = 'Feed: Dummy news\n\nTitle: First news\nDate: Thu, 30 Oct 2019 10:22:00 +0300\n' \
                   'Link: https://dummy.xz/1\n\n' \
                   'Everything is ok\n\nLinks:\n[0]: https://img.dummy.xz/pic1.jpg (image/jpeg))\n'
        self.assertEqual(standard, self.feed.get_text(paint=lambda t, c=None: t))

    def test_add_news(self) -> None:
        """New news is added"""
        init_len = len(self.feed.news)
        self.feed.add_news('Third news', 'Thu, 31 Oct 2019 10:22:00 +0300', datetime(2019, 10, 31, 10, 22, 0),
                           'https://dummy.xz/3', 'I trust you', [])
        self.assertEqual(init_len + 1, len(self.feed.news))

    def test_print_json_ok(self) -> None:
        """
        Feed is printed (in stdout) in json format
        """
        with io.StringIO() as buf:
            with redirect_stdout(buf):
                self.feed.print(True, paint=lambda t, c=None: t)
            self.assertEqual(self.feed.get_json()+'\n', buf.getvalue())

    def test_print_text_ok(self) -> None:
        """
        Feed is printed (in stdout) as text
        """
        with io.StringIO() as buf:
            with redirect_stdout(buf):
                self.feed.print(False, paint=lambda t, c=None: t)
            self.assertEqual(self.feed.get_text(paint=lambda t, c=None: t)+'\n', buf.getvalue())

    def test_print_err(self) -> None:
        """
        Exception is raised as there is no news
        """
        self.feed.news = []
        with self.assertRaises(Exception) as cm:
            self.feed.print(False, to_json=True)
