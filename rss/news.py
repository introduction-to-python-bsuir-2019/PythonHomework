"""Module contains class related to news"""

import json
import logging
import sys

import feedparser
from bs4 import BeautifulSoup


class RssReader():
    """This class parse, process and output news."""

    def __init__(self, url: str, limit=None):
        logging.info('Initialization')

        self.url = url
        self.feeds = feedparser.parse(url)
        self._check_url()

        self.feed_title = self.feeds.feed.get('title')
        self.list_of_news = []
        self.limit = limit

        self._check_limit()
        self.make_list_of_news()

    def _check_url(self):
        """Check if the url is valid."""

        logging.info('Check URL')
        if self.feeds['bozo'] or self.feeds.status != 200:
            logging.error('Something wrong with URL or Internet connection')
            sys.exit(1)

    def _check_limit(self):
        """Check if the limit >= 0."""

        logging.info('Check limit')
        if self.limit is not None and self.limit < 0:
            logging.error('Limit < 0')
            sys.exit(1)

    def print_news(self):
        """Print news in human-readable format."""

        logging.info('Print news')

        print('Feed:', self.feed_title, "\n\n")

        news_number = 1
        for news in self.list_of_news:
            print('№', news_number)
            news_number += 1
            print('Title:', news['title'])
            print('Date:', news['date'])
            print('Link:', news['link'], '\n')

            if news['description']['text']:
                print(news['description']['text'], '\n')

            if news['description']['images']:
                print('Images:')
                for item in news['description']['images']:
                    print(item)

            if news['description']['links']:
                print('Links:')
                for item in news['description']['links']:
                    print(item)

            print('-' * 50)

    def _find_date_tag(self, news: dict) -> str:
        """
        Find date tag and return its value,
        or return 'Unknown' if tag not found.
        """

        logging.info('Find date tag')

        if news.get('published'):
            return news['published']
        elif news.get('pubDate'):
            return news['pubDate']
        elif news.get('Date:'):
            return news['Date']
        else:
            return 'Unknown'

    def make_list_of_news(self):
        """Make a list of news.

        type of news: dict
         """

        logging.info('Make a list of news')

        if self.limit is None or self.limit > len(self.feeds):
            self.limit = len(self.feeds)


        for news in self.feeds['entries'][:self.limit]:
            one_news = {}

            if news.get('title'):
                one_news['title'] = news['title']
            else:
                one_news['title'] = 'Unknown'

            if news.get('link'):
                one_news['link'] = news['link']
            else:
                one_news['link'] = 'Unknown'

            one_news['date'] = self._find_date_tag(news)
            one_news.update(self._read_description(news))
            self.list_of_news.append(one_news)

    def _read_description(self, news: dict) -> dict:
        """Return dict with keys 'text', 'images', 'links'.

        'text' value is description(str)
        'images' value is a list of images sources
        'links' value is a list of urls
        """

        logging.info('Get information from description')
        soup = BeautifulSoup(news.description, features="html.parser")

        logging.info('Get text of description')
        text = soup.text
        text.replace('&#39;', "'")
        if not text:
            text = 'Nothing'

        logging.info('Get list of images')
        list_of_images = []
        images = soup.findAll('img')
        for image in images:
            if image.get('src'):
                list_of_images.append(image['src'])

        if not list_of_images:
            list_of_images = None

        logging.info('Get list of links')
        list_of_links = []
        for tag in soup.findAll():
            if tag.get('href'):
                list_of_links.append(tag['href'])
            if tag.get('url'):
                list_of_links.append(tag['url'])

        if not list_of_links:
            list_of_links = None

        return {'description': {'text': text, 'images': list_of_images,
                'links': list_of_links}}

    def convert_to_json(self):
        """Return news in JSON format."""

        logging.info('Convert news into JSON format')
        try:
            result = json.dumps({'news': {'feed': self.feed_title, 'items': self.list_of_news}},
                                indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error("Can't convert to JSON:", e)

        return result
