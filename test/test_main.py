import unittest
import logging
from rss import logger_init, get_bot_instance, main
from bots import yahoo, tut, default
from unittest.mock import patch, Mock
from contextlib import redirect_stdout

from utils.RssInterface import RssException


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

    def test_main_raise_exception(self):
        with self.assertRaises(TypeError):
            main('asf', 3, logger_init(), 200)

    def test_none_output(self):

        self.assertEqual(main('asf', 3, 220, False, False), None)

    def test_json_output(self):
        self.assertEqual(main('asf', 3, 220, True, False), None)

    def test_verbose_output(self):
        self.assertEqual(main('asf', 3, 220, True, True), None)

    def test_exc_output(self):
        mock = Mock()
        main = mock
        main('asf', 3, 220, True, True)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_args[0][0], 'asf')

    def test_main_output_json_verbose_on(self):
        with open('./test/data/help.txt', 'w') as f:
            with redirect_stdout(f):
                main('asf', 3, 220, False, False)

        with open('./test/data/help.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 261)
        self.assertEqual(out_str.find('not well-formed (invalid token)'), -1)

    def test_main_output_json_on(self):
        with open('./test/data/help.txt', 'w') as f:
            with redirect_stdout(f):
                main('./test/data/tut_news.xml', 3, 220, True, False)

        with open('./test/data/help.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 15081)
        self.assertEqual(out_str.find('not well-formed (invalid token)'), -1)
        self.assertEqual(out_str.find('INFO'), -1)

    def test_main_output_news(self):
        with open('./test/data/help.txt', 'w') as f:
            with redirect_stdout(f):
                main('./test/data/tut_news.xml', 3, 220, False, False)

        with open('./test/data/help.txt', 'r') as f:
            out_str = f.read()

        self.assertEqual(len(out_str), 11643)
        self.assertEqual(out_str.find('WARNING'), -1)
        self.assertEqual(out_str.find('INFO'), -1)



