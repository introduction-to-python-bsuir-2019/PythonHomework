"""
    Contains class RSSReader which receives arguments from cmd
    and allows to parse URL with RSS feed and print it in stdout
    in different formats
"""

import os
import json

import feedparser
from bs4 import BeautifulSoup
import dateutil.parser as dateparser


class RSSReader:
    """ Reads news from RSS url and prints them """

    def __init__(self, args, logger):
        self.args = args.get_args()
        self.logger = logger

    def get_feed(self):
        """ Returns parsed feed and caches it"""

        news_feed = feedparser.parse(self.args.url)
        for entry in news_feed.entries[:self.args.limit]:
            self.cache_news_json(entry)
        self.logger.info('News has been cached')
        return news_feed.entries[:self.args.limit]

    def print_feed(self, entries):
        """ Prints feed in stdout """

        self.logger.info('Printing feed')

        for entry in entries:
            print('========================================================')
            print(f'Title: {entry.title}')
            print(f'Published: {entry.published}', end='\n\n')
            print(f'Summary: {BeautifulSoup(entry.summary, "html.parser").text}', end='\n\n')
            print(f'Image: {self.get_img_url(entry)}')
            print(f'Link: {entry.link}')
            print('========================================================')

    def get_img_url(self, entry):
        """ Parses image url from <description> in rss feed """
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img:
            img_url = img['src']
            return img_url
        else:
            return None

    def print_feed_json(self, entries):
        """ Prints feed in stdout in JSON format """

        self.logger.info('Printing feed in JSON format')

        for entry in entries:
            feed = self.to_dict(entry)
            print(json.dumps(feed, indent=2, ensure_ascii=False), ',', sep='')

    def to_dict(self, entry):
        """ Converts entry to dict() format """

        feed = dict()
        feed['Title'] = entry.title
        feed['Published'] = entry.published
        feed['Summary'] = BeautifulSoup(entry.summary, "html.parser").text
        feed['Link'] = entry.link
        feed['Url'] = self.args.url
        feed['Image'] = self.get_img_url(entry)
        return feed

    def cache_news_json(self, entry):
        """ Saves all printed news in JSON format (path = 'cache/{publication_date}.json')"""

        date = dateparser.parse(entry.published, fuzzy=True).strftime('%Y%m%d')
        directory_path = 'cache' + os.path.sep
        if not os.path.exists(directory_path):
            self.logger.info('Creating directory cache')
            os.mkdir(directory_path)

        file_path = directory_path + date + '.json'

        feed = self.to_dict(entry)
        news = list()
        try:
            with open(file_path, encoding='utf-8') as rf:
                news = json.load(rf)
                if feed in news:
                    # already cached
                    return
        except FileNotFoundError:
            self.logger.info('File not found')
        except json.JSONDecodeError:
            self.logger.info('Empty JSON file')

        with open(file_path, 'w', encoding='utf-8') as wf:
            news.append(feed)
            json.dump(news, wf, indent=2)

    def get_cached_json_news(self):
        """ Returns the list of cached news with date from arguments """

        file_path = 'cache' + os.path.sep + self.args.date + '.json'
        cached_news = list()
        try:
            with open(file_path) as rf:
                news = json.load(rf)
                for new in news:
                    if new['Url'] == self.args.url:
                        cached_news.append(new)
                if not cached_news:
                    # News with such url have not been found
                    raise FileNotFoundError
                return cached_news[:self.args.limit]
        except FileNotFoundError:
            print('There are no cached news with such date by this url')
        except json.JSONDecodeError:
            # Empty json file
            # Or no news by needed url
            print('There are no cached news with such date by this url')
        return False

    def print_cached_feed(self, cached_feed):
        """ Prints saved news in stdout """

        self.logger.info('Printing cached feed')
        for new in cached_feed:
            print('---------------------------------------------------------')
            for key, value in new.items():
                print(f'{key}: {value}')
            print('---------------------------------------------------------')

    def print_cached_feed_json(self, cached_feed):
        """ Prints saved news in stdout in JSON format """

        self.logger.info('Printing cached feed in JSON format')
        for new in cached_feed:
            print(json.dumps(new, indent=2), ',', sep='')
