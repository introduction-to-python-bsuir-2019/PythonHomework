"""Tests for rss_reader_ft.conversion module"""

import unittest

from rss_reader_ft.conversion.json_converter import JsonConverter
from rss_reader_ft.conversion.html_converter import HtmlConverter
from tests.unit.conversion_test.data import JSON_STR, NEWS, HTML_STR


class RssParserTestCase(unittest.TestCase):
    """Test cases for FormatConverter class"""

    def test__convert_to_format_json(self):
        """Function convert_to_format test"""
        self.assertEqual(
            JsonConverter(NEWS).convert_to_format(),
            JSON_STR
        )

    def test__convert_to_format_html(self):
        """Function convert_to_format test"""
        self.assertEqual(
            HtmlConverter(NEWS).convert_to_format(),
            HTML_STR
        )


if __name__ == "__main__":
    unittest.main()
