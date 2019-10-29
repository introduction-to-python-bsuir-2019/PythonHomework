import requests
import re

import lxml.html as html
import xml.etree.ElementTree as ET
import json

import argparse

PROJECT_VERSION = '1.0'
PROJECT_DESCRIPTION = ''


class NewsReader:
    """
        Class for reading news from rss-format files.

        @Input: url
    """

    def __init__(self, url, limit=None, verbose=False):
        """

        :param url: url of rss
        :param limit: limit of news in feed
        """

        self.url = url
        self.limit = limit
        self.verbose = verbose

        self.items = self.get_news()

    def get_news(self):
        request = requests.get(self.url)  # TODO: catch all errors

        if self.verbose:
            print(request.status_code)  # TODO: create understandable error status output

        result = request.text
        tree = ET.fromstring(result)

        items = dict()
        items.setdefault('title', ' ')
        useful_tags = ['title', 'pubDate', 'link', 'description']

        for head_el in tree[0]:
            if head_el.tag == 'title':
                items['title'] = head_el.text

        for num, item in enumerate(tree.iter('item')):

            if self.limit is not None and self.limit == num:
                break

            items.setdefault(num, {})

            news_description = dict()

            for description in item:
                if description.tag in useful_tags:
                    news_description[description.tag] = description.text

            text, image_link, image_text = NewsReader.parse_description(news_description['description'])

            news_description['description'] = text
            news_description['imageLink'] = image_link
            news_description['imageDescription'] = image_text

            items[num].update(news_description)

        return items

    @staticmethod
    def parse_description(description):
        text = NewsReader.get_description(description)
        image = NewsReader.get_image(description)

        # TODO: deal with image indexing
        image_link = image[0]
        image_text = image[1]

        return text, image_link, image_text

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

        if len(image_src) == 0:
            image_src = 'No image'
        else:
            image_src = image_src[0]

        if len(image_description) == 0:
            image_description = 'No image description'
        else:
            image_description = image_description[0]

        return image_src, image_description

    @staticmethod
    def get_description(description):
        node = html.fromstring(description)

        return node.text_content()

    @staticmethod
    def news_text(news):

        result = "\n\tTitle: {}\n\tDate: {}\n\tLink: {}\n\n\tImage link: {}\n\t" \
                 "Image description: {}\n\tDescription: {}".format(news['title'],
                                                                   news['pubDate'],
                                                                   news['link'],
                                                                   news['imageLink'],
                                                                   news['imageDescription'],
                                                                   news['description'])

        return result

    def fancy_output(self):
        if self.verbose:
            print('News feed is ready')

        for key, value in self.items.items():
            if key == 'title':
                print(f'Feed: {value}')
            else:
                print(self.news_text(value))

            print('_' * 100)

    def to_json(self):
        if self.verbose:
            print('Json was created')

        json_result = json.dumps(self.items)

        return json_result


def main():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')

    parser.add_argument('source', type=str, help='RSS URL')

    parser.add_argument('--version', help='Print version info', action='store_true')
    parser.add_argument('--json', help='Print result as json in stdout', action='store_true')
    parser.add_argument('--verbose', help='Output verbose status messages', action='store_true')
    # TODO: add flags to output logs
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided')

    args = parser.parse_args()
    print(args)

    if args.version:
        print(PROJECT_VERSION)
        print(PROJECT_DESCRIPTION)

    if args.json:
        news = NewsReader(args.source, args.limit, args.verbose)

        print(news.to_json())
    else:
        news = NewsReader(args.source, args.limit, args.verbose)

        news.fancy_output()


if __name__ == '__main__':
    main()
