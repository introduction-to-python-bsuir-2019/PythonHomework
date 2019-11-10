import feedparser
from bs4 import BeautifulSoup


class RssReader():

    def __init__(self, url, limit=None):
        self.url = url
        self.feeds = feedparser.parse(url)
        self.tags = ['title', 'published', 'pubDate', 'link', 'date']
        self.list_of_news = []
        self.limit = limit


    def print_date(self, news):
        """print date"""
        if news.get('published') != 'Unknown':
            print('Date:', news['published'])
        elif news.get('pubDate') != 'Unknown':
            print('Date:', news['pubDate'])
        elif news.get('date') != 'Unknown':
            print('Date:', news['date'])
        else print('Date: unknown')


    def print_news(self):
        """print news"""
        self.make_list_of_news()
        print('Feed:', self.feeds.feed.get('title'), "\n\n")

        for news in self.list_of_news:
            print('Title:', news['title'])
            self.print_date(news)
            print('Link:', news['link'], '\n')

            if news.get('text'):
                print(news['text'], '\n')

            if news.get('images'):
                print('Images:')
                for link in news['images']:
                    print(link)
                print()

            if news.get('links'):
                print('Links:')
                for link in news['links']:
                    print(link)
                print()

            print('-' * 50)


    def make_list_of_news(self):
        """Make a list of news

        type of news: dict
         """

        if self.limit == None or self.limit > len(self.feeds):
            self.limit = len(self.feeds)

        for news in self.feeds['entries'][:self.limit]:
            one_news = {}
            for tag in self.tags:
                if tag in news:
                    one_news[tag] = news[tag]
                else:
                    one_news[tag] = 'Unknown'
            one_news.update(self.read_description(news))
            self.list_of_news.append(one_news)


    def read_description(self, news)->dict:
        """Return dict with keys 'text', 'images', 'links'

        'text' value is description(str)
        'images' value is a list of images sources
        'links' value is a list of urls

        """
        soup = BeautifulSoup(news.description, features="html.parser")

        list_of_images = []
        images = soup.findAll('img')
        for image in images:
            if image.get('src'):
                list_of_images.append(image['src'])

        list_of_links = []
        for tag in soup.findAll():
            if tag.get('href'):
                list_of_links.append(tag['href'])
            if tag.get('url'):
                list_of_links.append(tag['url'])

        return {'text': soup.text,'images': list_of_images, 'links': list_of_links}
