"""Tests for rss_reader_ft.db module"""

import unittest

from rss_reader_ft.db.mongodb import MongoDatabase
from rss_reader_ft.db.mongodb_config import URL_CONNECTION, DB_NAME, COLLECTION_NAME
from tests.unit.db_test.data import NEWS


class RssParserTestCase(unittest.TestCase):
    """Test cases for MongoDatabase class"""

    def setUp(self):
        self.test_mongo_db = MongoDatabase(URL_CONNECTION, DB_NAME, COLLECTION_NAME)
        self.test_mongo_db.database_connection()

    def test__get_news(self):
        """Function _get_news test"""
        self.assertEqual(self.test_mongo_db._check_news_feed(NEWS), False)


if __name__ == "__main__":
    unittest.main()
