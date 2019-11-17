import argparse
import logging
from unittest.mock import Mock
import os
import unittest
import sys

from rss_reader.bots import yahoo, tut, default
from rss_reader.rss import logger_init, get_bot_instance, main, args_parser, PROG_VERSION

from contextlib import redirect_stdout


class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_logger_init(self):
        logger = logger_init()
        self.assertEqual(logger.level, logging.CRITICAL)

    def test_logger_set(self):
        logger = logger_init(logging.INFO)
        self.assertEqual(logger.level, logging.INFO)

    def test_yahoo_bot_init(self):
        logger = logger_init(logging.INFO)
        bot = get_bot_instance('asfnews.yahoo.com/rssasfasf', logger)
        self.assertEqual(bot, yahoo.Bot)

    def test_tut_bot_init(self):
        logger = logger_init()
        bot = get_bot_instance('asfn//asfnews.tut.by/rsssasfasf', logger)
        self.assertEqual(bot, tut.Bot)

    def test_default_bot_init(self):
        logger = logger_init()
        bot = get_bot_instance('asfnewsasdffsagoogleyahootututsasfasf', logger)
        self.assertEqual(bot, default.Bot)

    def test_args(self):
        rss_path = f'{os.getcwd()}/rss_reader/rss.py'
        sys.argv = [
            rss_path,
            'https://news.tut.by/rss/index.rss',
            '--verbose',
            '--limit', '3',
            '--json',
            '--width', '200',
        ]
        args = args_parser()
        self.assertEqual(args.url, 'https://news.tut.by/rss/index.rss'),
        self.assertEqual(args.verbose, True),
        self.assertEqual(args.json, True),
        self.assertEqual(args.limit, 3),
        self.assertEqual(args.width, 200),

        self.assertEqual(main(), None),

    def test_version(self):
        rss_path = f'{os.getcwd()}/rss_reader/rss.py'
        sys.argv = [
            rss_path,
            './tests/data/tut_news.xml',
            '--limit', '2',
        ]

        with open('./tests/data/help.txt', 'w') as f:
            with redirect_stdout(f):
               main()

        with open('./tests/data/help.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 5352)