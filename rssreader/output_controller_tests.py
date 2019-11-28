import json
import unittest
from unittest.mock import patch, MagicMock

from rssreader.output_controller import (SamplePrintController,
                                         JSONPrintController,
                                         PDFPrintController,
                                         HTMLPrintController,
                                         OutputController)


class TestSamplePrintController(unittest.TestCase):
    def setUp(self):
        self.articles = {
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

        self.printer = SamplePrintController()

    def test_print_to(self):
        # without colorize param
        self.printer._print_article = MagicMock(return_value=True)
        self.printer._print_title = MagicMock(return_value=False)
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer.print_to(self.articles))

        self.assertEqual(self.printer._print_article.call_count, 1)

        self.printer._print_title.assert_called_with('Yahoo News - Latest News & Headlines', colorize=False)
        self.assertEqual(self.printer._print_title.call_count, 1)

        self.assertEqual(base_print_mock.call_count, 0)

    def test_print_to_colorize(self):
        # with colorize=True
        self.printer._print_article = MagicMock(return_value=True)
        self.printer._print_title = MagicMock(return_value=False)
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer.print_to(self.articles, colorize=True))

        self.assertEqual(self.printer._print_article.call_count, 1)

        self.printer._print_title.assert_called_with('Yahoo News - Latest News & Headlines', colorize=True)
        self.assertEqual(self.printer._print_title.call_count, 1)

        self.assertEqual(base_print_mock.call_count, 0)

    def test_print_article(self):
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer._print_article(self.articles['articles'][0], colorize=False))

        self.assertEqual(base_print_mock.call_count, 4)

    def test_print_article_colorize(self):
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer._print_article(self.articles['articles'][0], colorize=True))

        self.assertEqual(base_print_mock.call_count, 4)

    def test_print_title(self):
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer._print_title(self.articles['title'], colorize=False))

        self.assertEqual(base_print_mock.call_count, 1)

    def test_print_title_colorize(self):
        with patch('builtins.print') as base_print_mock:
            self.assertIsNone(self.printer._print_title(self.articles['title'], colorize=True))

        self.assertEqual(base_print_mock.call_count, 1)


class TestJSONPrintController(unittest.TestCase):
    def setUp(self):
        self.articles = {
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

        self.printer = JSONPrintController()

    def test_print_to(self):
        with patch('json.dumps') as json_mock:
            json_mock.return_value = '{"title": "Yahoo News - Latest News & Headlines", "articles": [{"title": "Some title", "description": "Some long description", "dec_description": "[link 1][Image 2: Alt of image 2] Some long description", "link": "some long link", "pubDate": "Tue, 26 Nov 2019 20:53", "media": [{"src": "some long link to source of image 2", "alt": "Alt of image 2", "width": "130", "height": "86"}], "links": ["some long link", "some long link to source of image 2"], "dec_links": ["[1]: some long link (link)", "[2]: some long link to source of image 2 (image)"]}]}'
            with patch('builtins.print') as print_mock:
                self.assertIsNone(self.printer.print_to(self.articles))

        self.assertEqual(print_mock.call_count, 1)
        self.assertEqual(json_mock.call_count, 1)

        json_mock.assert_called_with(self.articles)
        print_mock.assert_called_with(json.dumps(self.articles))


class TestPDFPrintController(unittest.TestCase):
    pass


class TestHTMLPrintController(unittest.TestCase):
    pass


class TestOutputController(unittest.TestCase):
    def setUp(self):
        self.controller = OutputController()

        self.articles = {
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

        self.filename = 'filename'

    def test_print(self):
        # Sample
        with patch('rssreader.output_controller.SamplePrintController.print_to') as chosen_printer:
            self.assertIsNone(self.controller.print(self.articles))

        chosen_printer.assert_called_once_with(self.articles, colorize=False)

        with patch('rssreader.output_controller.SamplePrintController.print_to') as chosen_printer:
            self.assertIsNone(self.controller.print(self.articles, colorize=True))

        chosen_printer.assert_called_once_with(self.articles, colorize=True)

        # JSON
        with patch('rssreader.output_controller.JSONPrintController.print_to') as chosen_printer:
            self.assertIsNone(self.controller.print(self.articles, to_json=True))

        chosen_printer.assert_called_once_with(self.articles)

        # PDF
        with patch('rssreader.output_controller.PDFPrintController.print_to') as chosen_printer:
            self.assertIsNone(self.controller.print(self.articles, to_pdf='filename'))

        chosen_printer.assert_called_once_with(self.articles, filename='filename')

        # HTML
        with patch('rssreader.output_controller.HTMLPrintController.print_to') as chosen_printer:
            self.assertIsNone(self.controller.print(self.articles, to_html='filename'))

        chosen_printer.assert_called_once_with(self.articles, filename='filename')


if __name__ == '__main__':
    unittest.main()
