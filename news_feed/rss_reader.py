"""
Simple Rss reading module. Provides reading rss
by url. Cashing it into given directory. And reading
from file by date.

You can use it like script with argparse.
Print
>> python rss_reader.py --help
into command line to find more information

"""

import requests
import os

import datetime
from dateutil.parser import parse

import lxml.html as html
import lxml.etree as etree
import xml.etree.ElementTree as ET

import json
import sqlite3

import argparse
import logging
from colorama import init, Fore, Style

from .format_converter import (PdfNewsConverter,
                               FB2NewsConverter,
                               HTMLNewsConverter)  # no dot here -> not worked properly

from xml.etree.ElementTree import ParseError
from sqlite3 import OperationalError

init(convert=True)  # to use colorama

PROJECT_VERSION = '2.0'
PROJECT_DESCRIPTION = ''


class NewsNotFoundError(FileNotFoundError):
    pass


class NoNewsInCacheError(OperationalError):
    pass


class RssNotFoundError(ParseError):
    pass


class NewsReader:
    """
        Class for reading news from rss-format files.

        :param: url
    """

    def __init__(self, url, limit=None, caching=False, colorful=False):
        """

        :param url: url of rss
        :param limit: limit of news in feed
        """

        self.url = url
        self.limit = limit
        self.cashing = caching
        self.colorful = colorful
        self.items = None

    def add_news(self):
        """
        Is used to get news from self.url

        :return: None
        """

        self.items = self.get_news()

    def get_news(self):
        """
        Read rss from self.url and creates from it
        dictionary. If self.cashing is True -> cashed news

        :return: dictionary of news
        """

        try:
            request = requests.get(self.url)
        except requests.exceptions.MissingSchema:
            logging.warning(f'Invalid URL: {self.url}. Paste items by yourself.')
            raise

        if not request.ok:
            raise requests.exceptions.InvalidURL(f'You URL is invalid. Status code: {request.status_code}')
        else:
            logging.info('URL is valid, news were collected')

        logging.info(f'Status code: {request.status_code}')  # TODO: create understandable error status output

        result = request.text

        try:
            tree = ET.fromstring(result)
            logging.info('Rss was loaded.')
        except ParseError:
            raise RssNotFoundError('No rss on page.')

        items = dict()
        items.setdefault('title', ' ')
        items.setdefault('title_image', '')
        useful_tags = ['title', 'pubDate', 'link', 'description']

        for head_el in tree[0]:
            if head_el.tag == 'title':
                items['title'] = head_el.text
            if head_el.tag == 'image':
                for el in head_el:
                    if el.tag == 'url':
                        items['title_image'] = el.text

        for num, item in enumerate(tree.iter('item')):

            if self.limit is not None and self.limit == num:
                break

            items.setdefault(num, {})

            news_description = dict()

            news_description.setdefault('title', 'no title')
            news_description.setdefault('pubDate', str(datetime.datetime.today().date()))
            news_description.setdefault('link', 'no link')
            news_description.setdefault('description', 'no description')

            for description in item:
                if description.tag in useful_tags:
                    news_description[description.tag] = description.text

            text, image_link, image_text = NewsReader.parse_description(news_description['description'])

            news_description['description'] = text
            news_description['imageLink'] = image_link
            news_description['imageDescription'] = image_text

            items[num].update(news_description)

            if self.cashing:
                conn = sqlite3.connect('database.sqlite')
                NewsReader._cash_news_sql(items[num], conn)
                conn.close()

        logging.info('Dictionary from rss-feed was created')

        return items

    @staticmethod
    def _cash_news_sql(news, connection, dir='news_cash'):
        """
        Cashes news into sql database format by publication date
        into given directory

        !Important: connection to database was added for memory saving

        :param news: dictionary of given news
        :param connection: connection to sql database
        :param dir: directory into which we save news
        :return: None
        """

        date = NewsReader.get_date(news['pubDate'])
        date_id = ''.join(str(date).split('-'))

        values = list(news.values())
        column_names = list(news.keys())

        cursor = connection.cursor()

        # TODO: do something with unique values, because UNIQUE isn't really cool

        cursor.execute("""  
            CREATE TABLE IF NOT EXISTS news(
                dateId int NOT NULL,
                pubDate varchar(255),
                title varchar(255) UNIQUE,
                link varchar(255),
                description varchar(1000),
                imageLink varchar(1000),
                imageDescription varchar(1000)
            );
        """)  # is not secure?!

        try:
            cursor.execute("""
                INSERT INTO news
                VALUES (:dateId, :pubDate, :title, :link, :description, :imageLink, :imageDescription)        
            """, {'dateId': date_id,
                  'pubDate': date,
                  'title': news['title'],
                  'link': news['link'],
                  'description': news['description'],
                  'imageLink': news['imageLink'],
                  'imageDescription': news['imageDescription']})
            logging.info('News where cached')
        except sqlite3.IntegrityError:
            logging.warning('You have tried to add the same row into database')

        cursor.close()
        connection.commit()

    @staticmethod
    def read_by_date_sql(date, dir='news_cash'):
        """
        Reads news from sql database by given date
        from given directory

        :param date: news date
        :param dir: directory from which we get news
        :return: dictionary of news
        """

        try:
            conn = sqlite3.connect('database.sqlite')
            logging.info('Database was connected')
        except OperationalError:
            raise NoNewsInCacheError('Add news in cache')

        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT *
                FROM news
                WHERE dateId=:date
            """, (date, ))
            logging.info('News where added')
        except OperationalError:
            raise NoNewsInCacheError('Add news to cache')

        data = cursor.fetchall()

        headers = list(map(lambda x: x[0], cursor.description))

        items = dict()
        for index, row in enumerate(data):
            items.setdefault(index, dict())

            items[index] = dict(zip(headers, row))

        cursor.close()
        conn.close()

        return items

    @staticmethod
    def get_date(news_date):
        """
        Returns date of news publication

        :param news: string date from dictionary of given news
        :return: date of news publication
        """

        try:
            news_date = parse(news_date)
        except ValueError:
            print('There is not date. Today\'s has been pasted')
            news_date = datetime.datetime.today()

        news_date = news_date.date()

        return news_date

    @staticmethod
    def parse_description(description):
        """
        Return news description

        :param description: raw news description
        :return: news description
        """

        text = NewsReader.get_description(description)
        image = NewsReader.get_image(description)

        # TODO: deal with image indexing
        image_link = image[0]
        image_text = image[1]

        return text, image_link, image_text

    @staticmethod
    def get_description(description):
        """
        Remove all tags from raw description and
        return just simple news description

        :param description: news description
        :return: processed description
        """

        try:
            node = html.fromstring(description)
        except etree.ParserError:
            return ''

        return node.text_content()

    @staticmethod
    def get_image(description):
        """
        Parse description file trying to find image
        source and description of this image

        :param description: raw news description
        :return: image source, image description
        """

        xhtml = html.fromstring(description)
        image_src = xhtml.xpath('//img/@src')
        image_description = xhtml.xpath('//img/@alt')

        if len(image_src) == 0:
            image_src = 'No image'
        else:
            image_src = image_src[0]

        if len(image_description) == 0:
            image_description = 'No image description'
        else:
            image_description = image_description[0]

        return image_src, image_description

    def news_text(self, news):
        """
        Process news in dictionary format into
        readable text

        :param news: news dictionary
        :return: readable news description
        """

        red, cyan, blue, reset = [''] * 4

        if self.colorful:
            red = Fore.RED
            cyan = Fore.CYAN
            blue = Fore.BLUE
            reset = Style.RESET_ALL

        result = "\n\tTitle: {}\n\tDate: {}\n\tLink: {}\n\n\tImage link: {}\n\t" \
                 "Image description: {}\n\tDescription: {}".format(red + news['title'] + reset,
                                                                   news['pubDate'],
                                                                   blue + news['link'] + reset,
                                                                   blue + news['imageLink'] + reset,
                                                                   cyan + news['imageDescription'] + reset,
                                                                   cyan + news['description'] + reset)

        return result

    def fancy_output(self, items):
        """
        Output readable information about news
        from items dictionary

        :return: None
        """

        logging.info(print('News feed is ready'))

        yellow, reset = [''] * 2

        if self.colorful:
            yellow = Fore.YELLOW
            reset = Style.RESET_ALL

        for key, value in items.items():
            if key == 'title':
                print(f'Feed: {value}')
            elif key != 'title_image':
                print(self.news_text(value))

            print(yellow + '_' * 100 + reset)

    @staticmethod
    def to_json(items):
        """
        Convert self.items (all news description)
        into json format

        :return: json format news
        """

        logging.info('Json was created')

        json_result = json.dumps(items)

        return json_result


def get_items(news, date):
    """
    If date is not Null read data from
    sql database, else return simple python dictionary

    :param news: NewsReader class
    :param date: given data (if there is one)
    :return:
    """

    if date:
        items = news.read_by_date_sql(date)
    else:
        items = news.items

    return items


def get_parser():
    """
    Creates parser using argparse module

    :return: args from CLI
    """

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')

    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', help='Print version info', action='store_true')
    parser.add_argument('--json', help='Print result as json in stdout', action='store_true')
    parser.add_argument('--verbose', help='Output verbose status messages', action='store_true')
    parser.add_argument('--caching', help='Cache news if chosen', action='store_true')
    parser.add_argument('--colorful', help='Colorize output', action='store_true')

    # TODO: add flags to output logs
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')
    parser.add_argument('--date', type=int, help='Reads cashed news by date. And output them')

    parser.add_argument('--to-pdf', type=str,
                        help='Read rss by url and write it into pdf. Print file name as input')
    parser.add_argument('--to-html', type=str,
                        help='Read rss by url and write it into html. Print file name as input')
    parser.add_argument('--to-fb2', type=str,
                        help='Read rss by url and write it into fb2. Print file name as input')

    args = parser.parse_args()

    return args


def main_logic(args):
    """
    Depending on arguments use NewsReader class

    :param args: arguments from CLI
    :return:
    """

    if args.version:
        print(PROJECT_VERSION)
        print(PROJECT_DESCRIPTION)

    if args.verbose:
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
                            level=logging.DEBUG)

    news = NewsReader(url=args.source,
                      limit=args.limit,
                      caching=args.caching,
                      colorful=args.colorful)
    news.add_news()

    items = get_items(news, args.date)

    if args.json:

        print(news.to_json(items=items))
    elif args.to_pdf:

        pdf = PdfNewsConverter(items)
        pdf.add_all_news()
        pdf.output(args.to_pdf, 'F')
    elif args.to_html:

        html_converter = HTMLNewsConverter(items)
        html_converter.output(args.to_html)
    elif args.to_fb2:
        fb2_converter = FB2NewsConverter(items)
        fb2_converter.output(args.to_fb2)
    else:
        news.fancy_output(items)


def main():
    args = get_parser()

    main_logic(args)


if __name__ == '__main__':
    main()
