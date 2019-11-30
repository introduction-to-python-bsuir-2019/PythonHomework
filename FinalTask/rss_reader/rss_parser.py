import feedparser
import logging
import datetime
import os
import json
from collections import namedtuple
from bs4 import BeautifulSoup


class RssParser:
    """
    Class to parse RSS-news
    """
    def __init__(self, url, limit, verbose, date):
        """
        This function initializes the RssParser instance
        :param url: rss-feed to be parsed
        :param limit: number of news to be printed
        :param verbose: flag of verbosity
        :param date: date to print news of the specified day
        :return: None
        """
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
        """
        This function parses rss-link
        :return: None
        """
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
        """
        This function parses link (link or image) and creates link or image data object (namedtuple)
        :param entry_link: link to be parsed
        :param link_id: link id in list of links
        :param link_type: image or just a link
        :return: parsed_link - link or image date object (namedtuple)
        """
        if link_type == 'link':
            link_url = entry_link['href']
            parsed_link = self.link_data(link_id, link_url, 'link')
        else:
            image_alt = entry_link['alt']
            image_url = entry_link['src']
            parsed_link = self.image_data(link_id, image_url, 'image', image_alt)
        return parsed_link

    def create_article(self, entry):
        """
        This function parses raw article and creates article object from it (namedtuple)
        :param entry: article to be parsed
        :return: parsed_article - article data object (namedtuple)
        """
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
        parsed_article = self.article(title, date, url, description, links)
        return parsed_article

    def parse_json_cache(self):
        """
        This function parses json cache from cache text file
        :return: None
        """
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
        return

    def parse_cached_link(self, link):
        """
        This function parses cached link and creates link or image data object (namedtuple) from it
        :param link: link to be parsed
        :return: parsed_link - link or image data object (namedtuple)
        """
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
        """
        This function parses cached article and creates article data object (namedtuple) from it
        :param article: article to be parsed
        :return: parsed_article - article data object (namedtuple)
        """
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
        """
        This function converts current feed to JSON format
        :return: None
        """
        article_list = []
        for article in self.news:
            my_article_dict = self.article_to_json(article)
            article_list.append(my_article_dict)
        return {'feed': self.feed, 'url': self.url, 'news_objects': article_list}

    def article_to_json(self, article):
        """
        This function converts article to JSON format
        :param article: article to be converted
        :return: json_article_dict - article in JSON dictionary format
        """
        links_list = []
        for link in article.links:
            my_json_link = self.link_to_json(link)
            links_list.append(my_json_link)
        json_article_dict = dict(zip(('title', 'date', 'url', 'description', 'links'),
                                     (article.title, article.date, article.url, article.description, links_list)))
        return json_article_dict

    @staticmethod
    def link_to_json(link):
        """
        This function converts link to JSON format
        :param link:
        :return: json_link_dict - link in JSON dictionary format
        """
        if link.type == 'link':
            json_link_dict = dict(zip(('id', 'url', 'type'), (link.id, link.url, link.type)))
        else:
            json_link_dict = dict(zip(('id', 'url', 'type', 'alt'), (link.id, link.url, link.type, link.alt)))
        return json_link_dict

    def feed_to_string(self):
        """
        This function converts current feed to string to be printed out
        :return: result_string - string contains news to be printed in human-readable format
        """
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

    def feed_to_html(self):
        result_string = ''
        result_string += f'<!DOCTYPE html><html><title>rss-feed</title>'
        result_string += f'<body><h3>Feed: {self.feed}</h3>'
        for article in self.news:
            result_string += f'<h4 style="display:inline">Title:</h4><span> {article.title}</span><br>' \
                             f'<h4 style="display:inline">Date:</h4><span> {article.date}</span><br>' \
                             f'<h4 style="display:inline">Url:</h4><span> {article.url}</span><br><br>'
            for link in article.links:
                if link.type == 'image':
                    result_string += f'<img src="{link.url}" width="20%"><br><br>'
                    result_string += f'<span>{article.description}</span><br><br>'
                    break
            for link in article.links:
                if link.type == 'image':
                    result_string += f'<span>[{link.id + 1}]: </span>' \
                                     f'<a href="{link.url}">{link.alt}({link.type})</a><br>'
                else:
                    result_string += f'<span>[{link.id + 1}]: </span>' \
                                     f'<a href="{link.url}">{link.url}({link.type})</a><br>'
            result_string += f'</body></html><br>'
        return result_string

    def cache_feed_to_text_file(self):
        """
        This function caches current feed to cache text file
        :return: None
        """
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

    def cache_feed_to_html_file(self):
        if os.path.exists("news_cache.html"):
            with open("news_cache.html", 'w+') as cache_file:
                cache_file.write(self.feed_to_html())
        else:
            cache_file = open("news_cache.html", 'w+')
            cache_file.close()
            self.cache_feed_to_html_file()


def create_logger(logging_module):
    """
    This function creates logger
    :param logging_module: logging module to be used
    :return: logger - logger for current module
    """
    logger = logging.getLogger(logging_module)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
