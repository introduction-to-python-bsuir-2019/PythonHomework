import requests
import re

import lxml.html as html
import xml.etree.ElementTree as ET

import argparse

class NewsReader:
    def __init__(self, url, limit=None):
        self.url = url
        self.limit = limit
        self.items = self.get_news()

    def get_news(self):
        request = requests.get('https://news.yahoo.com/rss')

        result = request.text
        tree = ET.fromstring(result)

        items = dict()
        items.setdefault('title', ' ')

        for head_el in tree[0]:
            if head_el.tag == 'title':
                items['title'] = head_el.text

        for num, item in enumerate(tree.iter('item')):

            if self.limit is not None and self.limit == num:
                break

            items.setdefault(num, {})

            news_description = dict()

            for description in item:
                news_description[description.tag] = description.text

            items[num].update(news_description)

        return items

    @staticmethod
    def get_image_regexpr(description):
        image_url = re.findall(r'src="([^"]+)"', description)
        image_description = re.findall(r'alt="([^"]+)"', description)

        return image_url, image_description

    @staticmethod
    def get_image(description):
        xhtml = html.fromstring(description)
        image_src = xhtml.xpath('//img/@src')
        image_description = xhtml.xpath('//img/@alt')

        return image_src, image_description

    @staticmethod
    def get_description(description):
        node = html.fromstring(description)

        return node.text_content()

    @staticmethod
    def news_text(news):
        image = NewsReader.get_image(news['description'])

        # TODO: solve problem with image indexing

        image_src = image[0][0]
        image_description = image[1][0]

        result = "\n\tTitle: {}\n\tDate: {}\n\tLink: {}\n\n\tImage link: {}\n\t" \
                 "Image description: {}\n\tDescription: {}".format(news['title'],
                                                                   news['pubDate'],
                                                                   news['link'],
                                                                   image_src,
                                                                   image_description,
                                                                   NewsReader.get_description(news['description']))

        return result

    def fancy_output(self):
        for key, value in self.items.items():
            if key == 'title':
                print(f'Feed: {value}')
            else:
                print(self.news_text(value))

            print('_' * 100)


rss = NewsReader('https://news.yahoo.com/rss', limit=2)
rss.fancy_output()
