"""RSS-reader module"""

import feedparser
import logging

from article import Article
from json_format import JsonFormat


class Reader:
    logger = logging.getLogger('__main__.py')

    def __init__(self, link, limit, json):
        self.link = link
        self.limit = limit
        self.articles = []
        self.json = json
        self.hrefs = []

    def parse_url(self):
        """Get RSS xml-file from url"""
        self.logger.info('Get RSS XML-file from url')

        self.feed = feedparser.parse(self.link)
        self.parse_xml(self.feed)

    def parse_xml(self, source):
        """Parse xml-file to articles"""
        self.logger.info('Parse XML-file to articles')

        i = 0
        for item in source.entries:
            content = []
            for element in item.media_content:
                content.append(element['url'])

            self.articles.append(Article(item.title, item.published, item.description, item.link, content))

            i += 1
            if i == self.limit:
                break

        if self.json is True:
            json_format = JsonFormat()
            feeds = self.articles_to_array()
            json_format.format(feeds)

    def articles_to_array(self):
        self.logger.info('Convert articles to array of dicts')

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
        self.logger.info('Print articles to console')

        for article in self.articles:
            self.print_article(article)
            print('\n-------------------------\n')

    def print_article(self, article):
        """Print article to console"""

        print(f'Title: {article.title}')
        print(f'Date:  {article.date}')
        print(f'Link: {article.link}')
        print('\nArticle text:')
        print(article.text)
        print('\nHrefs:')
        for href in article.hrefs:
            print(href)
