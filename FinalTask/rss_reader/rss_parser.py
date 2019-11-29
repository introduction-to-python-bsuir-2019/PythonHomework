import feedparser
from bs4 import BeautifulSoup
import logging
import datetime
import os
import json
from collections import namedtuple


class RssParser:
    """
    Class to parse RSS-news
    """

    def __init__(self, url, limit, verbose, date):
        self.url = url
        self.limit = limit
        self.feed = ''
        self.news = []
        self.verbose = verbose
        self.date = date
        self.link_data = namedtuple('link', 'id url type')
        self.image_data = namedtuple('image', 'id url type alt')
        self.article = namedtuple('article', 'title date url description links')
        if self.verbose:
            self.logger = create_logger('rss-parser')
            self.logger.info('logging enabled')

    def parse_rss(self):
        rss_feed = feedparser.parse(self.url)
        if self.verbose:
            self.logger.info(f'{self.limit} news have been fetched')
        self.feed = rss_feed['feed']['title']
        if self.limit > 0:
            entries = rss_feed.entries[:self.limit]
        else:
            entries = rss_feed.entries
        for entry in entries:
            my_article = self.create_article(entry)
            self.news.append(my_article)

    def parse_rss_link(self, entry_link, link_id, link_type):
        if link_type == 'link':
            link_url = entry_link['href']
            my_link = self.link_data(link_id, link_url, 'link')
        else:
            image_alt = entry_link['alt']
            image_url = entry_link['src']
            my_link = self.image_data(link_id, image_url, 'image', image_alt)
        return my_link

    def create_article(self, entry):
        title = (entry.get('title').replace('&#39;', "'"))
        date = entry.get('published')
        url = entry.get('link')
        links = []
        soup = BeautifulSoup(entry['summary_detail']['value'], features='html.parser')
        for entry_link in soup.findAll('a'):
            my_link = self.parse_rss_link(entry_link, len(links), 'link')
            links.append(my_link)
        for entry_image in soup.findAll('img'):
            my_link = self.parse_rss_link(entry_image, len(links), 'image')
            links.append(my_link)
        description = soup.text.replace('&#39;', "'")
        my_article = self.article(title, date, url, description, links)
        return my_article

    def parse_json_cache(self):
        if os.path.exists("news_cache.txt") and os.path.getsize("news_cache.txt") > 0:
            with open("news_cache.txt", 'r') as cache_file:
                json_cache = json.load(cache_file)
            for feed_instance in json_cache['news']:
                if feed_instance['url'] == self.url:
                    self.feed = feed_instance['feed']
                    cached_news = feed_instance['news_objects']
                    for article in cached_news:
                        my_article = self.create_cached_article(article)
                        if any(char in my_article.date for char in ('+', '-')):
                            my_article_date_obj = datetime.datetime.strptime(my_article.date,
                                                                             '%a, %d %b %Y %H:%M:%S %z')
                        else:
                            my_article_date_obj = datetime.datetime.strptime(my_article.date,
                                                                             '%a, %d %b %Y %H:%M:%S %Z')
                        my_article_date_string = datetime.datetime.strftime(my_article_date_obj, '%Y%m%d')
                        if my_article_date_string == self.date:
                            self.news.append(my_article)
                    if self.limit > 0:
                        self.news = self.news[:self.limit]
                    cached_news_count = self.limit if self.limit >= len(cached_news) else len(cached_news)
                    total_cached_news = 0
                    for feed in json_cache['news']:
                        total_cached_news += len(feed['news_objects'])
                    if self.verbose:
                        self.logger.info(f'{cached_news_count} news have been fetched from local cache')
                        self.logger.info(f'{total_cached_news} news are in the local cache now')
        else:
            print('Parse some online news first so there will be something to read from cache')
            exit()
        return len(cached_news)

    def parse_cached_link(self, link):
        if link['type'] == 'image':
            link_id = link['id']
            image_url = link['url']
            link_type = link['type']
            image_alt = link['alt']
            parsed_link = self.image_data(link_id, image_url, link_type, image_alt)
        else:
            link_id = link['id']
            link_url = link['url']
            link_type = link['type']
            parsed_link = self.link_data(link_id, link_url, link_type)
        return parsed_link

    def create_cached_article(self, article):
        parsed_links = []
        for link in article['links']:
            my_link = self.parse_cached_link(link)
            parsed_links.append(my_link)
        title = article['title']
        date = article['date']
        url = article['url']
        description = article['description']
        links = parsed_links
        parsed_article = self.article(title, date, url, description, links)
        return parsed_article

    def feed_to_json(self):
        article_list = []
        for article in self.news:
            my_article_dict = self.article_to_json(article)
            article_list.append(my_article_dict)
        return {'feed': self.feed, 'url': self.url, 'news_objects': article_list}

    def article_to_json(self, article):
        links_list = []
        for link in article.links:
            my_json_link = self.link_to_json(link)
            links_list.append(my_json_link)
        my_article_dict = dict(zip(('title', 'date', 'url', 'description', 'links'),
                                   (article.title, article.date, article.url, article.description, links_list)))
        return my_article_dict

    @staticmethod
    def link_to_json(link):
        if link.type == 'link':
            my_link_dict = dict(zip(('id', 'url', 'type'), (link.id, link.url, link.type)))
        else:
            my_link_dict = dict(zip(('id', 'url', 'type', 'alt'), (link.id, link.url, link.type, link.alt)))
        return my_link_dict

    def feed_to_string(self):
        if len(self.news) == 0:
            return 'No news for that day, try another'
        else:
            result_string = ''
            result_string += f'\nFeed: {self.feed}\n\n'
            for article in self.news:
                result_string += f'Title: {article.title}\nDate: {article.date}\nUrl: {article.url}\n\n'
                for link in article.links:
                    if link.type == 'image':
                        result_string += f'[image {link.id + 1} : {link.alt}][{link.id + 1}]'
                        result_string += f'{article.description}\n\n'
                        break
                for link in article.links:
                    if link.type == 'image':
                        result_string += f'[{link.id + 1}]: {link.url} ({link.type})\n'
                    else:
                        result_string += f'[{link.id + 1}]: {link.url} ({link.type})\n'
                result_string += f'\n'
            return result_string

    def cache_feed_to_file(self):
        if not os.path.exists("news_cache.txt"):
            cache_file = open("news_cache.txt", 'w+')
            cache_file.close()
        json_feed = self.feed_to_json()
        if os.path.getsize("news_cache.txt") > 0:
            with open("news_cache.txt", 'r') as cache_file:
                json_cache = json.load(cache_file)
                found = False
                for feed in json_cache['news']:
                    if feed['url'] == self.url:
                        found = True
                        cached_news = 0
                        for news in json_feed['news_objects']:
                            if news not in feed['news_objects']:
                                feed['news_objects'].append(news)
                                cached_news += 1
                if not found:
                    json_cache['news'].append(json_feed)
                    cached_news = len(json_feed['news_objects'])
                total_cached_news = 0
                for feed in json_cache['news']:
                    total_cached_news += len(feed['news_objects'])
            with open("news_cache.txt", 'w') as cache_file:
                json.dump(json_cache, cache_file)
        else:
            with open("news_cache.txt", 'w') as cache_file:
                json_file_format = {'news': [json_feed]}
                json.dump(json_file_format, cache_file)
                cached_news = total_cached_news = len(json_feed['news_objects'])
        if self.verbose:
            self.logger.info(f'{cached_news} online news have been saved in local cache (duplicates were removed)')
            self.logger.info(f'{total_cached_news} online news are cached in the file now')
        return total_cached_news


def create_logger(logging_module):
    logger = logging.getLogger(logging_module)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
