import feedparser
import re
from rssConverter.New import New
from rssConverter.Exeptions import RssGetError, IncorrectLimit


class RssConverter:

    def __init__(self):
        self.tags = ['image', 'links', 'title', 'pubDate', 'published', 'summary', ]

    def get_news(self, url):
        result = feedparser.parse(url)
        if result['entries'] and result.status == 200:
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
        summary_parser = r'>[A-ZА-Я0-9a-zа-я][‘+,:;=?@#|.^*() %!a-zA-Zа-яА-Я0-9"\s]*'  # readable item summary output
        for dictionary in dict_list:
            new = New()
            for key, value in dictionary.items():
                if key in self.tags:
                    if key == 'summary':
                        result = re.search(summary_parser, value)
                        if result:
                            new.items['summary'] = result.group(0)[1:-1]
                    elif key == 'links':  # list of links
                        links = {}
                        for link in value:
                            links[link.get('type', '')] = link.get('href', '')
                        new.items['links'] = links

                    else:
                        new.items[key] = value
            news_list.append(new)
        return news_list

    def print_news(self, news_list, limit=None):
        news_list = self.get_limited_news(news_list, limit)
        for new in news_list:
            for key, item in new.items.items():
                if key == 'links':
                    for key_link, item_link in item.items():
                        print("\n")
                        print(key_link+'    '+item_link)
                elif item is not None:
                    print("\n")
                    print(key + '    ' + item)
            print('-----------------------------------------------------------------------------------')

    def in_json_format(self, news_list, limit):
        news_list = self.get_limited_news(news_list, limit)
        print('{')
        print('\t' + 'news:')
        print('\t' + '[')
        for new in news_list:
            print('\t'*2 + '{')
            for key, item in new.items.items():
                if key == 'links':
                    print("\t" * 3 + 'links:')
                    print("\t" * 3 + '[')
                    for key_link, item_link in item.items():
                        print("\t" * 4 + key_link + ':' + item_link + ';')
                    print("\t" * 3 + '];')
                elif item is not None:
                    print("\t"*3 + key + ':' + item+';')
            print("\t" * 2 + '};')
        print("\t" * 1 + '];')
        print('};')
