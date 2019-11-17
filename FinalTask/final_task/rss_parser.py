import feedparser
from bs4 import BeautifulSoup
from collections import namedtuple


class RssParser():
    """
    Class to parse RSS-news
    """
    def __init__(self, url, limit):
        self.url = url
        self.limit = limit
        self.feed = ''
        self.news = []

    def parse_rss(self):
        rss_feed = feedparser.parse(self.url)
        self.feed = rss_feed['feed']['title']
        if self.limit > 0:
            entries = rss_feed.entries[:self.limit]
        else:
            entries = rss_feed.entries
        for entry in entries:
            title = entry.get('title')
            date = entry.get('published')
            link = entry.get('link')
            links = []
            link_data = namedtuple('link', 'id url type')
            link_id = 0
            for entry_link in entry.get('links'):
                link_url = entry_link['url']
                my_link = link_data(link_id, link_url, 'link')
                links.append(my_link)
                link_id += 1
            soup = BeautifulSoup(entry['summary_detail']['value'], features='html.parser')
            description = soup.text
            image_data = namedtuple('image', 'alt url')
            link_id = len(links)
            for entry_image in soup.findAll('img'):
                image_alt = entry_image['alt']
                image_url = entry_image['src']
                my_image = image_data(image_alt, image_url)
                my_link = link_data(link_id, my_image, 'image')
                links.append(my_link)
                link_id += 1
            article = namedtuple('article', 'title date link description links')
            my_article = article(title, date, link, description, links)
            self.news.append(my_article)
        result = ''
        result += f'\nFeed: {self.feed}\n\n'
        for news in self.news:
            result += f'Title: {news.title}\nDate: {news.date}\nLink: {news.link}\n\n'
            for l in news.links:
                if l.type == 'image':
                    result += f'[image {l.id + 1} : {l[1].alt}][{l.id + 1}]'
                    result += f'{news.description}\n\n'
            for l in news.links:
                if l.type == 'image':
                    result += f'[{l.id + 1}]: {l[1].url} ({l.type})\n'
                else:
                    result += f'[{l.id + 1}]: {l.url} ({l.type})\n'
        return result



