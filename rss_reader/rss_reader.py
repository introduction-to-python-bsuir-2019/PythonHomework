import argparse
import feedparser
import logging
import html
import json
import urllib
import colorama
from base64 import b64encode
from pathlib import Path
from bs4 import BeautifulSoup
from rss_reader import version as vers


class Converter:
    """This class is used to convert news feed to either html or fb2 version"""

    def __init__(self, news_feed):
        """
        Constructor of Converter class. It assigns encoding value additionally
        :param NewsFeed news_feed: A NewsFeed object that contains news feed
        """

        self.news_feed = news_feed
        self.encoding = self.news_feed.items[0].encoding

    def convert_to_html(self, path, limit, date):
        """
        This function creates a html file with news feed

        :param str path: The path where new file will be saved
        :param int limit: The number of news to be saved
        :param str date: Optional: if exists than resulting html file will only contain news from specific date
        """

        logging.info('Converting to html')
        path_object = Path(path)
        path_object.mkdir(parents=True, exist_ok=True)
        path_object /= 'news feed.html'
        with path_object.open('w', encoding="utf-8") as html_file:
            html_file.write(self.create_html(limit, date))

        logging.info('Converting to html successful')

    def convert_to_fb2(self, path, limit):
        """
        This function creates a fb2 file with news feed

        :param str path: The path where new file will be saved
        :param int limit: The number of news to be saved
        """

        logging.info('Converting to fb2')
        path_object = Path(path)
        path_object.mkdir(parents=True, exist_ok=True)
        path_object /= 'news feed.fb2'
        with path_object.open('w', encoding=self.encoding) as fb2_file:
            fb2_file.write(self.create_fb2(limit))

        logging.info('Converting to fb2 successful')

    def create_html(self, limit, date):
        """
        This function creates a html version of news feed

        :param int limit: The number of news to be created
        :param str date: Optional: if exists than resulting html implementation will contain news from specific date
        :return: a html like news feed
        :rtype: str
        """

        logging.info('Creating html text')
        limit = checking_limit(limit, self.news_feed.items)
        news = '\n'.join([item.create_div(date) for item in self.news_feed.items[:limit]])  # ????

        return """
           <html>
               <head><meta charset="utf-8"></head>
               <body>
                   <p>News Feed</p>
                   {0}
               </body>
           </html>
           """.format(news)

    def create_fb2(self, limit):
        """
        This function creates a fb2 version of news feed

        :param int limit: The number of news to be created
        :return: a fb2 like news feed
        :rtype: str
        """

        logging.info('Creating fb2 text')
        limit = checking_limit(limit, self.news_feed.items)
        news = ''.join([item.create_section() for item in self.news_feed.items[:limit]])
        binaries = ''.join([item.create_binary() for item in self.news_feed.items[:limit]])

        return """<?xml version="1.0" encoding="{encoding}"?>
           <FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
               <description>
                   <title-info>
                       <genre>newspapers</genre>
                       <book-title>RSS Reader</book-title>
                       <author><nickname>el0ny</nickname></author>
                   </title-info>
                   <document-info>
                       <program-used>{myprog}</program-used>
                       <version>{vers}</version>
                   </document-info>
               </description>
               <body>
                   {news}
               </body>
               {binaries}
           </FictionBook>
           """.format(myprog=__name__, vers=vers.__version__,
                      news=news, encoding=self.encoding,
                      binaries=binaries)


class NewsFeed:
    """Base class for news feed"""

    def __init__(self, feed_title, items):
        """
        This constructor only initializes two values, nothing else

        :param str feed_title: The title of news feed
        :param list items: A list of Item objects, basically, a list of news
        """

        self.feed_title = feed_title
        self.items = items

    def print_feed(self, _json, limit, colorize):
        """
        This function allows to print news in cmd either in json or str format

        :param colorize: If true than colorize the output in cmd
        :param bool _json: If true than the news will be in json format, otherwise in str format
        :param int limit: The number of news to be printed
        """

        limit = checking_limit(limit, self.items)
        if _json:
            self.print_to_json(limit)
        else:
            self.print_to_console(limit, colorize)

    def create_json(self, is_cached, limit):
        """
        This function allows to create json like dict of news

        :param bool is_cached: If true then json will be ready to be saved, otherwise, to be printed
        :param int limit: The number of news to be printed
        :return: A json like dict of news
        :rtype: dict
        """

        return {'Feed': self.feed_title, 'Items': [item.return_item(is_cached) for item in self.items[:limit]]}

    def print_to_json(self, limit):
        """
        This function allows to print news in cmd in json format

        :param int limit: The number of news to be printed
        """

        logging.info('Printing news in json format')
        print(json.dumps(self.create_json(0, limit)))

    def print_to_console(self, limit, colorize):
        """
        This function allows to print news in cmd in str format

        :param colorize: If true than colorize the output in cmd
        :param int limit: The number of news to be printed
        """

        logging.info('Printing news in console format')
        print('Feed: {0}'.format(self.feed_title))
        for item in self.items[:limit]:
            item.print_to_console(colorize)
        logging.info('Printed %s news', limit)

    def save_news(self, limit):
        """
        This function allows to save news in a json file in homedirectory/rss_reader_cache/cache.json

        :param int limit: The number of news to be saved
        """
        logging.info('Saving news')
        news_to_save = self.create_json(1, limit)['Items']
        existing_news = load_from_cache()
        news_to_save += [item for item in existing_news if item not in news_to_save]
        path = Path.home().joinpath('rss_reader_cache')
        cache_file = "cache.json"
        path.mkdir(parents=True, exist_ok=True)
        filepath = path / cache_file
        with filepath.open('w') as json_file:
            json.dump(news_to_save, json_file)
        logging.info('Saving news successful')


class Item:
    """
    Class for single news item from news feed
    Attributes of the class can vary depend on if this item is created from loading from cache, or from parsed feed
    They are:
        str title          News title
        str pubDate        Published date in it's original form
        str link           Link to the news
        str description    Description of the news
        dict links         A dict with href, image, video links
        str date_string    (optional: only from cache) Published date in YYYYMMDD format
        str source         (optional: only from cache) Rss source
        str encoding       (optional: only from cache) Encoding of the news
    """
    def __init__(self, news_dict):
        for key in news_dict:
            setattr(self, key, news_dict[key])

    def print_to_console(self, colorize):
        """
        This function allows to print one news item in console

        :param colorize: If true than colorize the output in cmd
        """
        title_color = ''
        date_color = ''
        link_color = ''
        description_color = ''
        href_color = ''
        image_color = ''
        video_color = ''
        divider_color = ''
        if colorize:
            colorama.init(autoreset=True)
            title_color = colorama.Fore.MAGENTA
            date_color = colorama.Fore.WHITE
            link_color = colorama.Fore.LIGHTBLACK_EX
            description_color = colorama.Fore.LIGHTYELLOW_EX + colorama.Back.BLACK
            href_color = colorama.Fore.GREEN
            image_color = colorama.Fore.LIGHTGREEN_EX
            video_color = colorama.Fore.CYAN
            divider_color = colorama.Fore.LIGHTWHITE_EX + colorama.Back.LIGHTWHITE_EX
        print(colorama.Fore.GREEN)
        print(title_color + '\nTitle: {0}'.format(self.title))
        print(date_color + 'Date: {0}'.format(self.pubDate))
        print(link_color + 'Link: {0} \n'.format(self.link))
        print(description_color + self.description)
        print()

        if self.links['href_links']:
            print(href_color + '\nLinks:')
            for link in self.links['href_links']:
                print(href_color + link)

        if self.links['images_links']:
            print(image_color + '\nImages:')
            for link in self.links['images_links']:
                print(image_color + link)

        if self.links['video_links']:
            print(video_color + '\nVideos:')
            for link in self.links['video_links']:
                print(video_color + link)

        print(divider_color + '\n//////////////////////////////////////////////////////////////////////////')

    def create_div(self, date):
        """
        This function creates a div block of news needed for html convertation

        :param str date: Optional: if exists than resulting div implementation will only contain news from specific date
        :return: A string representation of div block of news
        :rtype: str
        """

        return """
           <div>
               <h3>{title}</h3>
               <em>{pubDate}</em>
               <p></p>
               <p>{description}</p>
               <a href="{link}">Read More</a>
               <p><br clear="all"></p>
           </div>
           """.format(title=html.escape(self.title), pubDate=self.pubDate,
                      description=self.insert_hrefs(self.description, date), link=self.link)

    def create_section(self):
        """
        This function creates a section block of news needed for fb2 convertation

        :return: A string representation of section block of news
        :rtype: str
        """

        logging.info('Creating section')
        description = html.escape(self.description)
        return """
            <section>
                <title><p>{title}</p></title>
                <p><emphasis>{pubDate}</emphasis></p>
                <p>{description}</p>
            </section>
            """.format(title=html.escape(self.title), pubDate=self.pubDate,
                       description=self.insert_hrefs_fb2(self.description))

    def insert_hrefs(self, description, date):
        """
        This function inserts href links in description needed for html convertation

        :param str description: The original description of news
        :param str date: Optional: if exists than resulting description will only contain news from specific date
        :return: A description with inserted href links
        :rtype: str
        """

        description = self.insert_images(html.escape(description), date)
        description = self.insert_videos(description)
        for href_link in self.links['href_links']:
            href_raw = description[description.find(' [link '):description.find(']', description.find(' [link '))+1]
            href_content = href_raw[href_raw.find(' | ')+3:len(href_raw)-1]
            href_html = '<a href="{href}">{content}</a>'.format(href=href_link[href_link.find(': ')+2:],
                                                                content=href_content)
            description = description.replace(href_raw, href_html)
        logging.info('href inserted')
        return description

    def insert_images(self, description, date):
        """
        This function inserts images in description needed for html convertation

        :param str description: The original description of news
        :param str date: Optional: if exists than resulting description will only contain news from specific date
        :return: A description with inserted image links
        :rtype: str
        """
        logging.info('Image inserted')
        for image_link in self.links['images_links']:
            image_raw = description[description.find(' [image '):description.find(']', description.find(' [image '))+1]
            image_alt = image_raw[image_raw.find(' | ') + 3:len(image_raw) - 1]
            source = image_link[image_link.find(': ') + 2:]
            if date:
                image_name = source.split('/')[-1]
                image_name = image_name.translate(str.maketrans('', '', '.?><"*:|')) + '.jpg'
                path = Path.home().joinpath('rss_reader_cache/image')
                source = path / image_name
            image_html = '<img src="{src}" alt="{alt}" align = "left">'.format(src=source, alt=image_alt)
            description = description.replace(image_raw, image_html)
        return description

    def insert_videos(self, description):
        """
        This function inserts video links in description needed for html convertation
        (I thought that I can convert them into full videos, but then I realised that it was a bad idea,
        so I decided to just keep that part, although it isn't necessary anymore

        :param str description: The original description of news
        :param str date: Optional: if exists than resulting description will only contain news from specific date
        :return: A description with inserted video links
        :rtype: str
        """
        logging.info('Video inserted')
        for video_link in self.links['video_links']:
            video_href = description[description.find(' [video '):description.find(']', description.find(' [video '))+1]
            logging.info(video_href)
            source = video_link[video_link.find(': ') + 2:]
            image_html = '<a href="{src}">{content}</a>'.format(src=source, content=video_href[1:])
            description = description.replace(video_href, image_html)
        return description

    def create_binary(self):
        """
        This function creates a <binary> with b64 images needed for fb2 convertation

        :return: A string in <binary> format with images inside
        """

        logging.info('Creating binaries')
        binaries = ''
        if not self.links['images_links']:
            return ''
        for image_link in self.links['images_links']:
            source = image_link[image_link.find(': ') + 2:]
            image_name = source.split('/')[-1]
            if source == '':
                image_name = '.jpg'
                encoded_string = '/9j/4AAQSkZJRgABAQEAXgBeAAD/4RpwRXhpZgAATU0AKgAAAAgABgALAAIAAAAmAAAIYgESAAMAAAABAAEAAAExAAIAAAAmAAAIiAEyAAIAAAAUAAAIrodpAAQAAAABAAAIwuocAAcAAAgMAAAAVgAAEUYc6gAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFdpbmRvd3MgUGhvdG8gRWRpdG9yIDEwLjAuMTAwMTEuMTYzODQAV2luZG93cyBQaG90byBFZGl0b3IgMTAuMC4xMDAxMS4xNjM4NAAyMDE5OjExOjMwIDE0OjQ2OjAyAAAGkAMAAgAAABQAABEckAQAAgAAABQAABEwkpEAAgAAAAMwMQAAkpIAAgAAAAMwMQAAoAEAAwAAAAEAAQAA6hwABwAACAwAAAkQAAAAABzqAAAACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMjAxOToxMTozMCAxNDo0MTo1MQAyMDE5OjExOjMwIDE0OjQxOjUxAAAAAAYBAwADAAAAAQAGAAABGgAFAAAAAQAAEZQBGwAFAAAAAQAAEZwBKAADAAAAAQAC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MTE8L3htcDpDcmVhdGVEYXRlPjwvcmRmOkRlc2NyaXB0aW9uPjwvcmRmOlJERj48L3g6eG1wbWV0YT4NCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDw/eHBhY2tldCBlbmQ9J3cnPz7/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8QEBD/wAALCABWAFYBAREA/8QAHAAAAwADAQEBAAAAAAAAAAAABAUGAgMHAQgA/8QAOxAAAQMDAgMFBQYDCQAAAAAAAQIDBAAFEQYhBxIxEyJBUWEIMkJxgRQVFiNSwZKhsRckcoKRotHS8P/aAAgBAQAAPwD6O3Ua3NMc2+KPYiZxtR7UDPhRSLcfKs/u75f6VqctxA6UI9Bx4Uvfi48KBcZ5TsKw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'
            else:
                logging.info('Image name %s', image_name)
                image_name = image_name.translate(str.maketrans('', '', '.?><"*:|')) + '.jpg'
                path = Path.home().joinpath('rss_reader_cache/image')
                source = path / image_name
                with open(source, "rb") as image_file:
                    encoded_string = b64encode(image_file.read()).decode()

            binaries += '<binary id="{src}" content-type="image/jpeg">{data}</binary>'\
                .format(src=image_name, data=encoded_string)
        return binaries

    def insert_hrefs_fb2(self, description):
        """
        This function allows find and insert links into description
        (That is also a rudimental function. Originally I wanted to make hrefs to web links, which are stored as
        notes. But something went wrong and not all rss were working correctly. So now it just makes links that are
        empty)

        :param str description: Were to find those hrefs
        :return: Resulting description with inserted href links
        :rtype: str
        """

        logging.info('href inserted')
        description = self.insert_images_fb2(html.escape(description))
        for href_link in self.links['href_links']:
            href_raw = description[description.find(' [link '):description.find(']', description.find(' [link '))+1]
            href_content = href_raw[href_raw.find(' | ')+3:len(href_raw)-1]
            href_fb2 = '<a l:href="#{href}">{content}</a>'.format(href=href_link[href_link.find(': ')+2:],
                                                                  content=href_content)
            description = description.replace(href_raw, href_fb2)
        return description

    def insert_images_fb2(self, description):
        """
        This function allows find and insert links to images into description

        :param str description: Were to find those images
        :return: Resulting description with inserted image links
        :rtype: str
        """
        logging.info('Image inserted')
        for image_link in self.links['images_links']:
            image_raw = description[description.find(' [image '):description.find(']', description.find(' [image '))+1]
            image_alt = image_raw[image_raw.find(' | ') + 3:len(image_raw) - 1]
            source = image_link[image_link.find(': ') + 2:]
            image_name = source.split('/')[-1]
            image_name = image_name.translate(str.maketrans('', '', '.?><"*:|')) + '.jpg'
            image_html = '<image l:href="#{src}" alt="{alt}"/>'.format(src=image_name, alt=image_alt)
            description = description.replace(image_raw, image_html)
        return description

    def return_item(self, is_cached):
        """
        This function returns the content of this object as a dict

        :param bool is_cached: If true than the result dict will be able to be cached
        :return: A dict with this object's content
        :rtype: dict
        """

        item_content = {'title': self.title, 'description': self.description,
                        'link': self.link, 'pubDate': self.pubDate, 'links': self.links}
        if is_cached:
            item_content['date_string'] = self.date_string
            item_content['source'] = self.source
            item_content['encoding'] = self.encoding
        return item_content


def set_argparse():
    """
    This function allows to get needed parameters from command line

    :return: An object with all needed parameters inside
    """

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', action='version', version='%(prog)s v'+vers.__version__,
                        help='Prints version info')
    parser.add_argument('--json', action='store_true', help='Prints result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=-1, help='Limits news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='Shows news of specific date')
    parser.add_argument('--to-html', dest='to_html', type=str,
                        help='Converts news into html format and save to a specified path')
    parser.add_argument('--to-fb2', dest='to_fb2', type=str,
                        help='Converts news into fb2 format and save to a specified path')
    parser.add_argument('--colorize', action='store_true', help='Colorizes the cmd output')
    return parser.parse_args()


def find_images(soup):
    """
    This function allows to extract <img> image links from parsed feed

    :param bs4.BeautifulSoup soup: A beautifulsoup representation of parsed news feed
    :return: A list of found image links
    :rtype: list
    """

    logging.info('Starting image finding')
    image_iterator = 0
    images_links = []

    for img in soup.findAll('img'):

        image_iterator += 1
        if 'alt' in img.attrs and img['alt'] != '':
            replaced_data = ' [image {0} | {1}] '.format(image_iterator, img['alt'])
        else:
            replaced_data = ' [image {0}]'.format(image_iterator)
        src = img['src']

        if src != '':
            image_name = src.split('/')[-1]
            image_name = image_name.translate(str.maketrans('', '', '.?><"*:|')) + '.jpg'
            path = Path.home().joinpath('rss_reader_cache/image')
            path.mkdir(parents=True, exist_ok=True)
            filepath = path / image_name
            if filepath.is_file():
                logging.info('Image already exists')
            else:
                urllib.request.urlretrieve(src, filepath)
        images_links.append('[{0}]: {1}'.format(image_iterator, src))
        soup.find('img').replace_with(replaced_data)

    logging.info('Image finding finished. Found %s images', image_iterator)
    return images_links


def find_href(soup):
    """
    This function allows to extract <a> href links from parsed feed

    :param bs4.BeautifulSoup soup: A beautifulsoup representation of parsed news feed
    :return: A list of found href links
    :rtype: list
    """

    logging.info('Starting link finding')
    href_iterator = 0
    href_links = []
    for href in soup.findAll('a'):
        if 'href' in href.attrs:
            href_iterator += 1
            link = href['href']
            if href.text != '':
                replaced_data = ' [link {0} | {1}] '.format(href_iterator, href.text)
            else:
                replaced_data = ' [link {0}] '.format(href_iterator)
            href_links.append('[{0}]: {1}'.format(href_iterator, link))
            href.replace_with(replaced_data)
    logging.info('Link finding finished. Found %s links', href_iterator)
    return href_links


def find_videos(soup):
    """
    This function allows to extract <iframe> video links from parsed feed

    :param bs4.BeautifulSoup soup: A beautifulsoup representation of parsed news feed
    :return: A list of found video links
    :rtype: list
    """

    logging.info('Starting video finding')
    video_iterator = 0
    video_links = []
    for video in soup.findAll('iframe'):
        if 'src' in video.attrs:
            video_iterator += 1
            link = video['src']
            replaced_data = ' [video {0}] '.format(video_iterator)
            video_links.append('[{0}]: {1}'.format(video_iterator, link))
            soup.find('iframe').replace_with(replaced_data)
    logging.info('Video finding finished. Found %s videos', video_iterator)
    return video_links


def read_from_cache(date, source):
    """
    This function allows to read news from cashed json file and convert them into list of Item objects

    :param str date: Only news from this date will be loaded
    :param str source: Only news from this source will be loaded
    :return: A list of Item object with news inside
    :rtype: list
    """

    cached_news = load_from_cache()
    dated_news = []
    for news in cached_news:
        if news['source'] == source and news['date_string'] == date:
            dated_news.append(Item(news))
    return dated_news


def load_from_cache():
    """
    This function allows to load news from cashed json file in a list of dicts format

    :return: The loaded news
    :rtype: list
    """

    logging.info('Loading from cache')
    cached_news = []
    filepath = Path.home().joinpath('rss_reader_cache') / "cache.json"
    if filepath.is_file():
        with filepath.open() as cache:
            data = cache.read()
            cached_news = json.loads(data)
    logging.info('Loaded %s news', len(cached_news))
    return cached_news


def checking_limit(limit, items):
    """
    This function allows to check if limit is valid

    :param int limit: The checked limit
    :param list items: A list of Item news that is used to extract length of it
    :return: A valid limit
    :rtype: int
    """

    if limit > len(items) or limit < 0:
        limit = len(items)
    return limit


def main():
    try:
        args = set_argparse()
        if args.verbose:
            logging.basicConfig(format='%(asctime)s %(funcName)s %(message)s', datefmt='%I:%M:%S', level=logging.DEBUG)
        logging.info('Application started. RSS source is %s', args.source)
        args.source = args.source.rstrip('/')
        if args.date:
            news = read_from_cache(args.date, args.source)
            if not news:
                raise Exception('The are no news of {0} from {1} stored'.format(args.source, args.date))
            news_feed = NewsFeed('Cached news', news)
        else:
            parsed_feed = feedparser.parse(args.source)
            if parsed_feed.bozo == 1:
                raise Exception('The feed is not well-formed XML. Details are {0}'.format(parsed_feed.bozo_exception))
            news = []
            logging.info('Begin processing each news')
            for i in range(len(parsed_feed.entries)):
                logging.info('Parsing news number %s', i + 1)
                entry = parsed_feed.entries[i]
                soup = html.unescape(BeautifulSoup(entry['summary'], 'html.parser'))
                images_links = find_images(soup)
                href_links = find_href(soup)
                video_links = find_videos(soup)
                links = {'images_links': images_links, 'href_links': href_links, 'video_links': video_links}
                date_string = ''.join(map(str, entry.published_parsed[:3]))
                dict_news = {'title': html.unescape(entry['title']), 'pubDate': entry['published'],
                             'link': entry['link'], 'description': html.unescape(soup.text), 'links': links,
                             'date_string': date_string, 'source': args.source, 'encoding': parsed_feed.encoding}
                news.append(Item(dict_news))
                logging.info('News number %s has parsed', i + 1)
            news_feed = NewsFeed(parsed_feed.feed.title, news)
            news_feed.save_news(len(parsed_feed.entries))
        if args.to_html:
            Converter(news_feed).convert_to_html(args.to_html, args.limit, args.date)
        elif args.to_fb2:
            Converter(news_feed).convert_to_fb2(args.to_fb2, args.limit)
        else:
            news_feed.print_feed(args.json, args.limit, args.colorize)
        logging.info('Application completed')

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
