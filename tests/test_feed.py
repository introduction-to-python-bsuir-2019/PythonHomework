"""
Tests for rssreader.feed module
"""
import unittest
from rssreader.news import News
from rssreader.feed import Feed
from datetime import date
import feedparser
import io
from contextlib import redirect_stdout


class FeedTestCase(unittest.TestCase):
    """
    Test cases for Feed class
    """
    def setUp(self) -> None:
        super().setUp()

        self.feed = Feed('https://dummy.xz/here.rss', 1)
        self.feed.encoding = 'utf-8'

        self.first_news = News(
            'First news', 'Thu, 30 Oct 2019 10:25:00 +0300', date(2019, 10, 30), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]
        )

        self.feed.news.append(self.first_news)

        with open('tests/correct.rss', 'r') as fd:
            self.correct_rss = fd.read()

        with open('tests/incorrect.rss', 'r') as fd:
            self.incorrect_rss = fd.read()

    def test_request(self):
        """
        Test that rss file is parsed
        """
        self.feed.limit = 10
        self.feed.news = []
        self.feed.url = self.correct_rss
        self.feed.request()
        self.assertEqual(3, len(self.feed.news))

    def test__parse_all(self):
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
                'Sun', 'Thu, 31 Oct 2019 14:42:00 +0300', date(2019, 10, 31), 'https://news.good.by/wild/1.html',
                'The sun is shining', [{'type': 'image/jpeg',
                                        'href': 'https://img.good.by/n/reuters/0c/a/meksika_1.jpg'}]
            ),
            News(
                'Birds', 'Thu, 31 Oct 2019 18:42:00 +0300', date(2019, 10, 31), 'https://news.good.by/wild/2.html',
                'The birds are signing', [{'type': 'image/jpeg',
                                           'href': 'https://img.good.by/n/reuters/0c/a/meksika_2.jpg'}]
            ),
            News(
                'Animals', 'Mon, 29 Oct 2019 14:42:00 +0300', date(2019, 10, 29), 'https://news.good.by/wild/3.html',
                'The animals are jumping', [{'type': 'image/jpeg',
                                             'href': 'https://img.good.by/n/reuters/0c/a/meksika_3.jpg'}]
            )
        ]

        # check parsed items
        for i in range(0, 3):
            with self.subTest(i=i):
                self.assertEqual(standards[i].get_json_dict(), self.feed.news[i].get_json_dict())

    def test__parse_one(self):
        """
        Feed is successfully parsed but only one news is stored because of the limit
        """
        self.feed.news = []
        self.feed.limit = 1
        data = feedparser.parse(self.correct_rss)
        self.feed._parse(data)
        self.assertEqual(1, len(self.feed.news))

    def test__parse_err(self):
        """feed.bozo attribute is set to 1. That means that feed is not well-formed."""
        data = feedparser.parse(self.incorrect_rss)
        with self.assertRaises(Exception) as cm:
            self.feed._parse(data)

    def test_get_json(self):
        """
        Feed is converted into json
        """
        standard = '{\n    "feed": "",\n    "news": [\n        {\n            "title": "First news",\n            ' \
                   '"published": "Thu, 30 Oct 2019 10:25:00 +0300",\n            "link": "https://dummy.xz/1",\n  ' \
                   '          "description": "Everything is ok",\n            "hrefs": [\n                {\n     ' \
                   '               "type": "image/jpeg)",\n                    "href": "https://img.dummy.xz/pic1.' \
                   'jpg"\n                }\n            ]\n        }\n    ]\n}'
        self.assertEqual(standard, self.feed.get_json())

    def test_get_text(self):
        """
        Feed is converted into text. This text is displayed into console.
        """
        standard = 'Feed: \n\nTitle: First news\nDate: Thu, 30 Oct 2019 10:25:00 +0300\nLink: https://dummy.xz/1\n\n' \
                   'Everything is ok\n\nLinks:\n [0]: https://img.dummy.xz/pic1.jpg (image/jpeg))\n'
        self.assertEqual(standard, self.feed.get_text())

    def test_add_news(self):
        """New news is added"""
        init_len = len(self.feed.news)
        self.feed.add_news('Third news', 'Thu, 31 Oct 2019 10:25:00 +0300', date(2019, 10, 31), 'https://dummy.xz/3',
                           'I trust you', [])
        self.assertEqual(init_len + 1, len(self.feed.news))

    def test_print_json_ok(self):
        """
        Feed is printed (in stdout) in json format
        """
        with io.StringIO() as buf:
            with redirect_stdout(buf):
                self.feed.print(True)
            self.assertEqual(self.feed.get_json()+'\n', buf.getvalue())

    def test_print_text_ok(self):
        """
        Feed is printed (in stdout) as text
        """
        with io.StringIO() as buf:
            with redirect_stdout(buf):
                self.feed.print(False)
            self.assertEqual(self.feed.get_text()+'\n', buf.getvalue())

    def test_print_err(self):
        """Exception is raised as there is no news"""
        self.feed.news = []
        with self.assertRaises(Exception) as cm:
            self.feed.print(False)

