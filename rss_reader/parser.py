from xml.etree import ElementTree
import html
import json
from bs4 import BeautifulSoup

from storage import Article


class Parser:
    ''' Class for all parsing operations '''
    def __init__(self):
        self.feed = dict()

    def parse(self, data):
        ''' Parse given data in xml format to Article objects
            and save to self.feed
        '''
        root = ElementTree.fromstring(data)
        channel = root.find('channel')
        self.feed['feed_name'] = channel.find('title').text
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
            content += (html.unescape(content_html.text))

            link = article.find('link').text
            self.feed['articles'].append(Article(date, title, content, media, link))

        return self.feed

    def get_json_feed(self, limit):
        '''Reformat self.feed to JSON format and return it'''
        return json.dumps({'feed_name': self.feed['feed_name'],
                           'articles': [article.to_dict() for article in self.feed['articles'][:limit]]}, indent=3)
