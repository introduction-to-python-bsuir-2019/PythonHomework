"""RSS-reader module"""

import re
import logging
import feedparser

from tldextract import extract

from news_cacher import NewsCacher
from json_formatter import NewsJsonFormatter


class NewsReader:
    def __init__(self, link, limit, json, date):
        self.link = link
        self.limit = limit
        self.json = json
        self.hrefs = []
        self.news = []
        self.date = date
        self.json_object = NewsJsonFormatter()

        ext_site_name = extract(self.link)
        site_name = f'{ext_site_name.domain}.{ext_site_name.suffix}'
        
        self.cacher_object = NewsCacher('cached_news.json', site_name)

    def parse_url(self):
        """Get RSS xml-file from url"""
        logging.info('Get RSS XML-file from url')

        self.feed = feedparser.parse(self.link)
        self.parse_xml(self.feed.entries[:self.limit])

    def parse_xml(self, source):
        """Parse xml-file to news array"""
        logging.info('Parse XML-file to news array')

        for item in source:
            content = []

            try:
                for element in item.media_content:
                    content.append(element['url'])
            except AttributeError:
                try:
                    for element in item.media_thumbnail:
                        content.append(element['url'])
                except AttributeError:
                    content.append('No content!')

            self.news.append({"title": item.title, "date": item.published, 
                "text": self.strip_html_string(item.description), "link": item.link.split('?')[0], "hrefs": content})

        if self.date == None:
            self.cacher_object.cache(self.news)

        if self.json is True:
            self.json_object.format(self.news)

    def print_news(self):
        """Print news to console"""
        logging.info('Print news to console')

        if self.date != None:
            try:
                news = self.cacher_object.get_cached_news(self.date, self.limit)
            except FileNotFoundError:
                print('Cache file not found :(')
                return

            if news == []:
                print('News for this date not found :(')
                return

            if self.json is True:
                self.json_object.format(news)
                print(self.json_object)
            else:
                for element in news:
                    self.print_one_news(element)
                    print('\n'*5)
        elif self.json is True:
            print(self.json_object)
        else:
            for element in self.news:
                self.print_one_news(element)
                print('\n'*5)

    def print_one_news(self, element, cached=False):
        """Print one news to console"""

        print(f'Title: {element["title"]}')
        if cached == True:
            print(f'Date:  {element["date"]}')
        print(f'Link: {element["link"]}')
        print('News text:')
        print(element["text"])
        print('Hrefs:')
        for href in element["hrefs"]:
            print('| ' + href)

    def strip_html_string(self, string):
        """Remove html tags from a string"""
        strip_string = re.compile('<.*?>')
        return re.sub(strip_string, '', string)
