import feedparser
from bs4 import BeautifulSoup
from app.rssConverter.New import New
from app.rssConverter.Exeptions import RssGetError, IncorrectLimit


class RssConverter:

    def __init__(self):
        self.tags = ['link', 'title', 'pubDate', 'published', ]

    def get_news(self, url):
        result = feedparser.parse(url)
        if result.bozo == 0 and result.status == 200:
            return result['entries']
        else:
            raise RssGetError("url")

    def get_limited_news(self, dict_list, limit):
        news_quantity = len(dict_list)
        if limit is None:
            limit = news_quantity
        elif limit > news_quantity:
            raise IncorrectLimit(news_quantity)
        return dict_list[:limit]

    def parse_news(self, dict_list):
        news_list = []
        for dictionary in dict_list:
            new = New()
            soup = BeautifulSoup(dictionary.get('summary', None), 'html.parser')
            new.items['images'] = []
            for image in soup.find_all('img'):
                src = image.get('src', 'Unknown')
                if src:
                    new.items['images'].append(src)
                new.items['summary'] = soup.text
            new.items['links'] = [link['href'] for link in soup.find_all('a') if link.get('href', None)]
            for key in self.tags:
                new.items[key] = dictionary.get(key, 'Unknown')
            news_list.append(new)
        return news_list

    def print_news(self, news_list, limit=None):
        news_list = self.get_limited_news(news_list, limit)
        for new in news_list:
            for key, item in new.items.items():
                if key == 'images' or key == 'links':
                    print("\n")
                    print(key)
                    for href in item:
                        print("\n")
                        print(href)
                else:
                    if item == 'Unknown' and key in ['pubDate', 'published']:
                        continue
                    print("\n")
                    print(key + '    ' + item)
            print('-----------------------------------------------------------------------------------')

    def in_json_format(self, news_list, limit):
        news_list = self.get_limited_news(news_list, limit)
        print('{')
        print('\t' + 'news:')
        print('\t' + '[')
        for new in news_list:
            print('\t' * 2 + '{')
            for key, item in new.items.items():
                if key == 'links' or key == 'images':
                    print("\t" * 3 + 'links:')
                    print("\t" * 3 + '[')
                    for link in item:
                        print("\t" * 4 + link + ';')
                    print("\t" * 3 + '];')
                else:
                    if item == 'Unknown' and key in ['pubDate', 'published']:
                        continue
                    print("\t" * 3 + key + ':' + item + ';')
            print("\t" * 2 + '};')
        print("\t" * 1 + '];')
        print('};')
