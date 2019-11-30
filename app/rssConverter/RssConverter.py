import feedparser
from bs4 import BeautifulSoup
from app.rssConverter.New import New
from app.rssConverter.Exeptions import RssGetError


class RssConverter:
    """Class for getting and parsing news from internet"""

    def __init__(self):
        self.tags = ['link', 'title', 'pubDate', 'published', ]

    def get_news(self, url):
        """Getting new from internet"""
        result = feedparser.parse(url)
        if result.bozo == 0 and result.status == 200:
            return result['entries']
        else:
            raise RssGetError("url")

    def parse_news(self, dict_list):
        """Parsing news to list"""
        news_list = []
        for dictionary in dict_list:
            new = New()
            soup = BeautifulSoup(dictionary.get('summary', None), 'html.parser')
            image = soup.find('img')
            src = image.get('src', 'Unknown')
            if src:
                new.items['images'] = src
            else:
                new.items['images'] = None
            new.items['summary'] = soup.text
            new.items['links'] = [link['href'] for link in soup.find_all('a') if link.get('href', None)]
            for key in self.tags:
                new.items[key] = dictionary.get(key, 'Unknown')
            news_list.append(new)
        return news_list
