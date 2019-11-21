import argparse
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


def print_to_console(channel_title, feeds):
    print()
    print('Feed:', channel_title)
    print('-' * 40)
    for item in feeds:
        print('Title:', item['title'])
        print('Date:', item['date'])
        print('Link:', item['link'])
        print()
        print('Image title:', item['image_title'])
        print('Image description:', item['image_description'])
        print('Image link:', item['image_link'])
        print('-' * 40)


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()

    reader = RSSReader(**vars(args))
    channel_title, feeds = reader.parse_source()
    print_to_console(channel_title, feeds)


if __name__ == '__main__':
    main()
