import logging
import json
import feedparser
from datetime import datetime, date
from time import mktime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DATE, func, TIME, desc, asc
from .news import News, engine, Base
from .json_formatter import Json

class RssReader(object):
    def __init__(self, source, limit, date, json):
        self.source = source
        self.limit = limit
        self.date = date
        self.json = json
        Base.metadata.create_all(engine)

    def get_and_parse_news(self):
        logging.info('Getting news')
        news = feedparser.parse(self.source)
        logging.info('Parsing news')
        session = self.create_session()
        if news['entries'] and news['status'] == 200:
            
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
                current_feed_in_table = session.query(News).filter(News.link==feed['link']).first()
                if not current_feed_in_table:
                    session.add(feed_object)
                else:
                    session.query(News)\
                           .filter(News.link==feed['link'])\
                           .update({'date_of_addition':datetime.today()}) 
                    session.commit()  
        else:
            raise ConnectionError
        logging.info('All news are cached')
        session.commit()
        session.close()

    @classmethod
    def create_session(cls):
        Session = sessionmaker(bind=engine)
        return Session()

    def parse_html(self, html):
        from bs4 import BeautifulSoup
        parser = BeautifulSoup(html, 'html.parser')
        return parser.get_text()
    
    def get_cached_news(self):
        session = self.create_session()
        date_for_find = [datetime.strptime(date_of_feed, '%Y%m%d').date() for date_of_feed in self.date]
        cached_news = session.query(News).filter(func.DATE(News.date) == date_for_find[0]).all()
        session.close()
        for feed in cached_news:
            print(feed)
        
    def get_news(self):
        if self.date:
            self.get_cached_news()
        else:
            self.get_and_parse_news()
            
    def print_news(self):
        if self.json:
            print(Json())
        else:
            session = self.create_session()
            if self.limit:
                news_to_print = session.query(News)\
                                        .filter(News.date_of_addition == datetime.today())\
                                        .order_by(News.date_of_addition.desc())\
                                        .limit(self.limit[0]).all()
            else:
                news_to_print = session.query(News)\
                                        .filter(func.DATE(News.date_of_addition) == datetime.today().date())\
                                        .order_by(News.date_of_addition.asc()).all()
            session.close()
            for feed in news_to_print:
                print(feed)
   
    def __str__(self):
        pass
