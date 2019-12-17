"""
Tests for rssreader.Cache
"""
from unittest import TestCase
from unittest.mock import patch, call, Mock
from datetime import datetime
from pathlib import Path
from collections import namedtuple
import json

from rssreader.news import News
from rssreader.feed import Feed
from rssreader.cache import Cache


class CacheTestCase(TestCase):
    def setUp(self) -> None:
        self.mock_cache = Mock(db='really/fake/db')
        self.mock_connection = Mock()
        self.mock_connection.__str__ = Mock(return_value=self.mock_cache.db)
        self.mock_connection.cursor = Mock()

    def test__init(self) -> None:
        with patch('sqlite3.connect', return_value='db_conn') as mock_sql3:
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        mock_sql3.assert_called_once_with('file:fake/cache/dir/db?mode=rw', uri=True)
        self.assertEqual(self.cache._connection, 'db_conn')

        # test readonly mode
        with patch('sqlite3.connect', return_value='db_conn') as mock_sql3:
            self.cache = Cache(Path('fake/cache/dir'), 'db', mode='ro')

        mock_sql3.assert_called_once_with('file:fake/cache/dir/db?mode=ro', uri=True)

    def test_create_db(self) -> None:
        with patch('sqlite3.connect', return_value=self.mock_connection):
            Cache._create_db(self.mock_cache)

        self.assertEqual(self.mock_cache.db, self.mock_connection.__str__())
        self.mock_connection.cursor.assert_called()

        self.assertTrue(call() == self.mock_connection.cursor.mock_calls[0])
        self.assertTrue('call().executescript(' in str(self.mock_connection.cursor.mock_calls[1]))
        self.assertTrue(call().close() == self.mock_connection.cursor.mock_calls[2])

    def test_get_feed_id(self) -> None:
        with patch('sqlite3.connect', return_value=self.mock_connection):
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        # existent id is returned
        self.mock_connection.cursor.return_value.fetchone.return_value = [10, 1]
        self.assertEqual(10, self.cache._get_feed_id('tell.me/truth.rss'))

        # check called methods
        self.assertTrue(call() == self.mock_connection.cursor.mock_calls[0])
        self.assertTrue('call().execute(' in str(self.mock_connection.cursor.mock_calls[1]))
        self.assertTrue(call().fetchone() == self.mock_connection.cursor.mock_calls[2])
        self.assertTrue(call().close() == self.mock_connection.cursor.mock_calls[3])

        # there no id
        self.mock_connection.cursor.return_value.fetchone.return_value = None
        self.assertEqual(self.cache._get_feed_id('tell.me/truth.rss'), None)

    def test_insert_news(self) -> None:
        self.feed = Feed('https://dummy.xz/here.rss', 1)

        self.feed.news = [
            News('N1', 'Thu, 30 Oct 2019 10:22:00 +0300', datetime(2019, 10, 30, 10, 22), 'https://dummy.xz/1',
                 'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}]),
            News('N2', 'Thu, 30 Oct 2019 10:22:00 +0300', datetime(2019, 10, 30, 10, 22), 'https://dummy.xz/2',
                 'Everything is ok', [{'type': 'image/jpeg)', 'href': 'https://img.dummy.xz/pic1.jpg'}])
        ]

        with patch('sqlite3.connect', return_value=self.mock_connection):
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        self.cache._insert_news(feed=self.feed, feed_id=0)
        # check called methods
        self.assertTrue(call() == self.mock_connection.cursor.mock_calls[0])
        self.assertTrue("call().execute('insert into news (" in str(self.mock_connection.cursor.mock_calls[1]))
        self.assertTrue("call().execute('insert into news (" in str(self.mock_connection.cursor.mock_calls[2]))
        self.assertTrue(call().close() == self.mock_connection.cursor.mock_calls[3])

    def test_insert_feed(self) -> None:
        with patch('sqlite3.connect', return_value=self.mock_connection):
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        self.mock_connection.cursor.return_value.lastrowid = -20

        self.assertEqual(-20, self.cache._insert_feed(feed=Feed('https://dummy.xz/here.rss', 1)))

        # check called methods
        self.assertTrue(call() == self.mock_connection.cursor.mock_calls[0])
        self.assertTrue("call().execute('insert into feed (" in str(self.mock_connection.cursor.mock_calls[1]))
        self.assertTrue(call().close() == self.mock_connection.cursor.mock_calls[2])

    def test_add(self) -> None:
        feed_data = Feed('https://dummy.rss', None)

        with patch('sqlite3.connect', return_value=self.mock_connection):
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        # Add new feed
        with patch('rssreader.cache.Cache._get_feed_id', return_value=None) as mock_getfeed:
            with patch('rssreader.cache.Cache._insert_feed', return_value=25) as mock_insertfeed:
                with patch('rssreader.cache.Cache._insert_news') as mock_insertnews:
                    self.cache.add(feed_data)

        mock_getfeed.assert_called_once_with(feed_data.url)
        mock_insertfeed.assert_called_once_with(feed_data)
        mock_insertnews.assert_called_once_with(feed_data, 25)

        # Changes have been committed and connection has been closed
        self.assertListEqual([call.commit(), call.close()], self.mock_connection.mock_calls)

        # Add existent feed
        self.mock_connection.reset_mock()

        with patch('rssreader.cache.Cache._get_feed_id', return_value=10) as mock_getfeed:
            with patch('rssreader.cache.Cache._insert_feed', return_value=25) as mock_insertfeed:
                with patch('rssreader.cache.Cache._insert_news') as mock_insertnews:
                    self.cache.add(feed_data)

        mock_getfeed.assert_called_once_with(feed_data.url)
        mock_insertfeed.assert_not_called()
        mock_insertnews.assert_called_once_with(feed_data, 10)  # Feed id is taken from _get_feed_id

        self.assertListEqual([call.commit(), call.close()], self.mock_connection.mock_calls)

    def test_load(self) -> None:
        with patch('sqlite3.connect', return_value=self.mock_connection):
            self.cache = Cache(Path('fake/cache/dir'), 'db')

        feed_data = Feed('lie.me/rss', None)
        # there is no such feed url in the cache
        self.mock_connection.cursor.return_value.fetchone.return_value = None
        self.assertEqual(None, self.cache.load(feed_data))

        # feed exists in the cache
        self.mock_connection.reset_mock()

        DBFeed = namedtuple('DBFeed', ['id', 'title', 'encoding'])
        db_feed = DBFeed(0, 'LiveNews', 'utf-8')

        DBNews = namedtuple('DBNews', ['title', 'published', 'published_dt', 'link', 'description', 'hrefs'])
        db_news = [
            DBNews('N1', 'Thu, 30 Oct 2019 10:22:00 +0300', datetime(2019, 10, 30, 10, 22), 'https://dummy.xz/1',
                   'Everything is ok', '[]'),
            DBNews('N2', 'Thu, 30 Oct 2019 10:22:00 +0300', datetime(2019, 10, 30, 10, 25), 'https://dummy.xz/2',
                   'Everything is really ok', '[{"type": "image/jpeg)", "href": "https://img.dummy.xz/pic1.jpg"}]')
        ]

        self.mock_connection.cursor.return_value.fetchone.return_value = db_feed
        self.mock_connection.cursor.return_value.fetchall.return_value = db_news

        self.cache.load(feed_data)

        # check common feed data
        self.assertEqual(db_feed.title, feed_data.title)
        self.assertEqual(db_feed.encoding, feed_data.encoding)

        # check news
        for i in range(0, 2):
            with self.subTest(i=i):
                for order, field in enumerate(DBNews.__dict__['_fields']):
                    if field == 'hrefs':
                        self.assertEqual(json.loads(db_news[i].__getitem__(order)),
                                         feed_data.news[i].__getattribute__(field))
                    else:
                        self.assertEqual(db_news[i].__getitem__(order), feed_data.news[i].__getattribute__(field))

        # connection has been closed
        self.assertTrue(call.close() in self.mock_connection.mock_calls)
