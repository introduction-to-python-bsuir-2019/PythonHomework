import feedparser
import json
from bs4 import BeautifulSoup
# https://news.yahoo.com/rss/


class RSSReader:
    def __init__(self, source, limit=1, json=False):
        self.source = source
        self.limit = limit
        self.json = json
        self.feeds = {}

    def parse_source(self):
        d = feedparser.parse(self.source)

        self.feeds['feed_name'] = d['channel']['title']
        self.feeds['news'] = []

        for news in d['entries'][0:self.limit]:
            self.feeds['news'].append(self.read_news(news))

        self.print_feeds()
        self.cache()

    @staticmethod
    def read_news(news):
        item = dict()

        item['title'] = news['title'].replace('&#39;', "'")
        item['date'] = news['published']
        item['link'] = news['link']

        soup = BeautifulSoup(news['summary'], 'html.parser')

        item['image_title'] = soup.find('img')['title']
        description = soup.p.contents[-2]
        if str(description)[0] == '<':
            item['image_description'] = 'No image description'
        else:
            item['image_description'] = description
        if soup.find('img')['src'] == "":
            item['image_link'] = 'No image link'
        else:
            item['image_link'] = soup.find('img')['src']

        return item

    def cache(self):
        with open('cache.json', 'r') as f:
            feeds_f = json.load(f)
            for item in self.feeds['news']:
                if item not in feeds_f['news']:
                    feeds_f['news'].append(item)

        if feeds_f['news'][0].get('title') == '':
            del feeds_f['news'][0]
        feeds_f['feed_name'] = self.feeds['feed_name']

        with open('cache.json', 'w') as f:
            json.dump(feeds_f, f, indent=1)

    def print_feeds(self):
        if not self.json:
            print()
            print('Feed:', self.feeds['feed_name'])
            print('-' * 40)
            for item in self.feeds['news']:
                print('Title:', item['title'])
                print('Date:', item['date'])
                print('Link:', item['link'])
                print()
                print('Image title:', item['image_title'])
                print('Image description:', item['image_description'])
                print('Image link:', item['image_link'])
                print('-' * 40)
        else:
            print(json.dumps(self.feeds, indent=1))
