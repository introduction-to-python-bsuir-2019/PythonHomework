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
from rss_reader.utils.rss_interface import RssException
from rss_reader.utils.data_structures import ConsoleArgs

class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url = './tests/data/yahoo_news.xml'
        args = ConsoleArgs(
            url=url,
            limit=2,
            width=120,
        )
        self.bot = yahoo.Bot(args, logger=logger_init())

    def test_bot_limit(self):
        self.assertEqual(self.bot.limit, 2)

    def test_bot_feed(self):
        self.assertEqual(self.bot.news.feed, 'Yahoo News - Latest News & Headlines')

    def test_bot_news_count(self):
        self.assertEqual(len(self.bot.news.items), 2)

    def test_bot_json_length(self):
        self.assertEqual(len(self.bot.get_json()), 3336)

    def test_bot_reddit_news_length(self):
        self.assertEqual(len(self.bot.print_news()), 6111)

    def test_human_text(self):
        item = self.bot.news.items[0]
        self.assertEqual(item.title, 'Israel kills Islamic Jihad commander, rockets rain from Gaza')
        self.assertEqual(len(self.bot._parse_news_item(item)), 1092)

    def test_raising_exception(self):
        url = 'asdf'
        args = ConsoleArgs(
            url=url,
            limit=2,
            width=120,
        )
        with self.assertRaises(RssException):
            self.bot = yahoo.Bot(args, logger=logger_init())

    def test_main_output_news(self):
        url = './tests/data/yahoo_news.xml'
        args = ConsoleArgs(
            url=url,
            limit=2,
            width=120,
        )
        with open('./tests/data/yahoo.txt', 'w') as f:
            with redirect_stdout(f):
                self.bot = yahoo.Bot(args, logger=logger_init(INFO))

        with open('./tests/data/yahoo.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 599)
        self.assertGreater(out_str.find('INFO'), 4)
