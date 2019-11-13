import html
import json
import logging
from xml.etree import ElementTree

from bs4 import BeautifulSoup

from storage import Article
from exceptions import ParsingError


class FeedParser:
    ''' Class for all parsing operations '''
    def __init__(self):
        self.logger = logging.getLogger("rss_reader.Parser")
        self.feed = dict()

    def parse(self, data: str) -> dict:
        ''' Parse given data in xml format to Article objects
            and save to self.feed
        '''
        try:
            self.logger.info('Parsing xml to Articles')
            root = ElementTree.fromstring(data)
        except ElementTree.ParseError:
            self.logger.error("Can't parse feed. Unsupported format.")
            raise ParsingError("Can't parse feed. Unsupported format.")

        channel = root.find('channel')
        self.feed['feed_name'] = channel.find('title').text

        if channel.find('lastBuildDate') is not None:
            self.feed['feed_date'] = channel.find('lastBuildDate').text
        elif channel.find('pubDate') is not None:
            self.feed['feed_date'] = channel.find('pubDate').text 

        self.feed['articles'] = []
        for article in channel.findall('item'):
            media = {'links': None, 'images': []}
            content = ''
            date = html.unescape(article.find('pubDate').text)
            title = html.unescape(article.find('title').text)

            content_html = BeautifulSoup(article.find('description').text, 'html.parser')
            media['links'] = [link['href'] for link in content_html.find_all('a')]
            for image in content_html.find_all('img'):
                media['images'].append({'description': image['alt'], 'source_url': image['src']})

            for number, image in enumerate(media['images']):
                content += f'[image {number+1}: {image["description"]}][{number+1}] '
            content += html.unescape(content_html.text)

            link = article.find('link').text
            self.feed['articles'].append(Article(date, title, content, media, link))

        return self.feed

    def get_json_feed(self, limit: int) -> str:
        '''Reformat self.feed to JSON format and return it'''
        self.logger.info('Converting feed to JSON')
        try:
            json_feed = json.dumps({'feed_name': self.feed['feed_name'],
                                    'feed_date': self.feed['feed_date'],
                                    'articles': [article.to_dict() for article in self.feed['articles'][:limit]]},
                                   indent=3, ensure_ascii=False)
        except Exception as e:
            self.logger.error("Can't convert feed to JSON.")
            raise ParsingError("Can't convert feed to JSON.")
        else:
            return json_feed
