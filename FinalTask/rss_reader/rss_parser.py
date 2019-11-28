import feedparser
from bs4 import BeautifulSoup
import logging
from collections import namedtuple, OrderedDict


class RssParser:
    """
    Class to parse RSS-news
    """

    def __init__(self, url, limit, verbose):
        self.url = url
        self.limit = limit
        self.feed = ''
        self.news = []
        self.verbose = verbose
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
        title = (entry.get('title'))
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

    def parse_json_cache(self, json_cache):
        for feed_instance in json_cache['news']:
            self.feed = feed_instance['feed']
            self.url = feed_instance['url']
            cached_news = feed_instance['news_objects']
            for article in cached_news:
                my_article = self.create_cached_article(article)
                self.news.append(my_article)
            if self.verbose:
                self.logger.info(f'{self.limit} news have been fetched from local cache')

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
        return {'news': [{'feed': self.feed, 'url': self.url, 'news_objects': article_list}]}

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


def create_logger(logging_module):
    logger = logging.getLogger(logging_module)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
