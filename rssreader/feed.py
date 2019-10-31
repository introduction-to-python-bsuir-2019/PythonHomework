"""Module keeps objects related to feed"""
import logging
import html
from typing import Dict, List
import json
import feedparser
from bs4 import BeautifulSoup
from rssreader.base import BaseClass
from rssreader.news import News
from datetime import date


class FeedEncoder(json.JSONEncoder):
    """Subclass of JSONEncoder to be used for an instance of Feed class transforming into JSON"""
    def default(self, obj) -> Dict:
        """Returns serializable object for Feed"""
        if isinstance(obj, Feed):
            return {'feed': obj.__dict__['title'], 'news': [nw.get_json_dict() for nw in obj.__dict__['news']]}
        return json.JSONEncoder.default(self, obj)


class Feed(BaseClass):
    """Class to work with feed data."""
    def __init__(self, url: str, limit: int):
        self.url = url
        self.limit = limit
        self.title = ''
        self.encoding = ''
        self.news = []
        logging.info(f'Initialize a feed ({self})')

    def get_json(self) -> str:
        """Return feed in json format"""
        return json.dumps(self, cls=FeedEncoder, indent=4, ensure_ascii=False).encode(self.encoding).decode()

    def get_text(self):
        """Return feed data in textual form"""
        delimiter = '{0}\n'.format('-' * 50)
        result = delimiter.join([n.get_text() for n in self.news])
        return f'Feed: {self.title}\n\n{result}'

    def print(self, to_json: bool) -> None:
        """"Prints the feed into stdout. If to_json is true, data are converted into JSON format."""
        logging.info(''.join(['Print the feed as ', 'json' if to_json else 'text']))
        if len(self.news) == 0:
            raise Exception('There is no news on this url!')

        print(self.get_json() if to_json else self.get_text())

    def add_news(self, title: str, published: str, published_dt: date, link: str, description: str, hrefs: List[Dict]):
        self.news.append(News(title, published, published_dt, link, description, hrefs))

    def request(self) -> None:
        """Request the feed from URL"""
        data = feedparser.parse(self.url)
        self._parse(data)

    def _parse(self, data: feedparser.FeedParserDict) -> None:
        """Parses the RSS URL to load feed"""
        logging.info('Parse provided url to obtain feed')

        if data.bozo == 1:
            logging.info('feedparser.bozo is set to 1. It means the feed is not well-formed XML.')
            raise Exception(f'RSS url processing error. Details are "{data.bozo_exception}"')

        self.encoding = data.encoding
        self.title = data.feed.title
        # create a list of news based on feed entries
        logging.info('Iterate over feed to process each news')
        for n in data.entries[:self.limit]:
            self.add_news(
                html.unescape(n.title), n.published, date(*n.published_parsed[:3]), n.link,
                html.unescape(BeautifulSoup(n.description, "html.parser").text),
                [{'type': d.type, 'href': d.href} for d in n.links if d.href != n.link]
            )
