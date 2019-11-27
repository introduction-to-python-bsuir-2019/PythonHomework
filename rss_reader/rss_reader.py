import logging
import json
import feedparser
from datetime import datetime, date
from time import mktime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DATE, func, TIME, desc, asc
from .news import News, engine, Base
from .json_formatter import Json
from contextlib import contextmanager


@contextmanager
def create_session(adding=None):
    Session = sessionmaker(bind=engine)
    s = Session()
    try:
        yield s
    finally:
        if adding:
            s.commit()
        s.close()


class RssReader(object):
    def __init__(self, source, limit, dates, json, configuration_for_conversion):
        self.source = source
        self.limit = limit
        self.dates = dates
        self.json = json
        self.configuration_for_conversion = configuration_for_conversion
        self.news_to_print = []
        Base.metadata.create_all(engine)

    def get_and_parse_news(self):
        logging.info('Getting news')
        news = feedparser.parse(self.source)
        logging.info('Parsing news')
        if news['entries'] and news['status'] == 200:
            with create_session('adding') as s:
                list_of_news = news['entries'][:self.limit[0]] if self.limit else news['entries']
                for feed in list_of_news:
                    text_of_the_feed = self.parse_html(feed['summary_detail']['value'])
                    title = self.parse_html(feed['title'])
                    if 'media_content' in feed.keys():
                        media_content = feed['media_content'][0]['url']
                    feed_object = News(news['feed']['title'],
                                    title,
                                    datetime.fromtimestamp(mktime(feed['published_parsed'])),
                                    feed['link'],
                                    text_of_the_feed,
                                    [image['url'] for image in feed['media_content']],
                                    datetime.today())
                    current_feed_in_table = s.query(News).filter(News.link==feed['link']).first()
                    if not current_feed_in_table:
                        s.add(feed_object)
                    else:
                        s.query(News)\
                            .filter(News.link==feed['link'])\
                            .update({'date_of_addition':datetime.today()}) 
        else:
            raise ConnectionError
        logging.info('All news are cached')
        
    def parse_html(self, html):
        from bs4 import BeautifulSoup
        parser = BeautifulSoup(html, 'html.parser')
        return parser.get_text()
    
    def get_cached_news(self):
        with create_session() as s:
            for date in self.dates:
                self.news_to_print.extend(s.query(News).filter(func.DATE(News.date) == date).all())
            if not self.news_to_print:
                raise Exception('No cached news on this date')
            self.print_news()        
            
    def get_news_to_print(self):
        with create_session() as s:
            if self.limit:
                self.news_to_print = s.query(News)\
                                      .filter(News.date_of_addition == datetime.today())\
                                      .order_by(News.date_of_addition.desc())\
                                      .limit(self.limit[0]).all()
            else:
                self.news_to_print = s.query(News)\
                                      .filter(func.DATE(News.date_of_addition) == datetime.today().date())\
                                      .order_by(News.date_of_addition.asc()).all()
        if self.json:
            print(Json(self.news_to_print))
        else:
            self.print_news()
            
    def print_news(self):
        for feed in self.news_to_print:
            print(feed)
            print('='*50)
    
    def __call__(self):
        if self.dates:
            self.get_cached_news()
        else:
            self.get_and_parse_news()
        self.get_news_to_print()
