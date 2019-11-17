import feedparser
from bs4 import BeautifulSoup
from html import unescape
import image as image


class News:

    def __init__(self, url, count):
        self.count = count
        self.url = url
        self.feed = ''
        self.items = []

    def parse_news(self):

        data = feedparser.parse(self.url)
        if data['bozo']:
            raise ValueError("Wrong URL address or there is no access to the Internet")
        self.feed = data['feed'].get('title', None)
        entries = data['entries'] if self.count < 0 else data['entries'][:self.count]
        for entry in entries:
            title = unescape(entry.get('title', 'No title'))
            date = entry.get('published', 'Unknown')
            link = entry.get('link', 'No link')
            html = entry.get('summary', None)
            content = NewsContent.get_content_html(html)
            self.items.append(NewsItem(title, date, link, content))

    def __str__(self):
        result = f'\nFeed: {self.feed}\n\n'
        for item in self.items:
            result += str(item) + '\n\n'
        return result

    def to_json(self):

        news_items = []
        for item in self.items:
            images = [{'link': img.link, 'alt': img.alt} for img in item.content.images_links]
            links = [link for link in item.content.other_links]
            content = {'text': item.content.text, 'images': images, 'links': links}
            news_item = {'title': item.title, 'date': item.date, 'source': item.link, 'content': content}
            news_items.append(news_item)
        return {'news': {'feed': self.feed, 'items': news_items}}

    def get_count(self):
        return len(self.items)


class NewsItem:
    def __init__(self, title, date, link, content):
        self.title = title
        self.date = date
        self.link = link
        self.content = content

    def __str__(self):
        return f'Title: {self.title}\nDate: {self.date}\nLink: {self.link}\n\n{self.content}'


class NewsContent:

    def __init__(self, text, images_links, other_links):
        self.text = text
        self.images_links = images_links
        self.other_links = other_links

    @staticmethod
    def get_content_html(html):

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
