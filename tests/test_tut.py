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
from rss_reader.utils.data_structures import ConsoleArgs



class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url = './tests/data/tut_news.xml'
        args = ConsoleArgs(
            url=url,
            limit=7,
        )
        self.bot = tut.Bot(args, logger=logger_init())

    def test_bot_limit(self):
        self.assertEqual(self.bot.limit, 7)

    def test_bot_feed(self):
        self.assertEqual(self.bot.news.feed, 'TUT.BY: Новости ТУТ - Главные новости')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot.news.items), 7)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot.get_json()), 18116)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot.print_news()), 20999)
