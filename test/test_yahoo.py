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
        url = './test/data/yahoo_news.xml'
        self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(), width=120)

    def test_bot_limit(self):
        self.assertEqual(self.bot.limit, 2)

    def test_bot_feed(self):
        self.assertEqual(self.bot.news.get('feed'), 'Yahoo News - Latest News & Headlines')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot.news.get('items')), 2)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot.get_json()), 5422)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot.get_news()), 5951)

    def test_human_text(self):
        item = self.bot.news.get('items')[0]
        self.assertEqual(item.get('title'), 'Israel kills Islamic Jihad commander, rockets rain from Gaza')
        self.assertEqual(len(item.get('human_text')), 1035)

    def test_raising_exception(self):
        url = 'asdf'
        with self.assertRaises(RssException):
            self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(), width=120)

    def test_main_output_news(self):
        url = './test/data/yahoo_news.xml'

        with open('./test/data/yahoo.txt', 'w') as f:
            with redirect_stdout(f):
                self.bot = yahoo.Bot(url=url, limit=2, logger=logger_init(INFO), width=120)

        with open('./test/data/yahoo.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 564)
        self.assertGreater(out_str.find('INFO'), 4)
