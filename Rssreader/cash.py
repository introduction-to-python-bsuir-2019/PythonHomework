import sqlite3
from Rssreader.SourseReader import NewsReader
from sqlite3 import Error
import logging
import os.path

class_name = 'SQL_Cashing '


class StoreCashSql():
    '''Class for cash collection with using sqlite database'''

    def __init__(self, url, db_file=None):
        '''Initialize cash db '''
        self.url = url
        self.db = 'cash.db'
        self.ready_database = 'cash.db'
        try:
            self.conn = sqlite3.connect(self.db)
        
        except sqlite3.OperationalError:
            self.create_db()
            self.insert_news()

    def create_db(self):
        '''Create an empty DB for cash collection,
            all elements based on feed elements
                                                    '''

        logging.info(class_name + 'Creating new database...')

        news_table_creation = '''
                                CREATE TABLE IF NOT EXISTS news (
                                    url text NOT NULL,
                                    feed text NOT NULL,
                                    title text NOT NULL,
                                    published text NOT NULL,
                                    short_date integer NOT NULL,
                                    link text unique,
                                    description text NOT NULL,
                                    image text NOT NULL,
                                    other_links text NOT NULL
                                    ); '''

        try:
            cur = self.conn.cursor()
            cur.execute(news_table_creation)

        except Error as e:
            print(e)

    def insert_news(self, conn, mynews):
        '''Function for inserting information into database'''
        if not self.ready_database:
            self.create_db()

        sql = '''INSERT INTO news (url,feed,title,published,short_date,link,description,image,other_links)
                    VALUES(?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        try:
            cur.execute(sql, mynews)
        except sqlite3.IntegrityError:
            logging.info('This news has already been cashed')

        return cur.lastrowid

    def news_add(self, news_feed):
        '''Add news after parsing into database'''
        logging.info(class_name + 'Adding news into database')
        if not self.ready_database:
            self.create_db()
        with self.conn:
            for item in news_feed:
                gotnews = (self.url, item['feed'], item['title'], item['date'],
                           item['simple_date'], item['link'], item['description'],
                           item['image'], item['links'])

                self.insert_news(self.conn, gotnews)

    def show_logs(self, url, date, limit):
        logging.info(class_name+'Injecting data from Sqlite databse')
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM news WHERE short_date = (?) and url = (?)', (date, self.url, ))
        row = cur.fetchall()
        if len(row) == 0:
            print('No news was published on this day .')
        for item in row[:limit]:
            print(f'Feed: {item[1]}\n\n Title: {item[2]}\n\n Date: {item[3]}\n\n Description: {item[6]}\n',)
            print(f'Provided links: {item[-1]}\n Provided image: {item[-2]}\n')
            print('-'*80)

    def SqlCashing(self, news_feed):
        '''Function for running functions which work with database'''
        self.create_db()
        self.news_add(news_feed)
