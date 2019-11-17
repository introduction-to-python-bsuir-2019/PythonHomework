import argparse
import feedparser
import html
import json
import logging
import requests
import sys
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup


def argument_parse():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', action="store_true", help='Print version info')
    parser.add_argument('--json', action="store_true", help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
    parser.add_argument('--limit', type=int, default=5, help='Limit news topics if this parameter provided')
    return parser.parse_args()


def parse(rss_url):
    logging.info('Parsing a feed from a remote URL.')
    return feedparser.parse(rss_url)


def get_news_feed(rss_url, limit=0):
    logging.info('Get news from RSS feed.')
    news_feed = parse(rss_url)
    print('Feed: ', news_feed['feed']['title'], '\n')
    dict_of_links = dict(img=[], link=[])
    for post in news_feed.entries[:limit]:
        print('Title: ', post.title)
        print('Date: ', post.published, '\n')
        dict_of_links['link'].append(post.link)
        soup = BeautifulSoup(post.description, 'html.parser')
        image_tags = soup.findAll('img')
        for image_tag in image_tags:
            dict_of_links['img'].append(image_tag.get("src"))
            print(f'[Image: {image_tag.get("alt")}]')
        print(html.unescape(soup.text), '\n')
        print('Useful links:')
        print(f'Image links: {dict_of_links["img"]}')
        print(f'Post link: {post.link}')


def load_rss(rss_url):
    logging.info('Saving the XML file.')
    resp = requests.get(rss_url)
    with open('topnewsfeed.xml', 'wb') as f:
        f.write(resp.content)


def parse_xml(xmlfile, limit=5):
    logging.info('Parse XML file.')
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    xml_dict = dict(feed=root.find('./channel/title').text, news_items=[])
    for item in root.findall('./channel/item')[:limit]:
        news = {}
        for child in item:
            if child.tag in ['link', 'title', 'pubDate', 'description']:
                news[child.tag] = child.text
        xml_dict['news_items'].append(news)
    return xml_dict


def get_console_handler():
    formatter = logging.Formatter("%(asctime)s — %(funcName)s — %(name)s — %(level)s — %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    return console_handler


def get_logger():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.info('Start logging INFO')
    logger.debug('Start logging DEBUG')
    logger.addHandler(get_console_handler())
    return logger


def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped


def main():
    args = argument_parse()
    load_rss(args.source)
    if args.json:
        print(json.dumps((parse_xml('topnewsfeed.xml', args.limit)), indent=4, ensure_ascii=False))
    elif args.verbose:
        get_logger()
    elif args.version:
        pass
    else:
        get_news_feed(args.source, args.limit)


if __name__ == '__main__':
    logging.info('Calling main function.')
    main()
