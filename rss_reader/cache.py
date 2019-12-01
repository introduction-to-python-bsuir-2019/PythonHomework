import sqlite3
import logging


file_path = 'cache.db'


class Cache:
    """"This class contains news and methods of work whit cache"""
    cursor = None
    conn = None

    def __init__(self):
        """This method initialize cursor to database"""
        if self.cursor is None:
            Cache._init_cursor()
        else:
            logger = logging.getLogger('rss_reader')
            logger.error("This is singleton class. Use get_cursor")

    @staticmethod
    def _init_cursor():
        Cache.conn = sqlite3.connect(file_path)
        Cache.cursor = Cache.conn.cursor()
        Cache.cursor.execute('''CREATE TABLE IF NOT EXISTS news(id INTEGER PRIMARY KEY, 
         title text, pub_date_key numeric, pub_date text, link text, description text, UNIQUE(link))''')
        Cache.cursor.execute('''CREATE TABLE IF NOT EXISTS links( id INTEGER PRIMARY KEY, 
         link text, news numeric)''')
        Cache.cursor.execute('''CREATE TABLE IF NOT EXISTS media( id INTEGER PRIMARY KEY,
         link text, news numeric)''')

    @staticmethod
    def get_cursor():
        """Static access method. """
        if Cache.cursor is None:
            Cache()
        return Cache.cursor

    @staticmethod
    def commit():
        """This method commit to database database"""
        return Cache.conn.commit()

    @staticmethod
    def close():
        """This method close connection to database"""
        return Cache.conn.close()

    @staticmethod
    def print_news(date):
        """This method print news to std from selected date to database"""
        Cache.get_cursor()
        Cache.cursor.execute('''SELECT * FROM news WHERE pub_date_key = ?''', (date,))
        news = Cache.cursor.fetchall()
        if len(news) == 0:
            return 1
        for elem in news:
            print('\nTitle: ', elem[1])
            print('Date: ', elem[3])
            print('Link: ', elem[4])
            print(f'Description: {elem[5]}\n')
            Cache.cursor.execute('''SELECT * FROM links WHERE news= ?''', (elem[0],))
            links = Cache.cursor.fetchall()
            i = 1
            for link in links:
                print(f'Link[{i}]: ', link[1])
                i = i + 1
            Cache.cursor.execute('''SELECT * FROM media WHERE news= ?''', (elem[0],))
            links = Cache.cursor.fetchall()
            for link in links:
                print(f'Link[{i}]: ', link[1])
                i = i + 1
