import argparse
import html
import json
import feedparser
import requests
from bs4 import BeautifulSoup as bs4
import time
import logging
from json2html import *
import re
import sys


class NewsReader():
    '''CLass for RSS parsing  '''
    def __init__(self, url, limit=None):
        self.title = None
        self.entries = None
        self.url = url
        self.description = None
        self.limit = limit

    def check_internet(self):
        url = 'http://www.google.com/'
        timeout = 5

        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            logging.info("No internet connection")
        return False

    def parse_rss(self):
        '''Parses RSS feed and returns list of dict with 'News' objects'''
        logging.info('RSS parsing...')
        if not self.check_internet():
            print('No internet connection, rss feed is unavaluable')

        self.rss = feedparser.parse(self.url)

        if self.rss.bozo == 1:
            logging.info('feedparser.bozo is set to 1. It means the feed is not well-formed XML.')
            raise Exception(f'RSS url processing error. Details are "{rss.bozo_exception}"')

        self.entries = []
        logging.info('Working with entry...')
        for entry in self.rss.entries:
            soup = bs4(entry['description'], 'lxml')
            links = ''

            for link in soup.findAll('a'):
                links += f"{link.get('href')}\n\t"
            if links == '':
                links = 'There is no provided links'
            try:
                image = soup.find('a').find('img').get('src')
            except AttributeError:
                image = 'No image'
            nice_desk = ' '.join(soup.text.split())

            self.entries.append({'title': entry.title,
                                 'feed': self.rss.feed.title,
                                 'date': time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed),
                                 'simple_date': int(time.strftime('%Y%m%d', entry.published_parsed)),
                                 'link': entry.link,
                                 'description': nice_desk,
                                 'image': image,
                                 'links': links
                                 })
        return self.entries

    def desc_of_resourse(self):
        '''Tuple container for resourse determining'''
        logging.info('Add resourse description')
        self.rss = feedparser.parse(self.url)
        try:
            image = self.rss.feed.image.url
        except AttributeError:
            image = 'No image'
        title = self.rss.feed.title
        link = self.rss.feed.link
        return title, link, image

    def make_json(self):
        '''Create json output with help of json.dumps and list of entries '''
        logging.info('Make readable json format...')
        try:
            self.parse_rss()
        except NameError:
            return 'Connection to rss feed failed'
        emp_list = []
        for feed in self.entries[0:self.limit]:
            emp_list.append((json.dumps({
                "item": {
                    "link": feed['link'],
                    "body": {
                         "title": feed['title'],
                         "date": feed['date'],
                         "links": feed['links'],
                         "image": feed['image'],
                         "description": feed['description']
                    }
                }
            }, indent=4, ensure_ascii=False)))
        return emp_list

    def json_for_html(self):
        '''Add special tags for nice html creating '''
        try:
            self.parse_rss()
        except NameError:
            return 'Connection to rss feed failed'

        logging.info('Сreating json for html converting format...')
        emp_list = []

        for feed in self.entries[0:self.limit]:
            emp_list.append((json.dumps({
                                         "item": {
                                            "link": f"<a href={feed['link']}>Go to sourse</a> ",
                                            "body": {
                                                 "title": feed['title'],
                                                 "date": feed['date'],
                                                 "links": feed['links'],
                                                 "image": f"<img src={feed['image']}>",
                                                 "description": feed['description']
                                            }
                                         }
                                    }, indent=4, ensure_ascii=False)))
        return emp_list

    def json_html(self, filepath):
        '''Creating html with help of json2html module and regular expressions'''
        symbol_one = '&lt;'
        symbol_two = '&gt;'
        string_list = []

        for item in self.json_for_html():
            raw_html = json2html.convert(item)
            raw_html = raw_html.replace(symbol_one, '<')
            string_list.append(raw_html.replace(symbol_two, '>'))
            rss_to_html = filepath + '.html'

            with open(rss_to_html, 'w') as wf:
                for item in string_list:
                    wf.write(item)

    def print_rss(self):
        '''Take elements from list with feed entries and outputs it'''
        logging.info('Show rss in readable format...')
        try:
            self.parse_rss()
        except NameError:
            logging.info('There might be troubles with internet connection')
        try:
            for entry in self.entries[0:self.limit]:
                print(f"Feed : ({entry['feed']})")
                print(f"Title : {entry['title']}\n")

                try:
                    print(f"Date: {entry['date']}\n")
                except IndexError:
                    print('Date: Date has not been provided')

                print(f"{entry['link']}\n")
                print(f"Description: {entry['description']}\n")
                print(f"Provided links:\n\t{entry['links']}\nProvided image: {entry['image']}")
                # Delimiter
                print('-'*80)
        except TypeError:
            print('Connection to rss feed failed')
