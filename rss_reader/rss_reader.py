import logging
import json
import feedparser
from datetime import datetime as dt
from time import mktime
from sqlalchemy.orm import sessionmaker
from .news import News, engine, Base


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
            from bs4 import BeautifulSoup
            list_of_news = news['entries'][:self.limit[0]] if self.limit else news['entries']
            for feed in list_of_news:
                text_of_the_feed = feed['summary_detail']['value']
                if text_of_the_feed.startswith('<p>'):
                    parser = BeautifulSoup(text_of_the_feed, 'html.parser')
                    text_of_the_feed = parser.find('p').get_text()
                if 'media_content' in feed.keys():
                    media_content = feed['media_content'][0]['url']
                feed_object = News(news['feed']['title'],
                                   feed['title'],
                                   dt.fromtimestamp(mktime(feed['published_parsed'])),
                                   feed['link'],
                                   text_of_the_feed,
                                   feed['media_content'][0]['url'])
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

    def __repr__(self):
        pass
