import base64
import datetime
import feedparser
import json
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image


class RSSReader:
    def __init__(self, source, limit, json, date, to_html, to_fb2):
        """
        RSSReader class constructor

        :param source: Link to the news site
        :param limit: Limit of news to print
        :param json: If the value is true, program will print news in .json format
        :param date: String param to print news by date from cache
        :param to_html: Path to save news in .html file
        :param to_fb2: Path to save news in .fb2 file
        """
        self.source = source
        self.limit = limit
        self.json = json
        self.date = date
        self.to_html = to_html
        self.to_fb2 = to_fb2
        self.feeds = {}

    def parse_source(self):
        """
        Main method to call all another class methods

        :return: Nothing to return
        """
        d = feedparser.parse(self.source)  # Parse rss from given source
        if not self.limit:
            self.limit = 1

        self.feeds['news'] = []
        channel = d['channel']['title']

        for news in d['entries'][0:self.limit]:
            self.feeds['news'].append(self.read_news(news, channel))

        # Method calls
        if not self.date and not self.to_html and not self.to_fb2:
            self.print_feeds(self.feeds['news'])
            self.to_cache()
        elif self.date:
            try:
                self.from_cache()
            except FileNotFoundError:
                print("No news in cache it doesn't exist. Relax and parse some news. They will appear in cache soon :)")
            except IndexError:
                print("No news by that date")
        elif self.to_html:
            try:
                self.convert_to_html(self.feeds['news'])
                self.to_cache()
            except FileNotFoundError:
                print('Incorrect file path. Please use something like: "D:/somedict/somedict" or "D:" or "."')
        elif self.to_fb2:
            try:
                self.convert_to_fb2(self.feeds['news'])
                self.to_cache()
            except FileNotFoundError:
                print('Incorrect file path. Please use something like: "D:/somedict/somedict" or "D:" or "."')

    @staticmethod
    def read_news(news, channel):
        """
        Method to get dict object with news, that we need

        :param news: Current parsing news
        :param channel: Feed, where did the news come from
        :return: Dictionary with parsed news
        """
        item = dict()

        # Create new dict keys and give them values
        item['feed_name'] = channel
        item['title'] = news['title'].replace('&#39;', "'")
        item['date'] = news['published']
        item['link'] = news['link']

        soup = BeautifulSoup(news['summary'], 'html.parser')

        item['image_title'] = soup.find('img')['title']
        description = soup.p.contents[-2]

        # If there no image description we will write about that
        if str(description)[0] == '<':
            item['image_description'] = 'No image description'
        else:
            item['image_description'] = description

        # If there no image in news we will write about that
        if soup.find('img')['src'] == "":
            item['image_link'] = 'No image link'
        else:
            item['image_link'] = soup.find('img')['src']

        return item

    def to_cache(self):
        """
        Method to cache your parsed news

        It create a new cache.json file and store your parsed news

        :return: Nothing to return
        """
        with open('./cache.json', 'w+') as f:
            try:
                feeds_f = json.load(f)
            except Exception:
                feeds_f = {'news': []}
            for item in self.feeds['news']:
                if item not in feeds_f['news']:
                    feeds_f['news'].append(item)

        if feeds_f['news'][0].get('title') == '':
            del feeds_f['news'][0]

        with open('./cache.json', 'w+') as f:
            json.dump(feeds_f, f, indent=1)

    def from_cache(self):
        """
        Method, that load news by given date from cache

        :return: Nothing to return
        """
        to_print = []
        with open('./cache.json', 'r') as f:
            feeds_f = json.load(f)

            for item in feeds_f['news']:
                item_date = datetime.datetime.strptime(item['date'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')
                if self.date == item_date:
                    to_print.append(item)

            self.print_feeds(to_print)

    def convert_to_html(self, convert):
        """
        Convert given news to .html format

        :param convert: List of news to convert
        :return: Nothing to return
        """
        html_string = '<!DOCTYPE html><html><head>RSSFeed</head><body>'
        for item in convert:
            html_string += f'<p>{item["feed_name"]}</p>'
            html_string += f'<p>{item["title"]}</p>'
            html_string += f'<p>{item["date"]}</p>'
            html_string += f'<a href="{item["link"]}">Original feed</a><br>'
            html_string += f'<p>{item["image_title"]}</p>'
            html_string += f'<p>{item["image_description"]}</p>'
            html_string += f'<img src="{item["image_link"]}"><br><br>'
        html_string += '</body></html>'

        with open(f'{self.to_html}/html_news.html', 'w') as f:
            f.write(html_string)
            print(f"Your news are successfully save to {self.to_html}/html_news.html file")

    def convert_to_fb2(self, convert):
        """
        Convert given news to .fb2 format

        :param convert: List of news to convert
        :return: Nothing to return
        """
        fb2_string = f'<?xml version="1.0" encoding="UTF-8"?>' \
            f'<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">' \
            f'<description>' \
            f'<title-info>' \
            f'<genre>antique</genre>' \
            f'<author><first-name></first-name><last-name>Unknown</last-name></author>' \
            f'<book-title>99ae0c9b60239ce04eded964c2dd198d</book-title>' \
            f'<lang>en</lang>' \
            f'</title-info>' \
            f'<document-info>' \
            f'<author><first-name></first-name><last-name>Unknown</last-name></author>' \
            f'<program-used>calibre 4.4.0</program-used>' \
            f'<date>1.12.2019</date>' \
            f'<id>6ad0484e-3669-44b5-bda1-78ddac516e9b</id>' \
            f'<version>1.0</version>' \
            f'</document-info>' \
            f'<publish-info>' \
            f'</publish-info>' \
            f'</description>' \
            f'<body>' \
            f'<section>'
        imgs_base64 = []
        i = 0
        for item in convert:
            fb2_string += f'<p>Feed name: {item["feed_name"]}</p>'
            fb2_string += f'<p>Title: {item["title"]}</p>'
            fb2_string += f'<p>Original feed link: {item["link"]}</p>'
            fb2_string += f'<p>News date: {item["date"]}</p>'
            fb2_string += f'<p>Image title: {item["image_title"]}</p>'
            fb2_string += f'<p>Image description: {item["image_description"]}</p>'

            # Get 64base image
            if item["image_link"] != 'No image link':
                fb2_string += f'<p><image l:href="#img_{i}"/></p>'
                response = requests.get(item["image_link"])
                img_file = Image.open(BytesIO(response.content))
                buffered = BytesIO()
                try:
                    img_file.save(buffered, format="JPEG")
                    img_str = str(base64.b64encode(buffered.getvalue()))
                    imgs_base64.append(img_str[2:-1])
                except Exception:
                    imgs_base64.append('No image here')
                i += 1

        fb2_string += '<empty-line/></section></body>'

        i = 0
        for item in imgs_base64:
            fb2_string += f'<binary id="img_{i}" content-type="image/jpeg">{item}</binary>'
            i += 1

        fb2_string += '</FictionBook>'

        with open(f'{self.to_fb2}/fb2_news.fb2', 'w') as f:
            f.write(fb2_string)
            print(f"Your news are successfully save to {self.to_fb2}/fb2_news.fb2 file")

    def print_feeds(self, to_print):
        """
        Print given news to console

        :param to_print: List of news to print
        :return: Nothing to return
        """
        if self.json:
            print(json.dumps(self.feeds, indent=1))
        else:
            print()
            print('Feed:', to_print[0].get('feed_name'))
            print('-' * 40)
            for item in to_print:
                print('Title:', item['title'])
                print('Date:', item['date'])
                print('Link:', item['link'])
                print()
                print('Image title:', item['image_title'])
                print('Image description:', item['image_description'])
                print('Image link:', item['image_link'])
                print('-' * 40)
