"""Tests for rss_reader_ft.db module"""

import unittest
from unittest import mock

from rss_reader_ft.db.mongodb import MongoDatabase
from rss_reader_ft.db.mongodb_config import URL_CONNECTION, DB_NAME, COLLECTION_NAME
from tests.unit.db_test.data import NEWS


class RssParserTestCase(unittest.TestCase):
    """Test cases for MongoDatabase class"""


if __name__ == "__main__":
    unittest.main()

