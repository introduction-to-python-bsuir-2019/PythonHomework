import dataset
from pathlib import Path
from datetime import datetime, date
from dateutil.parser import parse
from functools import partial
from itertools import repeat
import sqlite3
import time
from sqlite3 import Error

# datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
# date(2019, 12, 15)
# datetime.strptime(duration, '%HH').time().strftime('%H:%M')

from ..utils.data_structures import News
from ..utils.exceptions import RssNewsException
from ..utils.rss_utils import get_date

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

    _sql_create_imgs_table = """CREATE TABLE IF NOT EXISTS imgs (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        ref text NOT NULL,
                                        news_id integer NOT NULL, 
                                        FOREIGN KEY (news_id) REFERENCES news (id)
                                    );"""

    def __init__(self, logger):
        self.logger = logger
        self.connection = partial(sqlite3.connect, self._DB)
        self._init_empty_db()

    def _init_empty_db(self):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(self._sql_create_feed_table)
            cur.execute(self._sql_create_news_table)
            cur.execute(self._sql_create_idx_news_link)
            cur.execute(self._sql_create_links_table)
            cur.execute(self._sql_create_imgs_table)

    def _sql_insert_feed(self, feed_title: str, feed_link: str = '') -> str:
        return f'REPLACE INTO feeds(title, link) VALUES (?, ?)', (feed_title, feed_link)

    def _insert_news(self, news: News):
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

            for news_item in news.items:

                news_date = get_date(news_item.published)

                cur.execute('REPLACE INTO news(title, link, published, html, feed_id) '
                            'VALUES (?, ?, ?, ?, ?)',
                            (news_item.title, news_item.link, news_date, news_item.html, feed_id))

                news_id = cur.lastrowid

                with conn as cursor_many:
                    # Add news links to the appropriate table links
                    news_links = list(zip(news_item.links, repeat(news_id)))
                    cursor_many.executemany('REPLACE INTO links(ref, news_id) VALUES (?, ?)', news_links)

                    # Add news img to the appropriate table imgs
                    news_imgs = list(zip(news_item.imgs, repeat(news_id)))
                    cursor_many.executemany('REPLACE INTO imgs(ref, news_id) VALUES (?, ?)', news_imgs)

        self.logger.debug('News are successfully stored into the DB')
