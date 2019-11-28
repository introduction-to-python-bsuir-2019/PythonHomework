import time
import unittest
from unittest.mock import patch, MagicMock

from rssreader.rss_reader import RSSReader

__all__ = ['TestRSSReader']


class TestRSSReader(unittest.TestCase):
    def setUp(self):
        date = time.struct_time((2019, 11, 26, 20, 53, 11, 1, 330, 0))
        self.reader = RSSReader()
        self.source = "https://news.yahoo.com/rss/"
        self.response = {
            'feed': {
                'title': 'Yahoo News - Latest News & Headlines',
            },
            'status': 200,
            'entries': [{
                'title': 'Some title',
                'description': '<p><a href="some long link"><img src="some long link to source of image 2" width="130" height="86" alt="Alt of image 2"></a>Some long description<p><br clear="all">',
                'link': 'some long link',
                'published_parsed': date,
            }]
        }
        self.response_parsed = {
            'title': 'Yahoo News - Latest News & Headlines',
            'articles': [{
                'title': 'Some title',
                'description': 'Some long description',
                'dec_description': '[link 1][Image 2: Alt of image 2] Some long description',
                'link': 'some long link',
                'pubDate': 'Tue, 26 Nov 2019 20:53',
                'media': [{
                    'src': 'some long link to source of image 2',
                    'alt': 'Alt of image 2',
                    'width': '130',
                    'height': '86'
                }],
                'links': [
                    'some long link',
                    'some long link to source of image 2'
                ],
                'dec_links': [
                    '[1]: some long link (link)',
                    '[2]: some long link to source of image 2 (image)'
                ]
            }]
        }

    def test_get_articles_from_url(self):
        limit = 1
        with patch('rssreader.html_parser.Parser.parse') as html_parser_mock:
            html_parser_mock.return_value = 'Successful'
            with patch('feedparser.parse') as feedparser_mock:
                feedparser_mock.return_value = self.response
                self.assertEqual(self.reader._get_articles_from_url(self.source, limit), 'Successful')

        feedparser_mock.assert_called_with(self.source.strip())
        html_parser_mock.assert_called_with(self.response, limit)

    def test_call_save(self):
        limit = 1
        self.reader._get_articles_from_url = MagicMock(return_value=self.response_parsed)
        with patch('rssreader.output_controller.OutputController.print') as print_mock:

            # Time for crutches :)
            with patch('rssreader.storage.controller.StorageController.__init__') as crutch:
                crutch.return_value = None  # remove creating db file
                # How to replace a class object on MagicMock without crutch?

                with patch('rssreader.storage.controller.StorageController.save') as storage_mock:
                    storage_mock.return_value = 1
                    self.assertIsNone(self.reader(self.source, limit, None))

        print_mock.assert_called_with(self.response_parsed)

    def test_call_load(self):
        limit = 1
        date = '20191122'
        with patch('rssreader.output_controller.OutputController.print') as print_mock:
            # Time for crutches :)
            with patch('rssreader.storage.controller.StorageController.__init__') as crutch:
                crutch.return_value = None  # remove creating db file
                # How to replace a class object on MagicMock without crutch?

                with patch('rssreader.storage.controller.StorageController.load') as storage_mock:
                    storage_mock.return_value = self.response_parsed
                    self.assertIsNone(self.reader(self.source, limit, date))

        print_mock.assert_called_once_with(self.response_parsed)
        storage_mock.assert_called_with(self.source, date, limit)


if __name__ == '__main__':
    unittest.main()
