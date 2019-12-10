import html
import json
import logging
from xml.etree import ElementTree
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from rss_reader.models import Article
from rss_reader.exceptions import ParsingError


class FeedParser:
    ''' Class for all parsing operations '''
    def __init__(self):
        self.logger = logging.getLogger("rss_reader.Parser")
        self.feed = dict()

    def parse(self, data: str) -> dict:
        ''' Parse given feed in xml format to Article objects
            and save to self.feed
        '''
        try:
            self.logger.info('Parsing xml to Articles')
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError:
            self.logger.error("Can't parse feed. Unsupported format.")
            raise ParsingError("Can't parse feed. Unsupported format.")

        channel = root.find('channel')
        self.feed['feed_name'] = html.unescape(channel.find('title').text)
        self.feed['feed_source'] = html.unescape(channel.find('link').text)

        self.feed['articles'] = []
        for article in channel.findall('item'):
            media = {'links': None, 'images': []}
            date = date_parser.parse(html.unescape(article.find('pubDate').text))
            title = html.unescape(article.find('title').text)

            if article.find('description').text:
                content_html = BeautifulSoup(article.find('description').text, 'html.parser')
                content = content_html.get_text()

                media['links'] = [link['href'] for link in content_html.find_all('a')]
                for image in content_html.find_all('img'):
                    if 'alt' in image.attrs:
                        description = image['alt']
                    else:
                        description = 'No description'
                    media['images'].append({'description': description, 'source_url': image['src']})

            link = article.find('link').text
            self.feed['articles'].append(Article(date, title, content, media, link))

        return self.feed

    def get_json_feed(self, limit: int) -> str:
        '''Reformat self.feed to JSON format and return it'''
        self.logger.info('Converting feed to JSON')
        try:
            json_feed = json.dumps({'feed_name': self.feed['feed_name'],
                                    'articles': [article.to_dict() for article in self.feed['articles'][:limit]]},
                                   indent=3, ensure_ascii=False)
        except Exception as e:
            self.logger.error("Can't convert feed to JSON.")
            raise ParsingError("Can't convert feed to JSON.")
        else:
            return json_feed
