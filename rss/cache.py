"""This module provides work with cashed news."""

import logging
import shelve
import datetime
import sys
import json

import dateparser

from rss.converter_to_fb2 import Fb2Converter
from rss.converter_to_html import HTMLConverter


class Cache:
    """This class creates cache file, updates it and prints cached news."""

    def __init__(self):
        logging.info("Cache initialization")
        self.db_file_name = 'cache.db'

    def _create_key(self, date: str, url: str) -> str:
        """Create key for db."""

        logging.info('Create key')
        return date + url

    def _convert_date(self, date: str) -> str:
        """Convert date to %Y%m%d format."""

        logging.info('Convert date')

        converted_date = dateparser.parse(date)
        if not converted_date:
            logging.info("Date isn't clear. Try to parse again")
            try:
                converted_date = datetime.datetime.strptime(date, "%a, %d %b %Y %X %z")
                return converted_date.strftime('%Y%m%d')
            except Exception:
                raise Exception('Something wrong with date')
        return converted_date.strftime('%Y%m%d')

    def insert_news(self, news, row_description, url: str):
        """Insert news into cache file.
           Create cache file if it doesn't exist.
        """

        date = news['date']
        key = self._create_key(self._convert_date(date), url)
        logging.info("Open db or create if it doesn't exist for inserting news")
        with shelve.open(self.db_file_name) as db:
            if db.get(key):
                logging.info("Update record")
                record = db[key]
                if not list(record['list_of_news']).count(news):
                    record['list_of_news'].append(news)
                    record['list_of_row_descriptions'].append(row_description)
                db[key] = record
            else:
                logging.info("Create new record")
                record = {}
                record['list_of_news'] = []
                record['list_of_news'].append(news)
                record['list_of_row_descriptions'] = []
                record['list_of_row_descriptions'].append(row_description)
                db[key] = record

    def _check_entered_date(self, key: str):
        """Check length and characters in entered string"""

        logging.info('Check entered date')
        if len(key) != 8 or not key.isdigit():
            raise ValueError('Invalid entered date')

    def _get_news(self, key: str) -> list:
        """Get news from db by key"""

        logging.info("Open db or create if it doesn't exist for getting news")
        with shelve.open(self.db_file_name) as db:
            try:
                record = db[key]
                return record
            except KeyError:
                raise Exception("Can't find the news")

    def set_printing_news(self, url: str, date: str,
                          limit: int, json_mode: bool,
                          fb2_path: str, html_path: str):
        """Set print format"""

        logging.info("Set print format")

        self._check_entered_date(date)
        self._check_limit(limit)

        key = self._create_key(date, url)
        db = self._get_news(key)

        if json_mode:
            print(json.dumps(db['list_of_news'][:limit], indent=4, ensure_ascii=False))
        else:
            self.print_news(db['list_of_news'], limit)

        if fb2_path:
            conv = Fb2Converter(fb2_path)
            conv.convert_to_fb2(db['list_of_news'][:limit])
            conv.save_fb2()
        if html_path:
            conv = HTMLConverter(html_path)
            conv.save_html(conv.convert_to_html(db['list_of_news'][:limit],
                                                db['list_of_row_descriptions'][:limit]))

    def _check_limit(self, limit):
        """Check if the limit > 0."""

        logging.info('Check limit')
        if limit is not None and limit <= 0:
            raise ValueError('Invalid limit: limit <= 0')

    def print_news(self, list_of_news, limit):
        """Print news."""

        logging.info('Start printing cached news')
        news_number = 1
        # check if self.list_of_news consists of 1 element
        if type(list_of_news) == dict:
            print('№', news_number)
            self._print_entries(list_of_news)
        else:
            for news in list_of_news[:limit]:
                print('№', news_number)
                news_number += 1
                self._print_entries(news)

    def _print_entries(self, news: dict):
        """Print one news."""

        logging.info('Print one news')
        print('Title:', news['title'])
        print('Date:', news['date'])
        print('Link:', news['link'], '\n')

        if news['description']['text'] != 'Nothing':
            print(news['description']['text'], '\n')

        if news['description']['images']:
            print('Images:')
            for item in news['description']['images']:
                print(item['src'])

        if news['description']['links']:
            print('Links:')
            for item in news['description']['links']:
                print(item)

        print('-' * 50)
