"""
Tests for rssreader.feed module
"""
from unittest import TestCase
from unittest.mock import Mock, patch
from datetime import datetime
import io
from contextlib import redirect_stdout
from pathlib import Path
from html import unescape

from rssreader.news import News
from rssreader.feed import Feed


class FeedTestCase(TestCase):
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

        self.rss_entries = [
            Mock(title='&copy; M1', description='desc 1', published_parsed=[2019, 10, 31, 12, 54, 9]),
            Mock(title='&copy; M2', description='desc 2', published_parsed=[2019, 10, 31, 12, 54, 9]),
            Mock(title='M3', description='&copy; desc 3', published_parsed=[2019, 10, 31, 12, 54, 9])
        ]
        self.mock_feed = Mock(bozo=0, encoding='utf-8', feed=Mock(title='Feed'), entries=self.rss_entries)

    def test_request(self) -> None:
        """
        Test general function processing rss request
        """
        cache_dir = Path('path/to/cache')
        self.feed.url = 'ask/some/url'

        with patch('feedparser.parse', return_value='parsed rss') as mock_feedparser:
            with patch('rssreader.feed.Feed._parse') as mock_parse:
                with patch('rssreader.feed.Feed.cache') as mock_cache:
                    self.feed.request(cache_dir)

        mock_feedparser.assert_called_once_with('ask/some/url')
        mock_parse.assert_called_once_with('parsed rss')
        mock_cache.assert_called_once_with(cache_dir)

    def test__parse_all(self) -> None:
        """
        All news from the feed are parsed
        """
        self.feed.news = []
        self.feed.limit = None

        with patch('bs4.BeautifulSoup', return_value=Mock(text='data')):
            with patch('rssreader.feed.Feed._extract_links', return_value={}) as mock_links:
                self.feed._parse(self.mock_feed)

        self.assertEqual(self.mock_feed.encoding, self.feed.encoding)
        self.assertEqual('Feed', self.feed.title)

        self.assertEqual(3, len(self.feed.news))
        self.assertEqual(mock_links.call_count, 3)
        for i in range(0, 3):
            with self.subTest(i=i):
                self.assertEqual(unescape(self.rss_entries[i].title), self.feed.news[i].title)
                self.assertEqual(unescape(self.rss_entries[i].description), self.feed.news[i].description)

    def test__parse_one(self) -> None:
        """
        Limit argument does not impact on parsing - all news are processed.
        """
        self.feed.news = []
        self.feed.limit = 1

        with patch('bs4.BeautifulSoup', return_value=Mock(text='data')):
            with patch('rssreader.feed.Feed._extract_links', return_value={}):
                self.feed._parse(self.mock_feed)

        self.assertEqual(3, len(self.feed.news))

    def test__parse_err(self) -> None:
        """Test a situation when feed in incorrect"""

        # It means that result feed is not well-formed.
        data = Mock(bozo=1)
        with self.assertRaises(Exception):
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
        with self.assertRaises(Exception):
            self.feed.print(False, to_json=True)

    def test_load_from_cache(self) -> None:
        self.feed = Feed('https://dummy.xz/here.rss', 1)

        cache_dir = Path('path/to/cache')
        with patch('rssreader.cache.Cache.load', return_value=None) as mock_load:
            self.feed.load_from_cache(cache_dir)

        mock_load.assert_called_once_with(self.feed)
        self.assertEqual(0, len(self.feed.news))  # news list is empty
