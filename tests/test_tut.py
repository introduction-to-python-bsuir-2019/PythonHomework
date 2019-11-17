"""
Tests depend on local data. You have to launch the script
from the root directory (there rss.py is locate)

Example links:
tut_by_rss = 'https://news.tut.by/rss/index.rss'
google_rss = 'https://news.google.com/news/rss'
yahoo = 'https://news.yahoo.com/rss/'
"""
import unittest

from rss_reader.bots import tut
from rss_reader.rss import logger_init



class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url = './tests/data/tut_news.xml'
        self.bot = tut.Bot(url=url, limit=7, logger=logger_init(), width=120)

    def test_bot_limit(self):
        self.assertEqual(self.bot.limit, 7)

    def test_bot_feed(self):
        self.assertEqual(self.bot.news.get('feed'), 'TUT.BY: Новости ТУТ - Главные новости')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot.news.get('items')), 7)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot.get_json()), 34377)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot.get_news()), 20006)
