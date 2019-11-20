"""Module keeps objects related to feed"""
import logging
import html
import json
from typing import Dict, List, Callable
from datetime import datetime, date
from pathlib import Path
import mimetypes

import feedparser
from bs4 import BeautifulSoup

from rssreader.base import BaseClass
from rssreader.news import News
from rssreader.cache import Cache


class FeedEncoder(json.JSONEncoder):
    """Subclass of JSONEncoder to be used for an instance of Feed class transforming into JSON"""
    def default(self, obj: object) -> Dict:
        """Returns serializable object for Feed"""
        if isinstance(obj, Feed):
            return {'feed': obj.__dict__['title'],
                    'news': [nw.get_json_dict() for nw in obj.__dict__['news'][:obj.__dict__['limit']]]}
        return json.JSONEncoder.default(self, obj)


class Feed(BaseClass):
    """Class to work with feed data."""
    def __init__(self, url: str, limit: int, published_from: date = None) -> None:
        self.url = url
        self.limit = limit
        self.title = ''
        self.encoding = ''
        self.news = []
        self.published_from = published_from
        logging.info(f'Initialize a feed ({self})')

    def get_json(self) -> str:
        """Return feed in json format"""
        return json.dumps(self, cls=FeedEncoder, indent=4, ensure_ascii=False).encode(self.encoding).decode()

    def get_text(self, paint: Callable[[str, str], str]) -> str:
        """Return feed data in textual form"""
        delimiter = paint('{0}\n'.format('-' * 50), 'cyan')
        result = delimiter.join([n.get_text(paint) for n in self.news[:self.limit]])
        return f'{paint("Feed:", "green")} {self.title}\n\n{result}'

    def print(self, to_json: bool, paint: Callable[[str, str], str]) -> None:
        """"Prints the feed into stdout. If to_json is true, data are converted into JSON format."""
        logging.info(''.join(['Print the feed as ', 'json' if to_json else 'text']))
        print(self.get_json() if to_json else self.get_text(paint))

    def add_news(self, title: str, published: str, published_dt: datetime, link: str, description: str,
                 hrefs: List[Dict]) -> None:
        """Add a news into feed"""
        self.news.append(News(title, published, published_dt, link, description, hrefs))

    def request(self, storage: Path) -> None:
        """Request RSS data from URL"""
        data = feedparser.parse(self.url)
        self._parse(data)
        self.cache(storage)

    @staticmethod
    def _extract_links(description: BeautifulSoup) -> List[Dict]:
        """Manually parse description to obtain links"""
        lst = []
        # add hrefs
        for a in description.find_all('a'):
            try:
                url = a['href']
                if url:
                    # if mime-type can be determined, base type "text" is used
                    lst.append({'type': mimetypes.guess_type(url)[0] or 'text', 'href': url})
                else:
                    logging.info('Attribute "href" is empty - the item is skipped')
            except KeyError:
                logging.info('Tag "a" does not have an attribute "href" - the item is skipped')

        # add images
        for img in description.find_all('img'):
            try:
                url = img['src']
                if url:
                    # if mime-type can be determined, base type "image" is used
                    lst.append({'type': mimetypes.guess_type(url)[0] or 'image', 'href': url})
                else:
                    logging.info('Attribute "src" is empty - the item is skipped')
            except KeyError:
                logging.info('Tag "img" does not have an attribute "src" - the item is skipped')
        return lst

    def _parse(self, data: feedparser.FeedParserDict) -> None:
        """Parses the RSS data to load feed"""
        logging.info('Parse provided url to obtain feed')

        if data.bozo == 1:
            logging.info('feedparser.bozo is set to 1. It means the feed is not well-formed XML.')
            raise Exception(f'RSS url processing error. Details are "{data.bozo_exception}"')

        self.encoding = data.encoding
        self.title = data.feed.title
        # Create a list of news based on feed entries. All news are processed to be stored in local cache later.
        logging.info('Iterate over feed to process each news')
        for n in data.entries:
            parsed_description = BeautifulSoup(n.description, "html.parser")
            self.add_news(
                html.unescape(n.title), n.published, datetime(*n.published_parsed[:6]), n.link,
                html.unescape(parsed_description.text), self._extract_links(parsed_description)
            )

    def load_from_cache(self, storage: Path) -> None:
        """Load cached news"""
        Cache(cache_dir=storage).load(self)

    def cache(self, storage: Path) -> None:
        """Cache news"""
        Cache(cache_dir=storage).add(self)
