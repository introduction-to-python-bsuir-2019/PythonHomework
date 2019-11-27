"""Module implements local cache for feeds"""
import logging
import sqlite3
from pathlib import Path
import json
from contextlib import closing

import rssreader


class Cache(rssreader.base.BaseClass):
    """Class to work with cache. Implementation is based on using sqlite3."""
    def __init__(self, cache_dir: Path, db_name: Path = None, mode: str = 'rw') -> None:
        """Initialize cache. Default db name is cache.db"""
        self.db = cache_dir.joinpath(db_name or 'cache.db')
        try:
            self._connection = sqlite3.connect(f'file:{self.db}?mode={mode}', uri=True)
        except sqlite3.OperationalError:
            logging.info(f'There is not db at {self.db}')
            if mode == 'ro':
                self._connection = None
                logging.info('DB will no be created because cache is accessed in readonly mode')
            else:
                self._create_db()

    def _create_db(self) -> None:
        """Create an empty DB"""
        logging.info('Create an empty db to store cached news')
        script = """
            create table feed (
              id       integer primary key autoincrement,
              url      text unique not null,
              title    text not null,
              encoding text not null
            );
            create unique index ui_feed_url on feed (url);

            create table news (
              id             integer primary key autoincrement,
              feed_id	     integer not null,
              title	         text not null null,
              published 	 text not null,
              published_dt	 timestamp not null,
              link	         text not null,
              description	 text,
              hrefs	         text,
              foreign key(feed_id) references feed ( id )
            );
            create unique index ui_news_link on news (link);
            create index ni_news_feed_dt on news (feed_id, published_dt);
        """

        self._connection = sqlite3.connect(f'file:{self.db}?mode=rwc', uri=True)
        cursor = self._connection.cursor()
        cursor.executescript(script)
        cursor.close()

    def _get_feed_id(self, url: str) -> int:
        """Return feed db identifier"""
        logging.info('Get feed id using url')
        cursor = self._connection.cursor()
        cursor.execute('select id from feed where url=?', (url,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]

    def _insert_news(self, feed, feed_id: int) -> None:
        """Insert into db all feed news"""
        logging.info('Store feed news into cache')
        cursor = self._connection.cursor()
        for n in feed.news:
            logging.info(f'Process news "{n.link}"...')
            try:
                cursor.execute(
                    'insert into news (feed_id, title, published, published_dt, link, description, hrefs) '
                    'values (?, ?, ?, ?, ?, ?, ?)',
                    (feed_id, n.title, n.published, n.published_dt, n.link, n.description, json.dumps(n.hrefs),)
                )
                logging.info(f'  successfully inserted (id={cursor.lastrowid})')
            except sqlite3.IntegrityError:
                logging.info('  skipped because it already exists')

        cursor.close()

    def _insert_feed(self, feed: "rssreader.feed.Feed") -> int:
        """Insert general information about the feed"""
        logging.info('Insert a new feed into cache')

        cursor = self._connection.cursor()
        cursor.execute('insert into feed (url, title, encoding) values(?, ?, ?)',
                       (feed.url, feed.title, feed.encoding))
        feed_id = cursor.lastrowid
        cursor.close()
        return feed_id

    def add(self, feed: "rssreader.feed.Feed") -> None:
        """Add feed data into cache"""
        with closing(self._connection) as connection:
            logging.info('Add feed data into cache')

            feed_id = self._get_feed_id(feed.url)
            if not feed_id:
                feed_id = self._insert_feed(feed)
            logging.info(f'Feed id is {feed_id}')

            self._insert_news(feed, feed_id)
            connection.commit()

    def load(self, feed: "rssreader.feed.Feed") -> None:
        """
        Retrieve feed data from cache
        """
        if self._connection is None:
            return

        with closing(self._connection) as connection:
            logging.info('Load data from cache')
            cursor = connection.cursor()

            # load feed data
            logging.info('Load feed info from DB')
            cursor.execute('select id, title, encoding from feed where url = (?)', (feed.url,))
            row = cursor.fetchone()
            if row:
                logging.info('Load news data from DB')
                feed_id, feed.title, feed.encoding = row
                cursor.execute('select title, published, published_dt, link, description, hrefs '
                               'from news '
                               'where feed_id = (?) and published_dt >= (?) '
                               'order by published_dt desc limit ifnull((?), -1)',
                               (feed_id, feed.published_from, feed.limit,))

                for row in cursor.fetchall():
                    feed.add_news(row[0], row[1], row[2], row[3], row[4], json.loads(row[5]))
            else:
                logging.info('This url does not exist in local cache.')
