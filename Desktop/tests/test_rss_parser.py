"""Tests must be called from root project's directory."""
import unittest
import sys
import os

sys.path.append(os.getcwd() + '/rssreader')

from rss_reader.rss_parser import RssReader

CORRECT_LINK = 'https://news.yahoo.com/rss/'
INCORRECT_LINK = 'qwerty'


class TestRssParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_news_as_string(self):
        rss = RssReader(CORRECT_LINK)
        news = rss.get_news_as_string()
        self.assertEqual(type(news), str)

        rss.set_link(INCORRECT_LINK)
        try:
            rss.get_news_as_string()
        except Exception as exception:
            self.assertEqual(type(exception), AttributeError)

    def test_get_news_as_list(self):
        rss = RssReader(CORRECT_LINK)
        try:
            news_list = rss._get_news_as_list('qwe')
        except Exception as exception:
            self.assertEqual(type(exception), TypeError)

        news_list = rss._get_news_as_list(-100)
        self.assertGreater(len(news_list), 0)

        news_list = rss._get_news_as_list(0)
        self.assertGreater(len(news_list), 0)

        news_list = rss._get_news_as_list(3)
        self.assertEqual(len(news_list), 3)

    def test_fix_symbols(self):
        rss = RssReader(CORRECT_LINK)

        test_string = 'qwerty&#39; && &#39; #12__&#39;'
        assertion_string = "qwerty' && ' #12__'"

        self.assertEqual(rss._fix_symbols(test_string), assertion_string)
        self.assertEqual(rss._fix_symbols(assertion_string), assertion_string)
        self.assertEqual(rss._fix_symbols(''), '')

    def test_parse_item(self):
        text = 'Text'
        testing_str = f'<body>{text}</body>'

        rss = RssReader('')
        self.assertEqual(rss._parse_item(testing_str), text)


if __name__ == '__main__':
    unittest.main()
