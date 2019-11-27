import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path

from dateutil import parser as date_parser

from rss_reader.models import Article
from rss_reader.exceptions import CacheError


class CacheHandler:
    def __init__(self, db_path):
        self.logger = logging.getLogger('rss_reader.CacheHandler')
        self.db = sqlite3.connect(db_path.joinpath('feeds.db'))
        self.init_db(db_path)

    def init_db(self, db_path):
        """Create table if not exists"""
        self.logger.info('Create new cache storage.')
        cursor = self.db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS article(id integer primary key autoincrement,
                                                             date timestamp not null,
                                                             feed text not null,
                                                             title text not null,
                                                             content text not null,
                                                             media text not null,
                                                             link text not null unique)''')
        cursor.close()
        self.db.commit()

    def dump_articles(self, feed, source):
        "Dump articles from feed to DB"
        duplicates = 0
        cursor = self.db.cursor()
        for artcl in feed['articles']:
            try:
                cursor.execute('INSERT INTO article (date, feed, title, content, media, link) values(?, ?, ?, ?, ?, ?)',
                               (artcl.date.strftime("%Y%m%d"),
                                source,
                                artcl.title,
                                artcl.content,
                                json.dumps(artcl.media),
                                artcl.link))
            except sqlite3.IntegrityError:
                duplicates += 1
        self.logger.info(f'{duplicates} duplicates was skipped')
        cursor.close()
        self.db.commit()

    def load_articles(self, source, date):
        "Load articles to feed from DB"
        cursor = self.db.cursor()
        cursor.execute('''SELECT * FROM article WHERE feed=? AND date=?''', (source, date.strftime("%Y%m%d")))
        feed = {'feed_name': None, 'articles': []}
        for article in cursor.fetchall():
            feed['articles'].append(Article(date_parser.parse(str(article[1])).date(),
                                            article[3],
                                            article[4],
                                            json.loads(article[5]),
                                            article[6]))
        cursor.close()
        if len(feed['articles']) == 0:
            raise CacheError(f'News from {source} for {date} not found.')
        return feed
