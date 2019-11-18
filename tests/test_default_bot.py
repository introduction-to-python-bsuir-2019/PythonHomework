"""
Tests depend on local data. You have to launch the script
from the root directory (there rss.py is locate)

Example links:
tut_by_rss = 'https://news.tut.by/rss/index.rss'
google_rss = 'https://news.google.com/news/rss'
yahoo = 'https://news.yahoo.com/rss/'
"""
import unittest

from rss_reader.rss import logger_init
from rss_reader.bots import default


class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url_google = './tests/data/google_news.xml'
        url_reddit = './tests/data/reddit_news.xml'

        self.bot_google = default.Bot(url=url_google, limit=10, logger=logger_init(), width=120)
        self.bot_reddit = default.Bot(url=url_reddit, limit=3, logger=logger_init(), width=80)

    def test_bot_limit(self):
        self.assertEqual(self.bot_google.limit, 10)

    def test_bot_feed(self):
        self.assertEqual(self.bot_google.news.feed, 'Top stories - Google News')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot_google.news.items), 10)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot_google.get_json()), 31210)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot_google.get_news()), 45755)

    def test_bot_reddit_limit(self):
        self.assertEqual(self.bot_reddit.limit, 3)

    def test_bot_reddit_feed(self):
        self.assertEqual(self.bot_reddit.news.feed, 'World News')

    def test_bot_reddit_news_count(self):
        self.assertEqual(len(self.bot_reddit.news.items), 3)

    def test_bot_reddit_json_length(self):
        self.assertEqual(len(self.bot_reddit.get_json()), 2759)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot_reddit.get_news()), 5549)



