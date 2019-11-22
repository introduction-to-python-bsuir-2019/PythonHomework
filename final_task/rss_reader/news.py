"""
This module contains classes for fetching and representing RSS
"""

import feedparser
import time
import rss_reader.news_date as news_date
import rss_reader.image as image
from bs4 import BeautifulSoup
from html import unescape


class News:

    """
    This class represents news collection
    """

    def __init__(self, source, count=-1):
        self.count = count
        self.source = source
        self.feed = ''
        self.items = []

    def parse_news(self):
        """
        This method gets and parses RSS
        :return: list of NewsItem instances
        """
        data = feedparser.parse(self.source)
        if data['bozo']:
            raise ValueError("Wrong URL address or there is no access to the Internet")
        self.feed = data['feed'].get('title', None)
        entries = data['entries'] if self.count < 0 else data['entries'][:self.count]
        for entry in entries:
            title = unescape(entry.get('title', 'No title'))
            date = entry.get('published_parsed') or entry.get('updated_parsed') or news_date.get_current_date_tuple()
            link = entry.get('link', 'No link')
            html = entry.get('summary', None)
            content = NewsContent.get_content_from_html(html)
            self.items.append(NewsItem(title, date, link, content))
        return self.items

    def __str__(self):
        result = f'\nFeed: {self.feed}\n\n'
        for item in self.items:
            result += str(item) + '\n\n'
        return result

    def to_json(self):
        """
        This method converts News object to JSON format
        :return: dict
        """
        json_news_items = [item.to_json() for item in self.items]
        return {'news': {'feed': self.feed, 'items': json_news_items}, 'source': self.source}

    @staticmethod
    def from_json(json_object):
        """
        This method gets news from JSON object
        :param json_object: news in JSON format
        :return: News object
        """
        if json_object:
            json_news = json_object.get('news', None)
            if json_news:
                news = News(json_news.get('source', ''))
                news.items = [NewsItem.from_json(item) for item in json_news.get('items', [])]
                news.feed = json_news.get('feed', '')
                return news

    def get_count(self):
        """
        This method returns count of items in News object
        :return: int
        """
        return len(self.items)


class NewsItem:

    """
    This class represents news structure
    """

    def __init__(self, title, date, link, content):
        self.title = title
        self.date = date
        self.link = link
        self.content = content

    def to_json(self):
        """
        This method converts NewsItem object to JSON format
        :return: dict
        """
        return {'title': self.title, 'date': self.date, 'source': self.link, 'content': self.content.to_json()}

    @staticmethod
    def from_json(json_obj):
        """
        This method gets NewsItem object from JSON
        :param json_obj: dict
        :return: NewsItem
        """
        if json_obj:
            return NewsItem(json_obj.get('title', ''), tuple(json_obj.get('date', [])),
                            json_obj.get('source', ''), NewsContent.from_json(json_obj.get('content')))

    def __str__(self):
        date = time.strftime("%a, %-d %b %Y %H:%M:%S %z", self.date)
        return f'Title: {self.title}\nDate: {date}\nLink: {self.link}\n\n{self.content}'


class NewsContent:
    """
    This class represent news content like text and links to images
    """
    def __init__(self, text, images_links, other_links):
        self.text = text
        self.images_links = images_links
        self.other_links = other_links

    @staticmethod
    def get_content_from_html(html):
        """
        This method provides a way to get content like images links and text from HTML-code in string format
        :param html: HTML-code in string format
        :return: NewsContent class instance
        """
        soup = BeautifulSoup(html, 'lxml')
        text = soup.text
        images_links = []
        for img in soup.find_all('img'):
            src = img.get('src', 'Unknown')
            alt = img.get('alt', '')
            if src:
                images_links.append(image.Image(src, alt))
        other_links = [link['href'] for link in soup.find_all('a') if link.get('href', None)]
        return NewsContent(text, images_links, other_links)

    def to_json(self):
        """
        This method converts NewsContent object to JSON format
        :return: dict
        """
        return {'text': self.text, 'images': [img.to_json() for img in self.images_links], 'links': self.other_links}

    @staticmethod
    def from_json(json_obj):
        """
        This method gets NewsContent object from JSON
        :param json_obj: dict
        :return: NewsContent
        """
        if json_obj:
            images = [image.Image.from_json(img_json) for img_json in json_obj.get('images', [])]
            return NewsContent(json_obj.get('text', ''), images, json_obj.get('links', []))

    def __str__(self):
        result = ''
        link_index = len(self.other_links)

        for img in self.images_links:
            link_index += 1
            result += f'[image {link_index}: {img.alt}][{link_index}]'

        result += f'{self.text}\n\n\nLinks:\n'

        link_index = 1
        for link in self.other_links:
            result += f'[{link_index}]: {link} (link)\n'
            link_index += 1

        for img in self.images_links:
            result += f'[{link_index}]: {img.link} (image)\n'
            link_index += 1

        return result
