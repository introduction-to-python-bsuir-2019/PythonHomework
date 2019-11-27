import feedparser
from bs4 import BeautifulSoup
import logging
from collections import namedtuple


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
        self.image_data = namedtuple('image', 'alt url')
        self.article = namedtuple('article', 'title date url description links')

    def parse_rss(self):
        if self.verbose:
            logger = create_logger('rss-parser')
            logger.info('logging enabled')
        rss_feed = feedparser.parse(self.url)
        if self.verbose:
            logger.info(f'{self.limit} news have been fetched')
        self.feed = rss_feed['feed']['title']
        if self.limit > 0:
            entries = rss_feed.entries[:self.limit]
        else:
            entries = rss_feed.entries
        self.news += self.create_articles(entries)
        result = ''
        result += self.create_result_string()
        return result

    def parse_links(self, entry):
        link_id = 0
        parsed_links = []
        for entry_link in entry.get('links'):
            link_url = entry_link['url']
            my_link = self.link_data(link_id, link_url, 'link')
            parsed_links.append(my_link)
            link_id += 1
        return parsed_links

    def parse_images(self, links_count, soup):
        link_id = links_count
        parsed_images = []
        for entry_image in soup.findAll('img'):
            image_alt = entry_image['alt']
            image_url = entry_image['src']
            my_image = self.image_data(image_alt, image_url)
            my_link = self.link_data(link_id, my_image, 'image')
            parsed_images.append(my_link)
            link_id += 1
        return parsed_images

    def create_articles(self, entries):
        parsed_articles = []
        for entry in entries:
            title = (entry.get('title'))
            date = entry.get('published')
            url = entry.get('link')
            links = []
            links += self.parse_links(entry)
            soup = BeautifulSoup(entry['summary_detail']['value'], features='html.parser')
            description = soup.text
            links_count = len(links)
            links += self.parse_images(links_count, soup)
            my_article = self.article(title, date, url, description, links)
            parsed_articles.append(my_article)
        return parsed_articles

    def feed_to_json(self):
        json_news_objects = [recursive_to_json(news_obj) for news_obj in self.news]
        return {'news': {'feed': self.feed, 'news_objects': json_news_objects}, 'url': self.url}

    def create_result_string(self):
        result_string = ''
        result_string += f'\nFeed: {self.feed}\n\n'
        for article in self.news:
            result_string += f'Title: {article.title}\nDate: {article.date}\nUrl: {article.url}\n\n'
            for l in article.links:
                if l.type == 'image':
                    result_string += f'[image {l.id + 1} : {l[1].alt}][{l.id + 1}]'
                    result_string += f'{article.description}\n\n'
            for l in article.links:
                if l.type == 'image':
                    result_string += f'[{l.id + 1}]: {l[1].url} ({l.type})\n'
                else:
                    result_string += f'[{l.id + 1}]: {l.url} ({l.type})\n'
            result_string += f'\n'
        return result_string


def recursive_to_json(obj):
    _json = {}
    if isinstance(obj, tuple):
        obj_data = obj._asdict()
        for data in obj_data:
            if isinstance(obj_data[data], tuple):
                _json[data] = (recursive_to_json(obj_data[data]))
            _json[data] = (obj_data[data])
    return _json


def create_logger(logging_module):
    logger = logging.getLogger(logging_module)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
