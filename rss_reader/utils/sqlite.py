"""
Module is for storing and loading news via sqlite3
"""
import dataset
from pathlib import Path
from datetime import datetime, date, timedelta
from dateutil.parser import parse
from functools import partial
from itertools import repeat
import sqlite3
from typing import Tuple, List
import time
from sqlite3 import Error

# datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
# date(2019, 12, 15)
# datetime.strptime(duration, '%HH').time().strftime('%H:%M')

from ..utils.data_structures import News, NewsItem
from ..utils.exceptions import RssNewsException
from ..utils.rss_utils import get_date, parse_date_from_console, dict_factory


class RssDB:
    """
    Storage class uses sqlite3 DB

    Check DB:
    sqlite3 ./rss_reader/sqlite3.db 'pragma integrity_check;'
    """
    _DB = 'sqlite3.db'

    _sql_create_feed_table = """CREATE TABLE IF NOT EXISTS feeds (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            title text NOT NULL,
                                            link text
                                        );"""
    _sql_create_idx_feed_link = 'CREATE UNIQUE INDEX IF NOT EXISTS idx_feed_link on feeds (link);'
    _sql_create_news_table = """CREATE TABLE IF NOT EXISTS news (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    title text NOT NULL,
                                    link text NOT NULL,
                                    published timestamp NOT NULL,
                                    html text NOT NULL,
                                    feed_id integer NOT NULL, 
                                    FOREIGN KEY (feed_id) REFERENCES feeds (id)
                                    );"""
    _sql_create_idx_news_link = 'CREATE UNIQUE INDEX IF NOT EXISTS idx_news_link on news (link);'
    _sql_create_links_table = """CREATE TABLE IF NOT EXISTS links (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    ref text NOT NULL,
                                    news_id integer NOT NULL, 
                                    FOREIGN KEY (news_id) REFERENCES news (id)
                                );"""
    _sql_create_idx_links_ref = 'CREATE UNIQUE INDEX IF NOT EXISTS idx_links_ref on links (ref);'
    _sql_create_imgs_table = """CREATE TABLE IF NOT EXISTS imgs (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        ref text NOT NULL,
                                        news_id integer NOT NULL, 
                                        FOREIGN KEY (news_id) REFERENCES news (id)
                                    );"""
    _sql_create_idx_imgs_ref = 'CREATE UNIQUE INDEX IF NOT EXISTS idx_imgs_ref on imgs (ref);'
    def __init__(self, logger):
        self.logger = logger
        self.connection = partial(sqlite3.connect, self._DB)
        self._init_empty_db()

    def _init_empty_db(self):
        """Init DB in a case of empty DB"""
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(self._sql_create_feed_table)
            cur.execute(self._sql_create_news_table)
            cur.execute(self._sql_create_idx_news_link)
            cur.execute(self._sql_create_links_table)
            cur.execute(self._sql_create_imgs_table)
            cur.execute(self._sql_create_idx_links_ref)
            cur.execute(self._sql_create_idx_imgs_ref)
            cur.close()

    @staticmethod
    def _sql_insert_feed(feed_title: str, feed_link: str = '') -> str:
        return f'REPLACE INTO feeds(title, link) VALUES (?, ?)', (feed_title, feed_link)

    def _get_feed_id(self, news: News) -> Tuple[int, str]:
        """Look for feed in the DB from stored news

        If DB doesn't contain a feed then insert it to a feeds table
        """
        feed_title = news.feed
        feed_link = news.link

        with self.connection() as conn:
            cur = conn.cursor()
            feed = cur.execute('SELECT * FROM feeds WHERE title=?', (feed_title,))
            if not feed.lastrowid:
                feed = cur.execute(*self._sql_insert_feed(feed_title, feed_link))
            feed_id = feed.lastrowid
            if not feed_id:
                self.logger.error(f'Error while writing to sqlite: {self._DB}')
                raise RssNewsException('Writing data to sql failed!')
            cur.close()
        return feed_id, feed_title

    def _store_news_item(self, news_item: NewsItem, feed_id: id):
        news_date = get_date(news_item.published)

        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute('REPLACE INTO news(title, link, published, html, feed_id) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (news_item.title, news_item.link, news_date, news_item.html, feed_id))
            news_id = cur.lastrowid

            # Add news links to the appropriate table links
            news_links = list(zip(news_item.links, repeat(news_id)))
            cur.executemany('REPLACE INTO links(ref, news_id) VALUES (?, ?)', news_links)

            # Add news img to the appropriate table imgs
            news_imgs = list(zip(news_item.imgs, repeat(news_id)))
            cur.executemany('REPLACE INTO imgs(ref, news_id) VALUES (?, ?)', news_imgs)
            cur.close()

    def insert_news(self, news: News):
        """Store current news into DB"""

        feed_id, feed_title = self._get_feed_id(news)
        self.logger.debug(f'News are storing with feed id {feed_id}: {feed_title}')

        # When received feed_id  we store every news_item with a separate cursor connection
        # to avoid connection overtime while performing queries with big amount of data
        for news_item in news.items:
            self._store_news_item(news_item, feed_id)

        self.logger.debug('News are successfully stored into the DB')

    def load_news(self, date_str: str) -> List[NewsItem]:
        news_from_tables = []

        sql_retrieve_news_query = """
                    SELECT 
                        news.id as newsId, 
                        news.title, news.link, news.published, news.html,
                        news.feed_id as feedID,
                        links.ref as linkRef,
                        imgs.ref as imgRef
                    FROM news 
                    JOIN links ON news.id = links.news_id
                    JOIN imgs ON news.id = imgs.news_id
                    WHERE published >= ? AND published < ?
                    """

        with self.connection() as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            news_date = get_date(date_str)
            date_tomorrow = news_date + timedelta(days=1)

            cur.execute(sql_retrieve_news_query, (news_date, date_tomorrow))

            for news in cur.fetchall():
                news_from_tables.append(news)
            cur.close()

        news_ids = {a['newsId'] for a in news_from_tables}
        news_items_output = []
        for news_id in news_ids:
            links = {item.get('linkRef', '') for item in news_from_tables if item.get('newsId', -1) == news_id}
            imgs = {item.get('imgRef', '') for item in news_from_tables if item.get('newsId', -1) == news_id}
            news_item = next(item for item in news_from_tables if item.get('newsId', -1) == news_id)

            news_items_output.append(
                NewsItem(
                    title=news_item.get('title', ''),
                    link=news_item.get('link', ''),
                    html=news_item.get('html', ''),
                    published=get_date(news_item.get('published')).strftime('%Y%m%d'),
                    links=list(links),
                    imgs=list(imgs)
                )
            )
        return news_items_output






