"""
Tests for rssreader.news module
"""
import unittest
from datetime import date

from rssreader.news import News


class NewsTestCase(unittest.TestCase):
    """
    Test cases for News class
    """
    def setUp(self):
        super().setUp()

        self.some_news = News(
            'Some news', 'Thu, 31 Oct 2019 10:25:00 +0300', date(2019, 10, 31), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]
        )

    def test__get_hrefs_text(self):
        self.assertEqual('[0]: https://img.dummy.xz/pic1.jpg (image/jpeg))\n', self.some_news._get_hrefs_text())

    def test_get_text(self):
        standard = 'Title: Some news\nDate: Thu, 31 Oct 2019 10:25:00 +0300\nLink: https://dummy.xz/1\n\n' \
                   'Everything is ok\n\nLinks:\n[0]: https://img.dummy.xz/pic1.jpg (image/jpeg))\n'

        self.assertEqual(standard, self.some_news.get_text(paint=lambda t, c=None: t))

    def test_get_json_dict(self):
        standard = {'title': 'Some news', 'published': 'Thu, 31 Oct 2019 10:25:00 +0300',
                    'link': 'https://dummy.xz/1', 'description': 'Everything is ok',
                    'hrefs': [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]}

        self.assertEqual(standard, self.some_news.get_json_dict())
