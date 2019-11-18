"""
Tests depend on local data. You have to launch the script
from the root directory (there rss.py is locate)

Example links:
tut_by_rss = 'https://news.tut.by/rss/index.rss'
google_rss = 'https://news.google.com/news/rss'
yahoo = 'https://news.yahoo.com/rss/'
"""
import unittest
from logging import INFO
from contextlib import redirect_stdout

from rss_reader.rss import logger_init
from rss_reader.bots import yahoo
from rss_reader.utils.RssInterface import RssException


class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url = './tests/data/yahoo_news.xml'
        self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(), width=120)

    def test_bot_limit(self):
        self.assertEqual(self.bot.limit, 2)

    def test_bot_feed(self):
        self.assertEqual(self.bot.news.feed, 'Yahoo News - Latest News & Headlines')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot.news.items), 2)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot.get_json()), 3336)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot.get_news()), 5951)

    def test_human_text(self):
        item = self.bot.news.items[0]
        self.assertEqual(item.title, 'Israel kills Islamic Jihad commander, rockets rain from Gaza')
        self.assertEqual(len(self.bot._parse_news_item(item)), 1035)

    def test_raising_exception(self):
        url = 'asdf'
        with self.assertRaises(RssException):
            self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(), width=120)

    def test_main_output_news(self):
        url = './tests/data/yahoo_news.xml'

        with open('./tests/data/yahoo.txt', 'w') as f:
            with redirect_stdout(f):
                self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(INFO), width=120)

        with open('./tests/data/yahoo.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 599)
        self.assertGreater(out_str.find('INFO'), 4)
