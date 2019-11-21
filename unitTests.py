import unittest
from rss_parser import parse

class FunctionTestMethods(unittest.TestCase):
    def test_url(self):
        self.assertEqual(parse(['https://news.yahoo.com/rss/',
                          'https://news.google.com/news/rss',
                          'https://news.yandex.ru/world.rss',
                          'https://news.tut.by/rss/world.rss',]),['https://news.yahoo.com/rss/',
                                                                  'https://news.google.com/news/rss',
                                                                  'https://news.yandex.ru/world.rss',
                                                                  'https://news.tut.by/rss/world.rss',])