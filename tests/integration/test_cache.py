"""
Tests for rssreader.Cache
"""
import unittest
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from rssreader.news import News
from rssreader.feed import Feed
from rssreader.cache import Cache


class CacheTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.feed = Feed('https://dummy.xz/here.rss', 1)
        self.feed.encoding = 'utf-8'
        self.feed.title = 'Dummy news'

        self.first_news = News(
            'First', 'Thu, 30 Oct 2019 10:25:00 +0300', datetime(2019, 10, 30, 10, 25, 11), 'https://dummy.xz/1',
            'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]
        )

        self.second_news = News(
            'Second', 'Thu, 31 Oct 2019 10:25:00 +0300', datetime(2019, 10, 31, 10, 25, 11), 'https://dummy.xz/2',
            'You are winner', [{'type': 'image/bmp)', 'href': 'https://img.dummy.xz/pic2.bmp'}]
        )

        self.feed.news.append(self.first_news)
        self.feed.news.append(self.second_news)

        self.db_name = 'test_rss.db'
        self.db_path = Path().cwd()
        self.db = self.db_path.joinpath(self.db_name)

        # clean up
        if self.db.is_file():
            self.db.unlink()

    def tearDown(self) -> None:
        self.db.unlink()

    def test_add(self) -> None:
        """Test storing into cache"""
        self.cache = Cache(self.db_path, self.db_name)
        self.assertTrue(os.path.isfile(self.db), 'Cache DB has not been created!')

        self.cache.add(self.feed)
        # test cached data
        self.connection = sqlite3.connect(f'file:{self.db}?mode=rw', uri=True)

        # test common feed data
        cursor = self.connection.cursor()
        cursor.execute('select url, title, encoding from feed')
        result = cursor.fetchall()
        self.assertEqual(1, len(result))
        self.assertEqual((self.feed.url, self.feed.title, self.feed.encoding), result[0])

        # test news
        cursor.execute('select link, title, published, published_dt, description from news')
        result = cursor.fetchall()
        self.assertEqual(2, len(result))

        for i in range(0, 2):
            with self.subTest(i=i):
                self.assertEqual(
                    (self.feed.news[i].link, self.feed.news[i].title, self.feed.news[i].published,
                     str(self.feed.news[i].published_dt), self.feed.news[i].description),
                    result[i])

        # load into cache one more time
        self.cache = Cache(self.db_path, self.db_name)
        self.cache.add(self.feed)

        # As this data already exist in cache, no news is added
        cursor.execute('select count(*) from news')
        self.assertEqual(2, cursor.fetchone()[0])

    def test_load(self) -> None:
        """Test retrieving data from cache"""
        self.cache = Cache(self.db_path, self.db_name)
        self.cache.add(self.feed)

        # create a new clean feed
        self.feed = Feed(self.feed.url, limit=None, published_from=datetime(2019, 10, 3, 0, 0, 0))

        # All news is loaded as there was no restriction by limit
        self.open_connection()
        self.cache.load(self.feed)
        self.assertEqual(2, len(self.feed.news))

        # One news is loaded because of specified limit
        self.feed = Feed(self.feed.url, limit=1, published_from=datetime(2019, 10, 3, 0, 0, 0))
        self.open_connection()
        self.cache.load(self.feed)
        self.assertEqual(1, len(self.feed.news))

        # There is no news published from this date
        self.feed = Feed(self.feed.url, limit=None, published_from=datetime(2019, 11, 1, 0, 0, 0))
        self.open_connection()
        self.cache.load(self.feed)
        self.assertEqual(0, len(self.feed.news))

        # cannot operate on a closed database. Connection is closed inside load method.
        with self.assertRaises(sqlite3.ProgrammingError) as cm:
            self.cache.load(self.feed)

    def open_connection(self) -> None:
        self.cache = Cache(self.db_path, self.db_name)
        self.connection = sqlite3.connect(f'file:{self.db}?mode=rw', uri=True)
