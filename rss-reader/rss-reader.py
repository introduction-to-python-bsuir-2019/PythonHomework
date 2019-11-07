#!/usr/bin/env python3.8

import argparse
import feedparser
import html
import json
from bs4 import BeautifulSoup

version = """Version 0.0.1"""

argument_parser = argparse.ArgumentParser(prog='RSS-reader.', description='Simple "one-shot" RSS Reader.')
argument_parser.add_argument('source', type=str, help='an RSS link')
argument_parser.add_argument('--version', action='store_true', help='print version info')
argument_parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
argument_parser.add_argument('--verbose', action='store_true', help='outputs verbose status messages')
argument_parser.add_argument('--limit', type=int, default=1, help='limit news topics if this parameter provided')
args = argument_parser.parse_args()


class News:
    """Class for news objects (lol)"""
    def __init__(self, feed, title, published, link, description, news_id):
        self.feed = feed
        self.title = title
        self.published = published
        self.link = link
        self.description = description
        self.news_id = news_id


def parse_rss(source: str):
    """Parses RSS feed and returns list of 'News' objects"""
    list_of_news = []
    print('Parsing rss feed...') if args.verbose else None
    rss = feedparser.parse(source)
    for x in rss['entries']:  # converting from type(rss) object into News object
        try:
            feed = html.unescape(rss['feed']['title'])
        except KeyError:
            feed = 'No feed name given'
        try:
            published = tuple(x['published_parsed'])
        except KeyError:
            published = ()
        try:
            title = html.unescape(x['title'])
        except KeyError:
            title = 'No title given'
        try:
            link = html.unescape(x['link'])
        except KeyError:
            link = 'No link given'
        try:
            description = html.unescape(x['description'])
        except KeyError:
            description = 'No description given'
        try:
            news_id = x['id']
        except KeyError:
            news_id = None
        list_of_news.append(News(feed, title, published, link, description, news_id))
    if not list_of_news:
        print('News not found')
    return list_of_news


def output_in_console(list_of_news):
    """Outputs news from the list given in a readable format"""
    print('Printing news in console ...') if args.verbose else None
    for news in list_of_news:
        print('Feed: {}'.format(news.feed), end='\n\n')
        print('Title: {}'.format(news.title))
        try:
            print('Date: {}.{}.{}'.format(news.published[2], news.published[1], news.published[0]))
        except IndexError:
            print('Date: No date given')
        print('Link: {}'.format(news.link), end='\n\n')
        print('{}'.format(make_description_readable(news.description)), end='\n\n')
        print('{:-^40s}'.format(''))


def output_as_json(list_of_news):
    """Outputs news from the list given in a JSON format"""
    dumped_news = []
    for x in list_of_news:  # converting list of news into list of dictionries
        news_dict = {}
        news_dict.update({'feed': x.feed})
        news_dict.update({'title': x.title})
        news_dict.update({'published': x.published})
        news_dict.update({'link': x.link})
        news_dict.update({'description': x.description})
        news_dict.update({'news_id': x.news_id})
        dumped_news.append({'item': news_dict})
    print(json.dumps(dumped_news, indent=2))


def make_description_readable(description: str) -> str:
    """Decodes xml string into readable format"""
    soup = BeautifulSoup(description, 'lxml')
    links = dict()
    for link in soup.findAll('a'):
        links.update({link.text.strip(): link.get('href')})
    try:
        image = soup.find('a').find('img').get('src')
    except AttributeError:
        image = 'no_image'
        if args.verbose:
            print('Unable to find image')
    result = ' '.join(soup.text.split())
    if image != 'no_image':
        result += '\n\nImage: {}'.format(image)
    if links:
        result += '\nLinks:'
        for link in links:
            result += '{} {}\n    '.format(link, links.get(link))
    return result


def main():
    """Entrypoint to rss_reader script"""
    if args.version:
        print(version, end='\n')
        return
    news = parse_rss(args.source)[:args.limit]
    if args.json:
        output_as_json(news)
    else:
        output_in_console(news)


if __name__ == '__main__':
    main()
