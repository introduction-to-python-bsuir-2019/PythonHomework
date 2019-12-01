import logging
import json
import feedparser
from datetime import datetime, date
from time import mktime
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc, Date, create_engine
from .news import News, Base
from .json_formatter import Json
from contextlib import contextmanager
from .converter import HtmlConverter, PdfConverter


@contextmanager
def create_session(session):
    "Context manager that creates a session for exchanging data with a database"
    s = session()
    try:
        yield s
    finally:
        s.close()


class RSSReader(object):
    '''Class of RSS reader'''
    def __init__(self, source, limit, date, json, configuration_for_conversion, all, name_of_database='news'):
        logging.info('Initialization of RSS Reader')
        self.source = source
        self.limit = limit
        self.date = date
        self.json = json
        self.configuration_for_conversion = configuration_for_conversion
        self.all = all
        self.news_to_print = []
        self.init_database(name_of_database)

    def init_database(self, name_of_database):
        '''Method initialize interaction with the database'''
        engine = create_engine(f'sqlite:///{name_of_database}')
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine, autocommit=True)
     
    def get_and_parse_news(self):
        '''Method for getting, parsing and saving news from the Internet'''
        logging.info('Getting news')
        news = feedparser.parse(self.source)
        logging.info('Parsing news')
        if news.bozo:
            if news.bozo_exception.args[0].endswith('name\n'):
                raise Exception('Entered URL is not a RSS source')
            else:
                raise news.bozo_exception
        with create_session(self.session) as s:
            list_of_news = news.entries[:self.limit+1] if self.limit else news.entries
            for feed in list_of_news:
                text_of_the_feed = self.parse_html(feed.summary_detail.value)
                title = self.parse_html(feed.title)
                feed_object = News(news.feed.title,
                                   title,
                                   datetime.fromtimestamp(mktime(feed.published_parsed)),
                                   feed.link,
                                   text_of_the_feed,
                                   [image.get('url') for image in feed.media_content],
                                   datetime.today())
                current_feed_in_table = s.query(News).filter(News.link == feed.link).first()
                if not current_feed_in_table:
                    s.add(feed_object)
                else:
                    s.query(News)\
                        .filter(News.link == feed.link)\
                        .update({'date_of_addition': datetime.today()})
        logging.info('All news are cached')

    @staticmethod
    def parse_html(html):
        '''Method that parse html elements from news'''
        logging.info('Parsing content of the news in HTML format')
        parser = BeautifulSoup(html, 'html.parser')
        return parser.getText()

    def get_cached_news(self):
        '''Method for getting cached news by date'''
        logging.info('Getting news from cache by date')
        with create_session(self.session) as s:
            if self.limit:
                self.news_to_print.extend(s.query(News).filter(func.date(News.date) == self.date).limit(self.limit).all())
            else:
                self.news_to_print.extend(s.query(News).filter(func.date(News.date) == self.date).all())
            if not self.news_to_print:
                raise Exception('No cached news on this date')

    def get_all_news(self):
        '''Method getting all news from database'''
        logging.info('Getting all news from cache')
        with create_session(self.session) as s:
            self.news_to_print = s.query(News).all()
            if not self.news_to_print:
                raise Exception('No cached news')

    def get_news_to_print(self):
        '''Getting news that will be printed'''
        logging.info('Receiving news that will be displayed')
        with create_session(self.session) as s:
            if self.limit:
                self.news_to_print = s.query(News)\
                                      .filter(func.Date(News.date_of_addition) == datetime.today().date())\
                                      .order_by(News.date_of_addition.desc())\
                                      .limit(self.limit)\
                                      .all()
            else:
                self.news_to_print = s.query(News)\
                                      .filter(func.Date(News.date_of_addition) == datetime.today().date())\
                                      .order_by(News.date_of_addition.desc())\
                                      .all()

    def print_news(self):
        '''Method that print news in sys.stdout'''
        logging.info('Print news')
        if self.json:
            print(Json(self.news_to_print))
            return
        for feed in self.news_to_print:
            print(feed)
            print('='*77)

    def exec(self):
        '''Method implements execution of RSS reader'''
        logging.info('Starting work of the RSS Reader')
        try:
            if self.all:
                self.get_all_news()
            elif self.date:
                self.get_cached_news()
            else:
                self.get_and_parse_news()
                self.get_news_to_print()
            self.print_news()
            if 'pdf' in self.configuration_for_conversion:
                PdfConverter(self.news_to_print, self.configuration_for_conversion.get('pdf')).convert()
            if 'html' in self.configuration_for_conversion:
                HtmlConverter(self.news_to_print, self.configuration_for_conversion.get('html')).convert()
        except Exception as e:
            print(e)
