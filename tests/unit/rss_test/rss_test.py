"""Tests for rss_reader_ft.rss module"""

import unittest

from rss_reader_ft.rss.data_loader import DataLoader


class RssParserTestCase(unittest.TestCase):
    """Test cases for RssParser class"""
    def test__get_rss_from_url(self):
        """Function _get_rss_from_url test"""
        self.assertRaises(TypeError, DataLoader("").upload())
