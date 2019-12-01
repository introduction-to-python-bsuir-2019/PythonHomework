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
from colorama import init
from colorama import Fore

from app.rss_exception import RSSException


class RSSReader:
    """ Reads news from RSS url and prints them """

    def __init__(self, url, limit, date, logger, colorize=None):
        self.url = url
        self.limit = limit
        self.date = date
        self.logger = logger
        self.colorize = colorize
        init() # colorama

    def get_feed(self):
        """ Returns parsed feed and caches it"""

        news_feed = feedparser.parse(self.url)
        for entry in news_feed.entries[:self.limit]:
            self.cache_news_json(entry)
        self.logger.info('News has been cached')
        if not news_feed.entries:
            raise RSSException('Did not parse any news')
        return news_feed.entries[:self.limit]

    def print_feed(self, entries):
        """ Prints feed in stdout """

        self.logger.info('Printing feed')

        if self.colorize:
            for entry in entries:
                print(f'{Fore.GREEN}========================================================{Fore.RESET}')
                print(f'{Fore.GREEN}Title:{Fore.RESET} {entry.title}')
                print(f'{Fore.GREEN}Published:{Fore.RESET} {entry.published}')
                print(f'{Fore.GREEN}Summary:{Fore.RESET} {BeautifulSoup(entry.summary, "html.parser").text}')
                print(f'{Fore.GREEN}Image:{Fore.RESET} {self.get_img_url(entry.summary)}')
                print(f'{Fore.GREEN}Link:{Fore.RESET} {entry.link}')
                print(f'{Fore.GREEN}========================================================{Fore.RESET}')
        else:
            for entry in entries:
                print('========================================================')
                print(f'Title: {entry.title}')
                print(f'Published: {entry.published}', end='\n\n')
                print(f'Summary: {BeautifulSoup(entry.summary, "html.parser").text}', end='\n\n')
                print(f'Image: {self.get_img_url(entry.summary)}')
                print(f'Link: {entry.link}')
                print('========================================================')

    def get_img_url(self, summary):
        """ Parses image url from <description> in rss feed """
        soup = BeautifulSoup(summary, 'html.parser')
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
            if self.colorize:
                print(Fore.GREEN + json.dumps(feed, indent=2, ensure_ascii=False) + Fore.RESET, end=',\n')
            else:
                print(json.dumps(feed, indent=2, ensure_ascii=False), end=',\n')

    def to_dict(self, entry):
        """ Converts entry to dict() format """

        feed = dict()
        feed['Title'] = entry.title
        feed['Published'] = entry.published
        feed['Summary'] = BeautifulSoup(entry.summary, "html.parser").text
        feed['Link'] = entry.link
        feed['Url'] = self.url
        feed['Image'] = self.get_img_url(entry.summary)
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
            self.logger.info('Creating new .json file')
        except json.JSONDecodeError:
            self.logger.info('Empty JSON file')

        with open(file_path, 'w', encoding='utf-8') as wf:
            news.append(feed)
            json.dump(news, wf, indent=2)

    def get_cached_json_news(self):
        """ Returns the list of cached news with date from arguments """

        file_path = 'cache' + os.path.sep + self.date + '.json'
        cached_news = list()
        try:
            with open(file_path) as rf:
                news = json.load(rf)
                for new in news:
                    if new['Url'] == self.url:
                        cached_news.append(new)
                if not cached_news:
                    # News with such url have not been found
                    raise FileNotFoundError
                return cached_news[:self.limit]
        except FileNotFoundError:
            if self.colorize:
                print(f'{Fore.RED}There are no cached news with such date by this url{Fore.RESET}')
            else:
                print('There are no cached news with such date by this url')
        except json.JSONDecodeError:
            # Empty json file
            # Or no news by needed url
            if self.colorize:
                print(f'{Fore.RED}There are no cached news with such date by this url{Fore.RESET}')
            else:
                print('There are no cached news with such date by this url')
        return False

    def print_cached_feed(self, cached_feed):
        """ Prints saved news in stdout """

        self.logger.info('Printing cached feed')
        for new in cached_feed:
            if self.colorize:
                print(f'{Fore.GREEN}---------------------------------------------------------{Fore.RESET}')
                for key, value in new.items():
                    print(f'{Fore.GREEN}{key}:{Fore.RESET} {value}')
                print(f'{Fore.GREEN}---------------------------------------------------------{Fore.RESET}')
            else:
                print('---------------------------------------------------------')
                for key, value in new.items():
                    print(f'{key}: {value}')
                print('---------------------------------------------------------')

    def print_cached_feed_json(self, cached_feed):
        """ Prints saved news in stdout in JSON format """

        self.logger.info('Printing cached feed in JSON format')
        for new in cached_feed:
            if self.colorize:
                print(Fore.GREEN + json.dumps(new, indent=2) + Fore.RESET, end=',\n')
            else:
                print(json.dumps(new, indent=2), end=',\n')
