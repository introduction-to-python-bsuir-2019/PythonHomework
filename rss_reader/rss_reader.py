"""RSS-reader module"""

import feedparser
import logging

from tldextract import extract

from .article import Article
from .json_formatter import NewsJsonFormatter
from .news_cacher import NewsCacher


class Reader:
    def __init__(self, link, limit, json, date):
        self.link = link
        self.limit = limit
        self.articles = []
        self.json = json
        self.hrefs = []
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
        """Parse xml-file to articles"""
        logging.info('Parse XML-file to articles')

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

            self.articles.append(Article(item.title, item.published, item.description, item.link, content))

        feeds = self.articles_to_array()
        if self.date == None:
            self.cacher_object.cache(feeds)

        if self.json is True:
            self.json_object.format(feeds)

    def articles_to_array(self):
        """Convert articles to array of dicts"""
        logging.info('Convert articles to array of dicts')

        array = []
        for article in self.articles:
            feed_dict = {}
            feed_dict.update({'title': article.title})
            feed_dict.update({'date': article.date})
            feed_dict.update({'text': article.text})
            feed_dict.update({'link': article.link})
            feed_dict.update({'hrefs': article.hrefs})
            array.append(feed_dict)

        return array

    def print_articles(self):
        """Print articles to console"""
        logging.info('Print articles to console')

        if self.json is True:
            print(self.json_object)
        elif self.date != None:  
            try:
                news = self.cacher_object.get_cached_news(self.date, self.limit)
            except FileNotFoundError:
                print('Cache file not found :(')
                return

            if news == []:
                print('News for this date not found :(')
                return
                
            for article in news:
                self.print_cached_article(article)
                print('\n'*5)
        else:
            for article in self.articles:
                self.print_article(article)
                print('\n'*5)

    def print_article(self, article):
        """Print article to console"""

        print(f'Title: {article.title}')
        print(f'Date:  {article.date}')
        print(f'Link: {article.link}')
        print('Article text:')
        print(article.text)
        print('Hrefs:')
        for href in article.hrefs:
            print('| ' + href)

    def print_cached_article(self, article):
        """Print cached article to console"""

        print(f'Title: {article["title"]}')
        print(f'Link: {article["link"]}')
        print('Article text:')
        print(article["text"])
        print('Hrefs:')
        for href in article["hrefs"]:
            print('| ' + href)
