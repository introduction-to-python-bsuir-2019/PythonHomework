import logging
import json
import feedparser
from datetime import datetime, date
from time import mktime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import DATE, func
from .news import News, engine, Base
from .json_formatter import Json

class RssReader(object):
    def __init__(self, source, limit, date, json):
        self.source = source
        self.limit = limit
        self.date = date[0]
        self.json = json
        #self.news_to_print = []
        Base.metadata.create_all(engine)

    def get_and_parse_news(self):
        logging.info('Getting news')
        news = feedparser.parse(self.source)
        logging.info('Parsing news')
        session = self.create_session()
        if news['entries'] and news['status'] == 200:
            from bs4 import BeautifulSoup
            list_of_news = news['entries'][:self.limit[0]] if self.limit else news['entries']
            for feed in list_of_news:
                text_of_the_feed = feed['summary_detail']['value']
                if text_of_the_feed.startswith('<p>'):
                    parser = BeautifulSoup(text_of_the_feed, 'html.parser')
                    text_of_the_feed = parser.find('p').get_text()
                if 'media_content' in feed.keys():
                    media_content = feed['media_content'][0]['url']
                print(datetime.fromtimestamp(mktime(feed['published_parsed'])))
                feed_object = News(news['feed']['title'],
                                   feed['title'],
                                   datetime.fromtimestamp(mktime(feed['published_parsed'])),
                                   feed['link'],
                                   text_of_the_feed,
                                   feed['media_content'][0]['url'])

                #self.news_to_print.append(feed_object)
                if not session.query(News).filter(News.title==feed['title']).first():
                    session.add(feed_object)
        else:
            raise ConnectionError
        logging.info('All news are cached')
        session.commit()
        session.close()

    @classmethod
    def create_session(cls):
        Session = sessionmaker(bind=engine)
        return Session()

    def get_cached_news(self):
        session = self.create_session()
        date_for_find = datetime.strptime(self.date, '%Y%m%d').date()
        cached_news = session.query(News).filter(func.DATE(News.date)==date_for_find).all()
        session.close()
        for feed in cached_news:
            print(feed)
        
    def get_news(self):
        if self.date:
            self.get_cached_news()
        else:
            self.get_and_parse_news()
            
    def print_news(self):
        for feed in self.news_to_print:
            print(feed)
        
    def __str__(self):
        pass
