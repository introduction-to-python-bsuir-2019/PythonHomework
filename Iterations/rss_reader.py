import feedparser
from bs4 import BeautifulSoup
# https://news.yahoo.com/rss/


class RSSReader:
    def __init__(self, source, limit):
        self.source = source
        self.limit = limit
        self.feeds = []

    def parse_source(self):
        d = feedparser.parse(self.source)

        channel_title = d['channel']['title']

        for news in d['entries'][0:self.limit]:
            self.feeds.append(self.read_news(news))

        return channel_title, self.feeds

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
