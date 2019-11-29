import logging
import json
import feedparser
from datetime import datetime, date
from time import mktime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, desc, asc, Date 
from .news import News, engine, Base
from .json_formatter import Json
from contextlib import contextmanager
from .converter import HtmlConverter

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
    def __init__(self, source, limit, date, json, configuration_for_conversion, all):
        self.source = source
        self.limit = limit
        self.date = date
        self.json = json
        self.configuration_for_conversion = configuration_for_conversion
        self.all = all
        self.news_to_print = []
        Base.metadata.create_all(engine)

    def get_and_parse_news(self):
        logging.info('Getting news')
        news = feedparser.parse(self.source)
        logging.info('Parsing news')
        if news['entries'] and news['status'] == 200:
            with create_session('adding') as s:
                list_of_news = news['entries'][:self.limit] if self.limit else news['entries']
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
            self.news_to_print.extend(s.query(News).filter(func.date(News.date) == self.date).all())
            if not self.news_to_print:
                raise Exception('No cached news on this date')      
    
    def get_all_news(self):
        with create_session() as s:
            self.news_to_print = s.query(News).all()
            if not self.news_to_print:
                raise Exception('No cached news')
                   
    def get_news_to_print(self):
        with create_session() as s:
            if self.limit:
                self.news_to_print = s.query(News)\
                                      .filter(func.Date(News.date_of_addition) == datetime.today().date())\
                                      .order_by(News.date_of_addition.desc())\
                                      .limit(self.limit).all()
            else:
                self.news_to_print = s.query(News)\
                                      .filter(func.Date(News.date_of_addition) == datetime.today().date())\
                                      .order_by(News.date_of_addition.asc()).all()
            
    def print_news(self):
        if self.json:
            print(Json(self.news_to_print))
            return
        for feed in self.news_to_print:
            print(feed)
            print('='*77)
    
    def exec(self):
        #try:
            if self.date:
                self.get_cached_news()
            elif self.all:
                self.get_all_news()
            else:
                self.get_and_parse_news()
                self.get_news_to_print()
            self.print_news()
            HtmlConverter(self.news_to_print, '/home/zavxoz/Pictures').convert()
        #except Exception as e:
        #    print(e)
