from bs4 import BeautifulSoup
import feedparser
import sqlite3
import logging
import json
import datetime
import os
from dateutil.parser import parse


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class RssHandler:

    def __init__(self, url: str):
        self.url = url
        self.feed = None
        self.feed_dict = {}
        self.json_feed = None

        self.url_handler()
        self.rss_dict()

    def url_handler(self):
        """Takes URL and return rss object"""
        self.feed = feedparser.parse(self.url)
        logging.info("RSS-Feed was parsed.")

    def rss_dict(self):
        """Make dictionary from RSS-Feed"""
        self.feed_dict['source'] = self.feed['feed']['title']
        self.feed_dict['news'] = []

        for descr in self.feed['entries']:
            soup = BeautifulSoup(descr['summary'], 'lxml')
            links = set(link.get('href') for link in soup.find_all('a'))
            media = set(pic.get('src') for pic in soup.find_all('img'))
            self.feed_dict['news'].append({'title': descr['title'], 'pubDate': descr['published'],
                                          'text': soup.get_text(), 'links': links,
                                           'media': media, 'src_link': descr['link']})

        logging.info('Created dictionary from parsed RSS-Feed.')

    def to_json(self, limit):
        """Make JSON file from RSS"""
        json_dict = self.feed_dict.copy()
        json_dict['news']
        if limit is not None:
            del(json_dict['news'][limit:])
        self.json_feed = json.dumps(json_dict, cls=SetEncoder)
        logging.info('Created JSON object from dictionary.')

    def output(self, json_param, limit):
        """Outputs information in stdout"""
        logging.info('Printing RSS-Feed in stdout.')
        if not json_param:
            print(f"\nFeed: {self.feed_dict['source']}")
            for elem in self.feed_dict['news']:
                if self.feed_dict['news'].index(elem) == limit:
                    break
                print(f"""
Title: {elem['title']}
Published: {elem['pubDate']}
Source link: {elem['src_link']}

{elem['text']}

                      """)

                print('Links:')
                for (count, link) in enumerate(elem['links'].union(elem['media'])):
                    print(f'[{count + 1}]{link}')
                print('-'*80)
        else:
            logging.info('Printing JSON object created from RSS-Feed in stdout.')
            self.to_json(limit)
            print(self.json_feed)


class CacheControl:

    def __init__(self, date=None):
        self.conn = None
        self.cursor = None
        self.date = date

    def connect_db(self):
        dbpath = os.path.join(os.path.dirname(__file__), 'newscache.db')
        logging.info('Connecting to the cache database at %s' % dbpath)
        self.conn = sqlite3.connect(dbpath)
        self.cursor = self.conn.cursor()

    def _table_exists(self, tbl_name):
        """Check if table exists"""
        self.connect_db()
        logging.info('Checking if table exists.')
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tbl_name])
        if self.cursor.fetchone() is None:
            logging.info('There is no such table.')
            return False
        else:
            logging.info("Table already exists.")
            return True

        self.conn.commit()
        logging.info('Closing connection with database')
        self.conn.close()

    def insert_values(self, tbl_name, values):
        """Inserts values into the table"""
        self.connect_db()
        if len(values) != 7:
            raise KeyError(f'Given {len(values)} params, but expected 7!')

        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tbl_name}
                               (title text, pubTime text, content text, other_links text,
                                media_links text, src_link text, feed text)""")

        if self._row_exists(tbl_name, values):
            return None

        logging.info('Inserting values in the table.')
        self.cursor.execute(f"""INSERT INTO {tbl_name}
                                VALUES(?,?,?,?,?,?,?)""", values)

        self.conn.commit()
        logging.info('Closing connection with database')
        self.conn.close()

    def cache_output(self, limit):
        "Outputs news from cache in stdout."
        self.date = 'date' + self.date
        if not self._table_exists(self.date):
            raise KeyError('There is no cache for this date!')
        elif self.date is None:
            raise TypeError('Date is required for this iperation!')

        logging.info('Printing RSS-Feed in stdout.')
        self.cursor.execute(f"SELECT * FROM {self.date} ORDER BY puBtime")
        feed_list = self.cursor.fetchall()
        print(f'\nDate: {parse(self.date[4:]).date()}\n')
        for row in feed_list:
            if feed_list.index(row) == limit:
                break
            print(f"""
Title: {row[0]}
Published: {row[1]}
Feed: {row[6]}
Source link: {row[5]}

{row[2]}

                  """)

            print('Links:')
            for (count, link) in enumerate((row[3]+''+row[4]).split()):
                print(f'[{count + 1}]{link}')
            print('-'*80)

        self.conn.commit()
        logging.info('Closing connection with database')
        self.conn.close()

    def _row_exists(self, tbl_name, values):
        "Check if given row exist"
        self.connect_db()
        self.cursor.execute(f"""SELECT * FROM {tbl_name} WHERE title=? AND
                              pubTime=? AND content=? AND other_links=? AND
                                media_links=? AND src_link=? AND feed=?""", values)

        if self.cursor.fetchall() == []:
            return False
        else:
            return True

        self.conn.commit()
        logging.info('Closing connection with database')
        self.conn.close()
