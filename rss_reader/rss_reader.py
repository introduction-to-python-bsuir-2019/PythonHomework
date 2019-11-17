import logging
import json
import feedparser
from sqlalchemy.orm import sessionmaker
from .news import News, engine, Base

class RssReader(object):
    def __init__(self, source, limit, date, json):
        self.source = source
        self.limit = limit
        self.date = date
        self.json = json
        Base.metadata.create_all(engine)  
        

    
    '''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RssReader, cls).__new__(cls)
        return cls.instance
          '''  

    def get_and_parse_news(self):
        logging.info('Getting news')
        a = feedparser.parse(self.source)
        logging.info('Parsing news')
        Session = sessionmaker(bind=engine)
        session = Session()
        if a['entries'] and a['status'] == 200:
            print("Feed: ", a['feed']['title'],"\n")
            from bs4 import BeautifulSoup
            list_of_news = a['entries'][:self.limit[0]] if self.limit else a['entries']
            for news in list_of_news: 
                
                
                print('Title: ', news['title'])
                print('Date: ', news['published'])
                print('Link: ', news['link'],  "\n")
                feed = news['summary_detail']['value']
                if feed.startswith('<p>'):
                    parser = BeautifulSoup(feed,'html.parser')
                    print("[image: ", parser.find('img')['alt'], "][2]", parser.find('p').get_text(), "\n")
                    print()
                    aaa = News(a['feed']['title'], 
                            news['title'], 
                            #news['published_parsed'], 
                            news['link'], 
                            parser.find('p').get_text(), 
                            news['media_content'][0]['url'])
                    session.add(aaa)
                else:
                    print(feed, "\n")
                print('Links: ')
                print("[1]  ", news['link'], '(link)')

                if 'media_content' in news.keys():
                    print("[2]  ", news['media_content'][0]['url'], '(image)')
                print("="*90)   
        session.commit()
        session.close()
