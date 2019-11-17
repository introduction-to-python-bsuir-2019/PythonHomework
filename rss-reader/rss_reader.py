import logging as log
import json
import feedparser
from validator_collection.checkers import is_url


class RssReader:
    def __init__(self, source):
        pass
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RssReader, cls).__new__(cls)
        return cls.instance

    def validation(self):
        try:         
            if is_url(url):
                return url
            else:
                raise Exception("Invalid url")
        except Exception as e:
            print(e)
            log.error(e)
            

    def get_news(source, limit=None):
        a = feedparser.parse(validation(source))
        if a['entries'] and a['status'] == 200:
            print("Feed: ", a['feed']['title'],"\n")
            from bs4 import BeautifulSoup
            list_of_news = a['entries'][:args.limit[0]] if limit else a['entries']
            for news in list_of_news:    
                print('Title: ', news['title'])
                print('Date: ', news['published'])
                print('Link: ', news['link'],  "\n")
                feed = news['summary_detail']['value']
                if feed.startswith('<p>'):
                    parser = BeautifulSoup(feed,'html.parser')
                    print("[image: ", parser.find('img')['alt'], "][2]", parser.find('p').get_text(), "\n")
                    print()
                else:
                    print(feed, "\n")
                print('Links: ')
                print("[1]  ", news['link'], '(link)')

                if 'media_content' in news.keys():
                    print("[2]  ", news['media_content'][0]['url'], '(image)')
                print("="*90)   

    

    def init_logging():
        log.basicConfig(format='%(asctime)s %(module)s %(message)s', datefmt='%I:%M:%S', level=log.INFO)
    

