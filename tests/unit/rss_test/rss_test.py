"""Tests for rss_reader_ft.rss module"""
import time
import pprint
from unittest import mock
from rss_reader_ft.rss.rss_feed import RSSFeed

class RSSTest():

    @mock.patch('time.time', return_value = 5)
    def test_func(self, mocker):
       
        assert RSSFeed({"source": "https://"}, {}) == True

if __name__ == "__main__":
    RSSTest.test_func()