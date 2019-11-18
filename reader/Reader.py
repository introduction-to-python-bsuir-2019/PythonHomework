import feedparser
import logging
from bs4 import BeautifulSoup
from datetime import datetime

from NewsItem import NewsItem
from Image import Image


class Reader:
    """
    Class which can parse html pages and get news from them.
    """
    is_verbose = False

    def __init__(self, rss_url):
        """
        Initialise _rss_url and _news fields.
        :param rss_url: url, which should be pursed further.
        """
        self._rss_url = rss_url
        self._news = list()

    def parse_rss(self):
        """
        Parse url for rss-reader.
        :return: parsed page.
        """
        logging.basicConfig(filename="rss_reader.log", filemode="w", level=logging.INFO)
        try:
            result = feedparser.parse(self._rss_url)
            if self.is_verbose:
                print(str(datetime.now()) + "\tNews are parsed successfully.")
            else:
                logging.info(str(datetime.now()) + "\tNews are parsed successfully.")
            return result
        except Exception as e:
            if self.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                logging.error(str(datetime.now()) + "\t" + str(e))
        return None

    def get_news(self, amount_news):
        """
        Get news from the parsed page and define fields of the NewsItems.
        :param amount_news: amount of news, which should be returned.
        :return: dict with defined amount of news.
        """
        feed = self.parse_rss()
        for news_item in feed['entries']:
            item = NewsItem(news_item.get('title', 'No title'),
                            # TODO: add description
                            news_item.get('link', 'No link'),
                            news_item.get('published', 'No date'),
                            Reader._get_images(news_item.get('summary', None)),
                            Reader._get_links(news_item.get('summary', None)))
            self._news.append(item)
        if self.is_verbose:
            print(str(datetime.now()) + "\t{0} news were given".format(amount_news))
        else:
            logging.info(str(datetime.now()) + "\t{0} news were given.".format(amount_news))
        return self._news[:amount_news]

    @staticmethod
    def _get_images(html_address):
        """
        Get image from the parsed page.
        :param html_address: address, where images should be searched.
        :return: Image object with defined fields.
        """
        images = list()
        try:
            soup = BeautifulSoup(html_address, features="lxml")
            if Reader.is_verbose:
                print(str(datetime.now()) +
                      "\tParsing object was successfully created with help of BeautifulSoup for parsing images.")
            else:
                logging.info(str(datetime.now()) +
                             "\tParsing object was successfully created with help of"
                             " BeautifulSoup for parsing images.")
            for image in soup.find_all('img'):
                src = image.get('src', '')
                alt = image.get('alt', '')
                images.append(Image(alt, src))
        except Exception as e:
            if Reader.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                logging.error(str(datetime.now()) + "\t" + str(e))
        return images

    @staticmethod
    def _get_links(html_address):
        """
        Get links from the parsed page.
        :param html_address: address, where links should be searched.
        :return: list of links, which were find in that page.
        """
        links = list()
        try:
            soup = BeautifulSoup(html_address, features="lxml")
            if Reader.is_verbose:
                print(str(datetime.now()) +
                      "\tParsing object was successfully created with help of BeautifulSoup for parsing links.")
            else:
                logging.info(str(datetime.now()) +
                             "\tParsing object was successfully created with help of "
                             "BeautifulSoup for parsing links.")
            for link in soup.find_all('a'):
                if link.get('href', None):
                    links.append(link['href'])
        except Exception as e:
            if Reader.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                logging.error(str(datetime.now()) + "\t" + str(e))
        return links
