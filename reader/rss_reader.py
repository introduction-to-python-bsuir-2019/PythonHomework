import feedparser
import json
import datetime
from bs4 import BeautifulSoup


class RSSReader:
    def __init__(self, source, limit=1, json=False, date='', to_html=''):
        self.source = source
        self.limit = limit
        self.json = json
        self.date = date
        self.to_html = to_html
        self.feeds = {}

    def parse_source(self):
        d = feedparser.parse(self.source)

        self.feeds['news'] = []
        channel = d['channel']['title']

        for news in d['entries'][0:self.limit]:
            self.feeds['news'].append(self.read_news(news, channel))

        if self.date:
            self.from_cache()
        elif self.to_html:
            self.convert_to_html(self.feeds['news'])
            self.to_cache()
        else:
            self.print_feeds(self.feeds['news'])
            self.to_cache()

    @staticmethod
    def read_news(news, channel):
        item = dict()

        item['feed_name'] = channel
        item['title'] = news['title'].replace('&#39;', "'")
        item['date'] = news['published']
        item['link'] = news['link']

        soup = BeautifulSoup(news['summary'], 'html.parser')

        item['image_title'] = soup.find('img')['title']
        description = soup.p.contents[-2]
        if str(description)[0] == '<':
            item['image_description'] = 'No image description'
        else:
            item['image_description'] = description
        if soup.find('img')['src'] == "":
            item['image_link'] = 'No image link'
        else:
            item['image_link'] = soup.find('img')['src']

        return item

    def to_cache(self):
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
        to_print = []
        with open('./cache.json', 'r') as f:
            feeds_f = json.load(f)
            for item in feeds_f['news']:
                item_date = datetime.datetime.strptime(item['date'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d')
                if self.date == item_date:
                    to_print.append(item)

        self.print_feeds(to_print)

    def convert_to_html(self, convert):
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

    def print_feeds(self, to_print):
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
