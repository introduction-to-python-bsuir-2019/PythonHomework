"""Contain unit tests of rss-reader objects."""
import json
import sys
from datetime import datetime
from io import StringIO
from unittest import mock, TestCase

import rss_reader.rss_reader
from rss_reader.cache_storage import CacheStorage, ReadCache, WriteCache
from rss_reader.containers import DictionaryValues, DateTimeSerializer
from rss_reader.display_news import DisplayNewsJSON, DisplayNewsText, format_to_display
from rss_reader.exceptions import (RSSNewsCacheError, RSSConvertationException, RSSCreateImageException,
                                   RSSCreateImageFolderException, RSSNewsDisplayError, RSSReaderParseException)
from rss_reader.format_converter import Converter, format_to_convert
from rss_reader.source_parser import DescriptionParser, SourceParser


class TestFormatFunctions(TestCase):
    def setUp(self):
        self.data = get_cache_data().get('data')

    def test_format_to_display_valid_params(self):
        expected_data = self.get_expected_display_data()
        self.assertEqual(format_to_display(self.data), expected_data, f'Should be {expected_data}')

    def test_format_to_convert_valid_params(self):
        expected_data = self.get_expected_convert_data()
        self.assertEqual(format_to_convert(self.data), expected_data, f'Should be \'{expected_data}\'')

    @staticmethod
    def get_expected_display_data():
        return {'feed': 'Feed & title', 'news': [
            {
                'link': 'http://test1/rss.html',
                'links':
                [
                    {'link': 'http://test/news.html', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'type': 'image'}
                ],
                'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
                'text': 'Mocked first text Mocked second text',
                'title': 'Title 1'
            },
            {
                'link': 'http://test2/rss.html',
                'links':
                [
                    {'link': 'http://test/news.html', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'type': 'image'}
                ],
                'published': 'Mon, 60 Bum 2019 04:90:44 +0300',
                'text': 'Mocked first text Mocked third text',
                'title': 'Title № 2'
            },
            {
                'link': 'http://test3/rss.html',
                'links':
                [
                    {'link': 'http://test/news.html', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'type': 'image'}
                ],
                'published': '',
                'text': 'Mocked second text Mocked third text',
                'title': 'Title 3'
            }
        ]}

    @staticmethod
    def get_expected_convert_data():
        return {'feed': 'Feed & title', 'news': [
            {
                'link': 'http://test1/rss.html',
                'description':
                [
                    {'link': '', 'text': 'Mocked first text', 'type': 'text'},
                    {'link': 'http://test/news.html', 'text': 'Mocked second text', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'text': 'Mocked third text', 'type': 'image'}
                ],
                'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
                'title': 'Title 1'
            },
            {
                'link': 'http://test2/rss.html',
                'description':
                [
                    {'link': '', 'text': 'Mocked first text', 'type': 'text'},
                    {'link': 'http://test/news.html', 'text': 'Mocked second text', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'text': 'Mocked third text', 'type': 'image'}
                ],
                'published': 'Mon, 60 Bum 2019 04:90:44 +0300',
                'title': 'Title № 2'
            },
            {
                'link': 'http://test3/rss.html',
                'description':
                [
                    {'link': '', 'text': 'Mocked first text', 'type': 'text'},
                    {'link': 'http://test/news.html', 'text': 'Mocked second text', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'text': 'Mocked third text', 'type': 'image'}
                ],
                'published': '',
                'title': 'Title 3'
            }
        ]}


class TestDisplayNewsText(TestCase):
    def setUp(self):
        data = get_display_data()
        self.display_news = DisplayNewsText(data, False)
        self.display_news_colorize = DisplayNewsText(data, True)

    def test_print_news_valid_params(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.display_news.print_news()
        sys.stdout = sys.__stdout__
        self.assertTrue(captured_output.getvalue())

    def test_get_news_feed_valid_params(self):
        feed_title = 'Test title'
        expected_text = '\x1b[32mFeed: Test title:\x1b[39m\n\n'
        self.assertEqual(self.display_news_colorize._get_news_feed(feed_title),
                         expected_text,
                         f'Should be \'{expected_text}\'')
        expected_text = expected_text.replace('[32m', '[39m')
        self.assertEqual(self.display_news._get_news_feed(feed_title),
                         expected_text,
                         f'Should be \'{expected_text}\'')

    def test_get_news_text_valid_params(self):
        news_data = self.get_news_data()
        expected_text = self.get_expected_news_text()
        self.assertEqual(self.display_news_colorize._get_news_text(1, news_data),
                         expected_text,
                         f'Should be \'{expected_text}\'')
        for value in ['[31m', '[36m']:
            expected_text = expected_text.replace(value, '[39m')
        self.assertEqual(self.display_news._get_news_text(1, news_data),
                         expected_text,
                         f'Should be \'{expected_text}\'')

    @staticmethod
    def get_news_data():
        return {
            'link': 'http://test1/rss.html',
            'links': [
                {'link': 'http://test/news.html', 'type': 'link'},
                {'link': 'http://test/news.jpg', 'type': 'image'}
            ],
            'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
            'text': 'Mocked first text Mocked second text Mocked third text',
            'title': 'Title 1'
        }

    @staticmethod
    def get_expected_news_text():
        return (
            '\x1b[31m[News: 1]\x1b[39m\n'
            'Title: Title 1\n'
            'Date: Sun, 20 Oct 2019 04:21:44 +0300\n'
            'Link: http://test1/rss.html\n'
            '\n'
            'Mocked first text Mocked second text Mocked third text\n'
            '\n'
            '\x1b[36mLinks:\x1b[39m\n'
            '[1]: http://test/news.html (link)\n'
            '[2]: http://test/news.jpg (image)\n'
            '\n'
            '\n'
        )


class TestDisplayNewsJSON(TestCase):
    def setUp(self):
        self.correct_json = self.get_correct_JSON()
        self.incorrect_json = self.get_incorrect_json()
        data = get_display_data()
        self.display_news_correct = DisplayNewsJSON(data)
        self.display_news_incorrect = DisplayNewsJSON({})

    @mock.patch('rss_reader.display_news.DisplayNewsJSON.validate_json')
    def test_print_news_valid_params(self, moked_validate_json):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.display_news_correct.print_news()
        sys.stdout = sys.__stdout__
        self.assertTrue(captured_output.getvalue())

    @mock.patch('rss_reader.display_news.DisplayNewsJSON.read_json_schema_file')
    def test_validate_json_valid_params(self, moked_read_json_schema_file):
        moked_read_json_schema_file.return_value = self.correct_json
        self.display_news_correct.validate_json()

    @mock.patch('rss_reader.display_news.DisplayNewsJSON.read_json_schema_file')
    def test_validate_json_invalid_params(self, moked_read_json_schema_file):
        moked_read_json_schema_file.return_value = self.incorrect_json
        with self.assertRaises(RSSNewsDisplayError) as exception_context:
            self.display_news_correct.validate_json()
        self.assertTrue(isinstance(exception_context.exception, RSSNewsDisplayError) and
                        exception_context.exception.message == 'Invalid JSON schema')
        moked_read_json_schema_file.return_value = self.correct_json
        with self.assertRaises(RSSNewsDisplayError) as exception_context:
            self.display_news_incorrect.validate_json()
        self.assertTrue(isinstance(exception_context.exception, RSSNewsDisplayError) and
                        exception_context.exception.message == 'Well-formed but invalid JSON')

    @mock.patch('json.load')
    @mock.patch('builtins.open', create=True)
    @mock.patch('os.path.isfile', return_value=True)
    def test_read_json_schema_file_valid_params(self, moked_isfile, moked_open, moked_json_load):
        moked_json_load.return_value = self.correct_json
        self.assertEqual(self.display_news_correct.read_json_schema_file('test.json'),
                         self.correct_json, f'Should be \'{self.correct_json}\'')

    @mock.patch('json.load')
    @mock.patch('builtins.open', create=True)
    @mock.patch('os.path.isfile')
    def test_read_json_schema_file_invalid_params(self, moked_isfile, moked_open, moked_json_load):
        moked_json_load.return_value = self.correct_json
        moked_isfile.return_value = False
        with self.assertRaises(RSSNewsDisplayError) as exception_context:
            self.display_news_correct.read_json_schema_file(None)
        self.assertTrue(isinstance(exception_context.exception, RSSNewsDisplayError) and
                        exception_context.exception.message == 'Can\'t read json schema.')
        moked_json_load.side_effect = json.decoder.JSONDecodeError('', '', 0)
        moked_isfile.return_value = True
        with self.assertRaises(RSSNewsDisplayError) as exception_context:
            self.display_news_correct.read_json_schema_file(None)
        self.assertTrue(isinstance(exception_context.exception, RSSNewsDisplayError) and
                        exception_context.exception.message == 'Poorly-formed text, not JSON')

    @staticmethod
    def get_correct_JSON():
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Feed json schema",
            "description": "JSON schema used by rss_news to print RSS feed news in stdout.",
            "properties": {
                "feed": {
                    "type": "string",
                    "title": "Feed",
                    "description": "Title of the RSS feed."
                },
                "news": {
                    "type": "array",
                    "title": "News",
                    "items": {
                        "type": "object",
                        "title": "News",
                        "properties": {
                            "title": {
                                "type": "string",
                                "title": "Title",
                                "description": "Title of the news."
                            },
                            "published": {
                                "type": "string",
                                "title": "Date",
                                "description": "Date and time of publication of the news."
                            },
                            "link": {
                                "type": "string",
                                "title": "Link",
                                "description": "Link of the news."
                            },
                            "text": {
                                "type": "string",
                                "title": "Description",
                                "description": "Description text of the news."
                            },
                            "links": {
                                "type": "array",
                                "title": "Links and images used in news description.",
                                "items": {
                                    "type": "object",
                                    "title": "News",
                                    "properties": {
                                        "link": {
                                            "type": "string",
                                            "title": "Link",
                                            "description": "Link to adress or image."
                                        },
                                        "type": {
                                            "type": "string",
                                            "title": "Type",
                                            "description": "Type of link"
                                        }
                                    },
                                    "required": [
                                        "link",
                                        "type"
                                    ],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": [
                                "title",
                                "published",
                                "link",
                                "text",
                                "links"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            "required": [
                "feed",
                "news"
            ],
            "additionalProperties": False
        }

    @staticmethod
    def get_incorrect_json():
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Feed json schema",
            "description": "JSON schema used by rss_news to print RSS feed news in stdout.",
            "properties": True
        }


class TestSourceParser(TestCase):
    def setUp(self):
        self.source = 'http://test/rss'
        self.parser = SourceParser(self.source)

    @mock.patch('rss_reader.source_parser.DescriptionParser')
    def test_get_source_data_valid_params(self, mocked_description_parser):
        mocked_description = mock.Mock()
        mocked_description.parse_description.return_value = None
        mocked_description.text = ['Mocked first text', 'Mocked second text', 'Mocked third text']
        news_data = get_cache_data()
        mocked_description.links = news_data.get('links')
        mocked_description.structure = news_data.get('structure')
        mocked_description_parser.return_value = mocked_description
        entries = self.get_news_entries()
        source_data = {'feed': {'title': 'Feed &#38; title'}, 'entries': entries}
        expected_cache_data = self.get_expected_cache_data(mocked_description.links, mocked_description.structure)
        self.parser.parse_source_data(source_data)
        self.assertEqual(self.parser.cache_data, expected_cache_data, f'Should be \'{expected_cache_data}\'')

    @mock.patch('feedparser.parse')
    def test_get_parse_source_data_valid_params(self, mocked_parse):
        mocked_source_data = mock.Mock()
        mocked_source_data.feed = {'Title': 'Test data'}
        mocked_source_data.bozo = 0
        mocked_parse.return_value = mocked_source_data
        source_data = self.parser.get_source_data()
        self.assertEqual(source_data.feed, mocked_source_data.feed, f'Should be \'{mocked_source_data.feed}\'')

    @mock.patch('feedparser.parse')
    def test_get_source_data_invalid_params(self, mocked_parse):
        mocked_source_data = mock.Mock()
        mocked_source_data.feed = {'Title': 'Test data'}
        mocked_source_data.bozo = 1
        mocked_parse.return_value = mocked_source_data
        with self.assertRaises(RSSReaderParseException) as exception_context:
            self.parser.get_source_data()
        self.assertTrue(isinstance(exception_context.exception, RSSReaderParseException) and
                        exception_context.exception.message == 'Invalid or inaccessible RSS URL')

    def get_expected_cache_data(self, links, structure):
        return [
            {
                'source': self.source, 'feed': 'Feed & title', 'id': '1',
                'date': datetime(2019, 10, 20, 4, 21, 44), 'news':
                {
                    'title': 'Title 1',
                    'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
                    'link': 'http://test1/rss.html',
                    'text': 'Mocked first text Mocked second text Mocked third text',
                    'links': links,
                    'description': structure
                }
            },
            {
                'source': self.source, 'feed': 'Feed & title', 'id': '2',
                'date': self.parser._empty_published, 'news':
                {
                    'title': 'Title № 2',
                    'published': 'Mon, 60 Bum 2019 04:90:44 +0300',
                    'link': 'http://test2/rss.html',
                    'text': 'Mocked first text Mocked second text Mocked third text',
                    'links': links,
                    'description': structure
                }
            },
            {
                'source': self.source, 'feed': 'Feed & title', 'id': '3',
                'date': self.parser._empty_published, 'news':
                {
                    'title': 'Title 3',
                    'published': '',
                    'link': 'http://test3/rss.html',
                    'text': 'Mocked first text Mocked second text Mocked third text',
                    'links': links,
                    'description': structure
                }
            }
        ]

    @staticmethod
    def get_news_entries():
        return [{'title': 'Title &#8470; 2', 'link': 'http://test2/rss.html', 'published_parsed': 2,
                 'published': 'Mon, 60 Bum 2019 04:90:44 +0300', 'id': '2'},
                {'title': 'Title 1', 'link': 'http://test1/rss.html', 'published_parsed': 3,
                 'published': 'Sun, 20 Oct 2019 04:21:44 +0300',  'id': '1'},
                {'title': 'Title 3', 'link': 'http://test3/rss.html', 'published_parsed': 1,
                 'published': '', 'id': '3'}]


class TestDescriptionParser(TestCase):
    def setUp(self):
        self.description = DescriptionParser('http://test/rss.html')

    @mock.patch('bs4.BeautifulSoup')
    @mock.patch('rss_reader.source_parser.DescriptionParser._parse_description_data')
    def test_parse_description_valid_params(self, mocked_parse_description_data, mocked_beautiful_soup):
        mocked_parse_description_data.return_value = None
        mocked_beautiful_soup.return_value = {}
        self.description.parse_description('Test')

    @mock.patch('rss_reader.source_parser.DescriptionParser._update_structure')
    @mock.patch('rss_reader.source_parser.DescriptionParser._parse_description_tag')
    def test_parse_description_data_valid_params(self, mocked_parse_description_tag, mocked_update_structure):
        mocked_objs = []
        mock_obj_data = [([], 'a', 'Test \'a\' string'),
                         ([], 'img', None),
                         (None, None, 'Test &#171;correct&#187; string'),
                         (None, None, '  \n ')]
        for child_generator, name, string in mock_obj_data:
            mocked_obj = mock.Mock()
            mocked_obj.childGenerator.return_value = child_generator
            mocked_obj.name = name
            mocked_obj.string = string
            mocked_objs.append(mocked_obj)
        mocked_data = mock.Mock()
        mocked_data.childGenerator.return_value = mocked_objs
        expected_text = ['Test «correct» string']
        self.description._parse_description_data(mocked_data)
        self.assertEqual(self.description.text, expected_text, f'Should be \'{expected_text}\'')
        self.description.text.clear()

    @mock.patch('rss_reader.source_parser.DescriptionParser._update_structure')
    def test_parse_description_tag_valid_params(self, mocked_update_structure):
        veriants = self.get_parse_description_tag_variants()
        for expected_links, expected_text, link_text, tag_attrs, start_links, search_attr, tag_type in veriants:
            self.description.links = start_links
            mocked_tag = mock.Mock()
            mocked_tag.attrs = tag_attrs
            mocked_tag.string = link_text
            self.description._parse_description_tag(mocked_tag, search_attr, tag_type)
            self.assertEqual(self.description.links, expected_links, f'Should be \'{expected_links}\'')
            self.assertEqual(self.description.text, expected_text, f'Should be \'{expected_text}\'')
            self.description.links.clear()
            self.description.text.clear()

    def test_update_structure_valid_params(self):
        variants = self.get_update_structure_variants()
        for input_structure, expected_result in variants:
            self.description._update_structure(input_structure)
            self.assertEqual(self.description.structure, expected_result, f'Should be \'{expected_result}\'')
            self.description.structure.clear()

    def test_format_string_valid_params(self):
        input_string = 'string,  that contains   \n random  amount\r   of  \t  spaces'
        expected_string = 'string, that contains random amount of spaces'
        self.assertEqual(self.description.format_string(input_string),
                         expected_string,
                         f'Should be \'{expected_string}\'')

    @staticmethod
    def get_parse_description_tag_variants():
        return [
            (
                [{'link': 'http://test/news.html', 'type': 'link'}],
                ['[link 1: Test «title»][1]'],
                'Test &#171;title&#187;',
                {'href': 'http://test/news.html'},
                [],
                'href',
                'link'
            ),
            (
                [{'link': 'http://test/news.html', 'type': 'link'},
                 {'link': 'http://test/news.jpg', 'type': 'image'}],
                ['[image 2: Test title][2]'],
                'Test title',
                {'src': '/news.jpg'},
                [{'link': 'http://test/news.html', 'type': 'link'}],
                'src',
                'image'
            ),
            (
                [{'link': 'http://test/news.jpg', 'type': 'image'}],
                ['[image 1]'],
                '',
                {'src': 'http://test/news.jpg'},
                [{'link': 'http://test/news.jpg', 'type': 'link'}],
                'src',
                'image'
            ),
            (
                [],
                [],
                'Test title',
                {'src': 'http://test/news.html'},
                [],
                'href',
                'link'
            )
        ]

    @staticmethod
    def get_update_structure_variants():
        return [({'text': 'test_text', 'type': 'test_type', 'link': 'test_link'},
                [{'text': 'test_text', 'type': 'test_type', 'link': 'test_link'}]),
                ({'not_need': 'test_not_need', 'type': 'test_type', 'link': 'test_link'},
                 [{'not_need': 'test_not_need', 'text': '', 'type': 'test_type', 'link': 'test_link'}]),
                ({'type': 'test_type', 'not_need': 200},
                 [{'not_need': 200, 'text': '', 'type': 'test_type', 'link': ''}]),
                ({},
                 [{'text': '', 'type': '', 'link': ''}])]


class TestCacheStorage(TestCase):
    def setUp(self):
        self.cache_file = 'rss.json'
        self.cache_storage = CacheStorage('http://test/rss')

    @mock.patch('tinydb.TinyDB')
    @mock.patch('os.path.isfile', return_value=True)
    def test_read_json_schema_file_valid_params(self, moked_isfile, moked_tinydb):
        moked_tinydb.table = True
        self.assertTrue(self.cache_storage.init_cache_db(self.cache_file))

    @mock.patch('os.path.isfile', return_value=False)
    def test_read_json_schema_file_invalid_params(self, moked_isfile):
        with self.assertRaises(RSSNewsCacheError) as exception_context:
            self.cache_storage.init_cache_db(self.cache_file)
        self.assertTrue(isinstance(exception_context.exception, RSSNewsCacheError) and
                        exception_context.exception.message == 'Can\'t read cache JSON file.')


class TestReadCache(TestCase):
    def setUp(self):
        self.date = datetime(2019, 11, 20, 22, 10, 00)
        self.cache_storage = ReadCache('http://test/rss.json', self.date)

    def test_get_end_of_the_period_valid_params(self):
        expected_date = datetime(2019, 11, 20, 23, 59, 59)
        self.assertEqual(self.cache_storage.get_end_of_the_period(self.date),
                         expected_date, f'Should be \'{expected_date}\'')

    @mock.patch('tinydb.Query')
    def test_read_cache_valid_params(self, moked_tiny_db_query):
        mock_search = mock.Mock()
        mock_search.date = self.date
        moked_tiny_db_query.return_value = mock_search
        moked_tiny_db_table = mock.Mock()
        moked_tiny_db_table.search.return_value = [
            {'news_data': f'Data {number}', 'date': datetime(2019, 11, 20, hour, 00, 00)}
            for number, hour in [('3', 15), ('2', 21), ('1', 23), ('5', 8), ('4', 10)]
        ]
        expected_result = [
            {'news_data': f'Data {number}', 'date': datetime(2019, 11, 20, hour, 00, 00)}
            for number, hour in [('1', 23), ('2', 21), ('3', 15), ('4', 10), ('5', 8)]
        ]
        self.assertEqual(self.cache_storage.read_cache(moked_tiny_db_table),
                         expected_result, f'Should be \'{expected_result}\'')


class TestWriteCache(TestCase):
    def setUp(self):
        self.data = get_cache_data()
        self.news_data = self.data.get('data')
        self.source = 'http://test/rss.json'
        self.cache_storage = WriteCache(self.source, self.news_data)

    def test_verify_data_valid_params(self):
        self.assertTrue(self.cache_storage.verify_data(next(iter(self.news_data))))
        self.assertFalse(self.cache_storage.verify_data({'id': ''}))
        self.assertFalse(self.cache_storage.verify_data({'id': 'Test', 'date': ''}))

    @mock.patch('tinydb.Query')
    @mock.patch('rss_reader.cache_storage.WriteCache.verify_data')
    def test_cache_news_list_valid_params(self, mocked_verify_data, moked_tiny_db_query):
        links = self.data.get('links')
        structure = self.data.get('structure')
        mocked_verify_data.return_value = True
        mocked_verify_data.side_effect = [True, True, False]
        mock_search = mock.Mock()
        mock_search.source = self.source
        mock_search.id = 'ID'
        moked_tiny_db_query.return_value = mock_search
        moked_tiny_db_table = mock.Mock()
        moked_tiny_db_table.search.side_effect = [None, [{'news': {
            'title': 'Title 2',
            'published': 'Mon, 40 Bum 2019 04:90:44 +0300',
            'link': 'http://test2/rss.html',
            'text': 'Mocked first text Mocked third text',
            'links': links,
            'description': structure
        }}]]
        moked_tiny_db_table.insert_multiple.return_value = None
        moked_tiny_db_table.update.return_value = None
        self.cache_storage.cache_news_list(moked_tiny_db_table)


class TestConverter(TestCase):
    def setUp(self):
        self.data = self.get_converted_data()
        self.converter = Converter(self.data, 'test_html.html', 'test_pdf.pdf')
        self.correct_html_file = 'tests/correct_html_conversion_file.html'

    @mock.patch('rss_reader.format_converter.Converter.conver_to_pdf')
    @mock.patch('rss_reader.format_converter.Converter.conver_to_html')
    @mock.patch('rss_reader.format_converter.Converter.remove_image_folder')
    @mock.patch('rss_reader.format_converter.Converter.get_html')
    @mock.patch('rss_reader.format_converter.Converter.create_image_folder')
    def test_convert_news_valid_params(self, mocked_create_image_folder, mocked_get_html, mocked_remove_image_folder,
                                       mocked_conver_to_html, mocked_conver_to_pdf):
        self.converter.convert_news()

    @mock.patch('rss_reader.format_converter.Converter.conver_to_pdf')
    @mock.patch('rss_reader.format_converter.Converter.conver_to_html')
    @mock.patch('rss_reader.format_converter.Converter.remove_image_folder')
    @mock.patch('rss_reader.format_converter.Converter.get_html')
    @mock.patch('rss_reader.format_converter.Converter.create_image_folder')
    def test_convert_news_invalid_params(self, mocked_create_image_folder, mocked_get_html, mocked_remove_image_folder,
                                         mocked_conver_to_html, mocked_conver_to_pdf):
        mocked_conver_to_html.side_effect = RSSConvertationException('Can\'t create HTML file', None)
        mocked_conver_to_pdf.side_effect = RSSConvertationException('Can\'t create FDP file', None)
        self.assertTrue(self.capture_output().getvalue() == (
            'News is not converted to HTML format, because can\'t save .html file\n'
            'News is not converted to PDF format, because can\'t save .pdf file\n'
        ))
        mocked_get_html.side_effect = RSSCreateImageException('Can\'t create image with path', None)
        self.assertTrue(self.capture_output().getvalue() == (
            'News is not converted, because can\'t save pictures to a images folder\n'
        ))
        mocked_create_image_folder.side_effect = RSSCreateImageFolderException(
            'Can\'t create directory for image files', None
        )
        self.assertTrue(self.capture_output().getvalue() == (
            'News is not converted, because can\'t create a folder for images\n'
        ))

    @mock.patch('os.mkdir')
    @mock.patch('os.path.exists', return_value=False)
    def test_create_image_folder_valid_params(self, mocked_path_exists, mocked_mkdir):
        self.converter.create_image_folder('/test/name.html')
        img_folder = '/test/name'
        self.assertEqual(self.converter.img_folder, img_folder, img_folder)

    @mock.patch('os.mkdir', side_effect=OSError('test'))
    @mock.patch('os.path.exists', return_value=False)
    def test_create_image_folder_invalid_params(self, mocked_path_exists, mocked_mkdir):
        with self.assertRaises(RSSCreateImageFolderException) as exception_context:
            self.converter.create_image_folder('/test/name.html')
        self.assertTrue(isinstance(exception_context.exception, RSSCreateImageFolderException))

    @mock.patch('shutil.rmtree')
    def test_download_image_valid_params(self, mocked_rmtree):
        self.converter.remove_image_folder()

    def test_get_html_valid_params(self):
        with open(self.correct_html_file) as file_obj:
            expected_html = file_obj.read()
            self.assertEqual(self.converter.get_html(False),
                             expected_html, f'Should be \'{expected_html}\'')

    def capture_output(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.converter.convert_news()
        sys.stdout = sys.__stdout__
        return captured_output

    @staticmethod
    def get_converted_data():
        return {'feed': 'Feed & title', 'news': [
            {
                'link': 'http://test1/rss.html',
                'description':
                [
                    {'link': 'http://test/news.html', 'text': 'Mocked second text', 'type': 'link'},
                    {'link': 'http://test/news.jpg', 'text': 'Mocked third text', 'type': 'image'}
                ],
                'published': 'Mon, 21 Oct 2019 04:30:12 +0300',
                'title': 'Title 1'
            },
            {
                'link': 'http://test2/rss.html',
                'description':
                [
                    {'link': 'http://test/auto_news.html', 'text': 'Mocked first text', 'type': 'text'},
                    {'link': '', 'text': 'Mocked third text', 'type': 'image'}
                ],
                'published': 'Sun, 20 Oct 2019 14:21:44 +0300',
                'title': 'Title № 2'
            },
            {
                'link': 'http://test3/rss.html',
                'description':
                [
                    {'link': 'http://test/auto_news.html', 'text': 'Mocked first text', 'type': 'text'},
                    {'link': 'http://test/news.html', 'text': 'Mocked second text', 'type': 'link'},
                ],
                'published': 'Sun, 20 Oct 2019 10:12:36 +0300',
                'title': 'Title 3'
            }
        ]}


class TestContainers(TestCase):

    def test_dictionary_values_valid_params(self):
        input_list = [{'test 1': 'value 1', 'test 2': 1},
                      {'test 1': 'value 3', 'test 2': 3}]
        expected_list = [('value 1', 1), ('value 3', 3)]
        self.assertEqual([(key, value) for key, value in DictionaryValues(input_list)],
                         expected_list, f'Should be \'{expected_list}\'')

    def test_date_time_serializer_valid_params(self):
        serializer = DateTimeSerializer()
        date = datetime(2019, 11, 21, 22, 20, 00)
        date_string = '2019-11-21T22:20:00'
        self.assertEqual(serializer.encode(date),
                         date_string, f'Should be \'{date_string}\'')
        self.assertEqual(serializer.decode(date_string),
                         date, f'Should be \'{date}\'')


def get_display_data():
    return {'feed': 'Feed & title', 'news': [
        {
            'link': 'http://test1/rss.html',
            'links':
            [
                {'link': 'http://test1/news.html', 'type': 'link'}
            ],
            'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
            'text': 'Mocked first text Mocked second text Mocked third text',
            'title': 'Title 1'
        },
        {
            'link': 'http://test2/rss.html',
            'links':
            [
                {'link': 'http://test2/news.html', 'type': 'link'},
                {'link': 'http://test2/news.jpg', 'type': 'image'}
            ],
            'published': 'Mon, 60 Bum 2019 04:90:44 +0300',
            'text': 'Mocked first text Mocked second text Mocked third text',
            'title': 'Title № 2'
        },
        {
            'link': 'http://test3/rss.html',
            'links':
            [
                {'link': 'http://test3/news.jpg', 'type': 'image'}
            ],
            'published': '',
            'text': 'Mocked first text Mocked second text Mocked third text',
            'title': 'Title 3'
        }]}


def get_cache_data():
    source = 'http://test/rss'
    empty_date = datetime.now()
    links = [{'link': 'http://test/news.html', 'type': 'link'},
             {'link': 'http://test/news.jpg', 'type': 'image'}]
    structure = [{'text': 'Mocked first text', 'type': 'text', 'link': ''},
                 {'text': 'Mocked second text', 'type': 'link', 'link': 'http://test/news.html'},
                 {'text': 'Mocked third text', 'type': 'image', 'link': 'http://test/news.jpg'}]
    return {'links': links, 'structure': structure, 'data': [
        {
            'source': source,
            'feed': 'Feed & title',
            'id': '1',
            'date': datetime(2019, 10, 20, 4, 21, 44),
            'news':
            {
                'title': 'Title 1',
                'published': 'Sun, 20 Oct 2019 04:21:44 +0300',
                'link': 'http://test1/rss.html',
                'text': 'Mocked first text Mocked second text',
                'links': links,
                'description': structure
            }
        },
        {
            'source': source,
            'feed': 'Feed & title',
            'id': '2',
            'date': empty_date, 'news':
            {
                'title': 'Title № 2',
                'published': 'Mon, 60 Bum 2019 04:90:44 +0300',
                'link': 'http://test2/rss.html',
                'text': 'Mocked first text Mocked third text',
                'links': links,
                'description': structure
            }
        },
        {
            'source': source,
            'feed': 'Feed & title',
            'id': '3',
            'date': empty_date,
            'news':
            {
                'title': 'Title 3',
                'published': '',
                'link': 'http://test3/rss.html',
                'text': 'Mocked second text Mocked third text',
                'links': links,
                'description': structure
            }
        }
    ]}
