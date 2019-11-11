import feedparser
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
        try:
            result = feedparser.parse(self._rss_url)
            if self.is_verbose:
                print(str(datetime.now()) + "\tNews are parsed successfully.")
            return result
        except Exception as e:
            if self.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                with open("error_log.txt", "w") as error_file:
                    error_file.write(str(datetime.now()) + "\t" + str(e))
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
                            Reader._get_image(news_item.get('summary', None)),
                            Reader._get_links(news_item.get('summary', None)))
            self._news.append(item)
        if self.is_verbose:
            print(str(datetime.now()) + "\t{0} news were given".format(amount_news))
        else:
            with open("data_log.txt", "w") as date_log_file:
                date_log_file.write(str(datetime.now()) + "\t{0} news were given.".format(amount_news))
        return self._news[:amount_news]

    @staticmethod
    def _get_image(html_address):
        """
        Get image from the parsed page.
        :param html_address: address, where images should be searched.
        :return: Image object with defined fields.
        """
        try:
            soup = BeautifulSoup(html_address, features="lxml")
            if Reader.is_verbose:
                print(str(datetime.now()) +
                      "\tParsing object was successfully created with help of BeautifulSoup for parsing images.")
        except Exception as e:
            if Reader.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                with open("error_log.txt", "w") as error_file:
                    error_file.write(str(datetime.now()) + "\t" + str(e))
        for image in soup.find_all('img'):
            src = image.get('src', '')
            alt = image.get('alt', '')
            return Image(alt, src)

    @staticmethod
    def _get_links(html_address):
        """
        Get links from the parsed page.
        :param html_address: address, where links should be searched.
        :return: list of links, which were find in that page.
        """
        try:
            soup = BeautifulSoup(html_address, features="lxml")
            if Reader.is_verbose:
                print(str(datetime.now()) +
                      "\tParsing object was successfully created with help of BeautifulSoup for parsing links.")
        except Exception as e:
            if Reader.is_verbose:
                print(str(datetime.now()) + "\t" + str(e))
            else:
                with open("error_log.txt", "w") as error_file:
                    error_file.write(str(datetime.now()) + "\t" + str(e))
        links = list()
        for link in soup.find_all('a'):
            if link.get('href', None):
                links.append(link['href'])
        return links
