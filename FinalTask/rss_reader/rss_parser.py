import os
import logging
import json
import feedparser
import requests
from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup
from fpdf import FPDF


class RssParser:
    """
    Class to parse RSS-news
    """
    def __init__(self, url: str, limit: int, verbose: bool, date: str, html_path: str, pdf_path: str):
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
            self.logger = self.create_logger('rss-parser')
            self.logger.info('logging enabled')
        self.data_path = self.create_folder(os.path.dirname(__file__), 'data')
        self.img_path = self.create_folder(self.data_path, 'images')
        self.html_path = html_path
        self.pdf_path = pdf_path
        if self.verbose:
            self.logger.info('RssReader object was initialized successfully')

    def parse_rss(self):
        """
        This function parses rss-link
        :return: None
        """
        rss_feed = feedparser.parse(self.url)
        if rss_feed['bozo']:
            raise ValueError("Wrong URL address or Internet access is unavailable")
        if self.verbose:
            self.logger.info(f'Source feed was received')
        self.feed = rss_feed['feed']['title']
        if self.limit > 0:
            entries = rss_feed.entries[:self.limit]
            if self.verbose:
                self.logger.info(f'News number in feed was cropped down to {self.limit} news')
        else:
            entries = rss_feed.entries
        for entry in entries:
            my_article = self.create_article(entry)
            self.news.append(my_article)
        if self.verbose:
            self.logger.info(f'{self.limit} news have been fetched from source')

    def parse_rss_link(self, entry_link: dict, link_id: int, link_type: str) -> namedtuple:
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

    def create_article(self, entry: dict) -> namedtuple:
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
        This function parses json cache from cache json file
        :return: None
        """
        cache_file_path = os.path.join(self.data_path, "news_cache.json")
        if os.path.exists(cache_file_path) and os.path.getsize(cache_file_path) > 0:
            with open(cache_file_path, 'r') as cache_file:
                json_cache = json.load(cache_file)
                if self.verbose:
                    self.logger.info(f'News are getting fetched from local cache. '
                                     f'Path to cache file: {cache_file_path}')
            for feed_instance in json_cache['news']:
                if feed_instance['url'] == self.url:
                    self.feed = feed_instance['feed']
                    cached_news = feed_instance['news_objects']
                    for article in cached_news:
                        my_article = self.create_cached_article(article)
                        my_article_date_string = self.format_date_string(article['date'])
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
            print('rss-reader: info : Parse some online news first so there will be something to read from cache')
            exit()

    @staticmethod
    def format_date_string(date: str) -> str:
        """
        This function converts time strings to %Y%m%d format to compare date of article with input
        :param date:
        :return: my_article_date_string - converted date string
        """
        if any(char in date for char in ('+', '-')):
            my_article_date_obj = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        else:
            my_article_date_obj = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        my_article_date_string = datetime.strftime(my_article_date_obj, '%Y%m%d')
        return my_article_date_string

    def parse_cached_link(self, link: dict) -> namedtuple:
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

    def create_cached_article(self, article: dict) -> namedtuple:
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
        if self.verbose:
            self.logger.info('Feed was converted to JSON format')

        return {'feed': self.feed, 'url': self.url, 'news_objects': article_list}

    def article_to_json(self, article: namedtuple) -> dict:
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
    def link_to_json(link: namedtuple) -> dict:
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
        :return: result_string - string containing news to be printed in human-readable format
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
                result_string += f'Links:\n'
                for link in article.links:
                    if link.type == 'image':
                        if link.url:
                            result_string += f'[{link.id + 1}]: {link.url} ({link.type})\n'
                        else:
                            result_string += f'[{link.id + 1}]: {link.alt} (invalid url or no image)({link.type})\n'
                    else:
                        result_string += f'[{link.id + 1}]: {link.url} ({link.type})\n'
                result_string += f'\n'
            if self.verbose:
                self.logger.info('Feed was converted to text format')
            return result_string

    def feed_to_html(self):
        """
        This function converts current feed to string to be written to HTML file
        :return: result_string - string containing news to be written to HTML file
        """
        result_string = ''
        result_string += f'<!DOCTYPE html><html><title>rss-feed</title>'
        result_string += f'<body><h3>Feed: {self.feed}</h3>'
        for article in self.news:
            result_string += f'<h4 style="display:inline">Title:</h4><span> {article.title}</span><br>' \
                             f'<h4 style="display:inline">Date:</h4><span> {article.date}</span><br>' \
                             f'<h4 style="display:inline">Url:</h4><span> {article.url}</span><br><br>'
            for link in article.links:
                if link.type == 'image':
                    result_string += f'<img src="{link.url}" width="10%"><br><br>'
                    result_string += f'<span>{article.description}</span><br><br>'
                    break
            result_string += f'<span>Links:</span><br>'
            for link in article.links:
                if link.type == 'image':
                    if link.url:
                        result_string += f'<span>[{link.id + 1}]: </span>' \
                                         f'<a href="{link.url}">{link.alt}({link.type})</a><br>'
                    else:
                        result_string += f'<span>[{link.id + 1}]: </span>' \
                                         f'<span>{link.alt}(invalid url or no image)({link.type})</span><br>'
                else:
                    result_string += f'<span>[{link.id + 1}]: </span>' \
                                     f'<a href="{link.url}">{link.url}({link.type})</a><br>'
            result_string += f'</body></html><br>'
        if self.verbose:
            self.logger.info('Feed was converted to HTML format')
        return result_string

    def feed_to_pdf(self):
        """
        This function converts current feed to PDF document
        :return: pdf - PDF document containing news feed
        """
        pdf = FPDF()
        pdf.add_page()
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'ttf', 'DejaVuSerifCondensed.ttf')
        pdf.add_font('DejaVu', '', font_path, uni=True)
        pdf.set_font('DejaVu', '', 14)
        pdf.set_margins(10, 10, 5)
        pdf.cell(w=0, h=5, txt=self.feed)
        pdf.ln()
        pdf.ln()
        for article in self.news:
            pdf.set_font_size(12)
            pdf.multi_cell(w=0, h=5, txt=f'Title: {article.title}')
            pdf.multi_cell(w=0, h=5, txt=f'Date: {article.date}')
            pdf.multi_cell(w=0, h=5, txt=f'Url: {article.url}')
            pdf.ln()
            images = self.download_images(article, self.img_path, self.news.index(article))
            if len(images):
                if images[0]:
                    pdf.image(images[0], w=30)
            pdf.ln()
            pdf.multi_cell(w=0, h=5, txt=article.description)
            pdf.ln()
            pdf.cell(w=0, h=5, txt=f'Links:')
            pdf.ln()
            for link in article.links:
                if link.type == 'image':
                    if link.url:
                        pdf.multi_cell(w=0, h=5, txt=f'[{link.id + 1}]: {link.url} ({link.type})')
                    else:
                        pdf.multi_cell(w=0, h=5, txt=f'[{link.id + 1}]: {link.alt} (invalid url or no image)'
                                                     f'({link.type})')
                else:
                    pdf.multi_cell(w=0, h=5, txt=f'[{link.id + 1}]: {link.url} ({link.type})')
            pdf.ln()
            pdf.ln()
        if self.verbose:
            self.logger.info('Feed was converted to PDF format')
        return pdf

    def cache_feed_to_json_file(self):
        """
        This function caches current feed to cache .json file
        :return: None
        """
        cache_file_path = os.path.join(self.data_path, "news_cache.json")
        if not os.path.exists(cache_file_path):
            cache_file = open(cache_file_path, 'w+')
            cache_file.close()
            if self.verbose:
                self.logger.info(f'News cache has been created. '
                                 f'Path to cache file: {cache_file_path}')
        json_feed = self.feed_to_json()
        if os.path.getsize(cache_file_path) > 0:
            with open(cache_file_path, 'r') as cache_file:
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
            with open(cache_file_path, 'w') as cache_file:
                json.dump(json_cache, cache_file)
        else:
            with open(cache_file_path, 'w') as cache_file:
                json_file_format = {'news': [json_feed]}
                json.dump(json_file_format, cache_file)
                cached_news = total_cached_news = len(json_feed['news_objects'])
        if self.verbose:
            self.logger.info(f'{cached_news} online news have been saved in local cache (duplicates were removed)')
            self.logger.info(f'{total_cached_news} online news are cached in the file now')

    def cache_feed_to_html_file(self):
        """
        This function caches current feed to cache HTML file
        :return: None
        """
        if self.html_path == "default":
            cache_file_path = os.path.join(self.data_path, 'news_cache.html')
        else:
            if self.html_path == os.path.abspath(self.html_path):
                cache_file_path = self.html_path
            else:
                cache_file_path = os.path.join(os.getcwd(), self.html_path)
        if not os.path.exists(cache_file_path):
            html_cache_file = open(cache_file_path, "w+")
            html_cache_file.close()
        if os.path.isfile(cache_file_path):
            with open(cache_file_path, 'w+', encoding='utf8') as cache_file:
                cache_file.write(self.feed_to_html())
                if self.verbose:
                    self.logger.info(f'News have been cached to HTML file. Path to file: {cache_file_path}')

    def cache_feed_to_pdf_file(self):
        """
        This function caches current feed to cache PDF file
        :return: None
        """
        if self.pdf_path == "default":
            cache_file_path = os.path.join(self.data_path, 'news_cache.pdf')
        else:
            if self.pdf_path == os.path.abspath(self.pdf_path):
                cache_file_path = self.pdf_path
            else:
                cache_file_path = os.path.join(os.getcwd(), self.pdf_path)
        if not os.path.exists(cache_file_path):
            pdf_cache_file = open(cache_file_path, "w+")
            pdf_cache_file.close()
        pdf = self.feed_to_pdf()
        if os.path.isfile(cache_file_path):
            pdf.output(cache_file_path)
            if self.verbose:
                self.logger.info(f'News have been cached to PDF file. Path to file: {cache_file_path}')

    @staticmethod
    def create_logger(logging_module: str):
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

    def create_folder(self, path: str, folder_name: str) -> str:
        """
        This function creates new folder
        :param path: path where new folder will be created
        :param folder_name: name of new folder
        :return: new_folder_path - path to created folder
        """
        if os.path.exists(path):
            new_folder_path = os.path.join(path, folder_name)
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)
                if self.verbose:
                    self.logger.info(f'New folder was created. Path to folder: {new_folder_path}')
        return new_folder_path

    @staticmethod
    def download_content_from_url(dest: str, source: str, name: str) -> str:
        """
        This function downloads file from URL
        :param dest: folder to save file
        :param source: url to file
        :param name: name of downloaded file
        :return: path_to_file - path to downloaded file
        """
        path_to_file = os.path.join(dest, name)
        resource = requests.get(source)
        with open(path_to_file, 'wb') as content_file:
            content_file.write(resource.content)
        return path_to_file

    def download_images(self, article: namedtuple, path: str, article_index: int) -> list:
        """

        :param article: article from which images are downloaded
        :param path: path to store downloaded images
        :param article_index: article index in feed list
        :return: images - list of images paths in local storage
        """
        images = []
        image_index = 0
        for link in article.links:
            if link.type == 'image':
                if link.url:
                    image_path = self.download_content_from_url(path, link.url, f'{article_index}_{image_index}.jpg')
                    images.append(image_path)
                    image_index += 1
        return images
