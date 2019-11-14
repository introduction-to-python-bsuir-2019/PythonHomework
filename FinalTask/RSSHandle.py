from bs4 import BeautifulSoup
import feedparser
import logging
import json


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class RssHandler:

    def __init__(self, rss: str):
        self.rss = rss
        self.feed = None
        self.feed_dict = {}
        self.json_feed = None

        self.url_handler()
        self.rss_dict()

    def url_handler(self):
        """Takes URL and return rss object"""
        self.feed = feedparser.parse(self.rss)
        logging.info("RSS-Feed was parsed.")

    def rss_dict(self):
        """Make dictionary from RSS-Feed"""
        self.feed_dict['source'] = self.feed['feed']['title']
        self.feed_dict['news'] = []

        for descr in self.feed['entries']:
            soup = BeautifulSoup(descr['summary'], 'lxml')
            links = set(link.get('href') for link in soup.find_all('a'))
            media = set(pic.get('src') for pic in soup.find_all('img'))
            self.feed_dict['news'].append({'title': descr['title'], 'pubDate': descr['published'],
                                          'text': soup.get_text(), 'links': links,
                                           'media': media, 'src_link': descr['link']})

        logging.info('Created dictionary from parsed RSS-Feed.')

    def to_json(self, limit):
        """Make JSON file from RSS"""
        json_dict = self.feed_dict.copy()
        json_dict['news']
        if limit is not None:
            del(json_dict['news'][limit:])
        self.json_feed = json.dumps(json_dict, cls=SetEncoder)
        logging.info('Created JSON object from dictionary.')

    def output(self, json_param, limit):
        """Outputs information in stdout"""
        logging.info('Printing RSS-Feed in stdout.')
        if not json_param:
            print(f"\nFeed: {self.feed_dict['source']}")
            for elem in self.feed_dict['news']:
                if self.feed_dict['news'].index(elem) == limit:
                    break
                print(f"""
Title: {elem['title']}
Published: {elem['pubDate']}
Source link: {elem['src_link']}

{elem['text']}

                      """)

                print('Links:')
                for (count, link) in enumerate(elem['links'].union(elem['media'])):
                    print(f'[{count + 1}]{link}')
                print('-'*80)
        else:
            logging.info('Printing JSON object created from RSS-Feed in stdout.')
            self.to_json(limit)
            print(self.json_feed)
