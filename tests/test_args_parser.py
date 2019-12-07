import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
import time

from app.support_files.rss_parser import Parser
from app.support_files.dtos import Item, Feed


class TestArgsParser(TestCase):

    def setUp(self):
        self.parser = Parser("rss_link")

    def test_parsing_method(self):
        with patch("feedparser.parse") as parse_mock:
            def mock_get(key, default=None):
                mock_dict = {"feed": {"title": "feed_title",
                                      "link": "feed_link"},
                             "entries":
                                 [{"title": "item_title",
                                   "link": "item_link",
                                   "author": "item_author",
                                   "published_parsed": time.struct_time((2019, 11, 30, 13, 45, 0, 5, 334, 0)),
                                   "description": "item_description",
                                   "media_content": []}]}

                return mock_dict.get(key, default)

            attrs = {"bozo": 0,
                     "status": 200,
                     "get": mock_get}
            parse_object_mock = Mock()
            parse_object_mock.configure_mock(**attrs)
            parse_mock.return_value = parse_object_mock
            test_feed = Feed(rss_link="rss_link",
                             title="feed_title",
                             link="feed_link",
                             items=[Item(title="item_title",
                                         link="item_link",
                                         author="item_author",
                                         published_parsed=time.struct_time((2019, 11, 30, 13, 45, 0, 5, 334, 0)),
                                         description="item_description",
                                         img_links=[])])
            self.assertEqual(test_feed, self.parser.parse_feed())

    def test_parsing_method_exception_1(self):
        with patch("feedparser.parse") as parse_mock:
            attrs = {"bozo": 1,
                     "status": 200}
            parse_object_mock = Mock()
            parse_object_mock.configure_mock(**attrs)
            parse_mock.return_value = parse_object_mock
            with self.assertRaises(ConnectionError):
                self.parser.parse_feed()

    def test_parsing_method_exception_2(self):
        with patch("feedparser.parse") as parse_mock:
            attrs = {"bozo": 0,
                     "status": 404}
            parse_object_mock = Mock()
            parse_object_mock.configure_mock(**attrs)
            parse_mock.return_value = parse_object_mock
            with self.assertRaises(ConnectionError):
                self.parser.parse_feed()


if __name__ == "__main__":
    unittest.main()
