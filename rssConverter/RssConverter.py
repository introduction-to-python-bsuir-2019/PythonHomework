import feedparser
import re
import json


class RssConverter:

    def __init__(self):
        self.tags = ['image', 'links', 'title', 'link', 'pubDate', 'published', 'summary', ]

    def get_news(self, url, limit=None):
        result = feedparser.parse(url)
        if result['entries'] and result.status == 200:
            return self.dict_list__maker(result, limit)
        else:
            raise Exception("something wrong with with url. Please check url and try later ")

    def dict_list__maker(self, rss, limit=None):
        if limit is None:
            limit = len(dict(rss))
        entries = rss['entries']
        return entries[:limit]

    def print_news(self, dict_list):
        for dictionary in dict_list:
            for key, value in dictionary.items():
                if key in self.tags:
                    if key == 'summary':
                        print("\n")
                        result = re.search(r'>[A-ZА-Я0-9a-zа-я][‘+,:;=?@#|.^*() %!a-zA-Zа-яА-Я0-9"\s]*', value)
                        if result:
                            print(result.group(0)[1:-1])
                    elif key == 'links':  # list of links
                        for j in value:
                            print("\n")
                            print(j.get('type', '') + '     ' + j.get('href', ''))
                    elif key == 'item':
                        self.print_result(self, value.items)
                    else:
                        print("\n")
                        print(key + '    ' + value)
            print('-----------------------------------------------------------------------------------')

    def json_convert(self, dict_list):
        for i in dict_list:
            print(json.dumps(i, sort_keys=True,
                             indent=4, separators=(',', ': ')))




