"""
main rss_reader module
"""

import sys
import argparse
import logging
import html
import json
import feedparser
from bs4 import BeautifulSoup

def init_cli_parser():
    """
    this function initializes command line parser with all nessecary arguments
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', prog='rss-reader')
    parser.add_argument("source", type=str, nargs='?', default=None, help="RSS URL")
    parser.add_argument('--version', help="print version info", action='version', version='%(prog)s 1.2')
    parser.add_argument("--json", help="print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="outputs verbose status messages", action="store_true")
    parser.add_argument("--limit", type=int, help="limit news topics if this parameter provided")

    return parser.parse_args()

def init_logger():
    """
    this function initizlizes logger connected with log file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("rss_reader_logs.txt")
    file_handler.setFormatter(logging.Formatter('%(asctime)s -- %(levelname)s -- %(message)s'))
    logger.addHandler(file_handler)

    return logger

def brush_text(line):
    """
    this function forms description text into more convinient form
    """
    start = 100
    while True:
        i = start - 10
        try:
            while line[i] != ' ':
                i += 1
        except IndexError:
            break
        line = line[:i] + "\n" + line[i + 1:]
        start += 100

    return line

def get_post_content(post):
    """
    this function fetches nessecary elements of a publication from post
    """
    data = {}
    data['title'] = html.unescape(post.title)
    data['pub_date'] = post.published
    data['link'] = post.link
    soup = BeautifulSoup(post.description, 'html.parser')
    data['description'] = brush_text(html.unescape(soup.text))
    data['hrefs'] = [(link['href'], 'link') for link in soup.find_all('a') if link.get('href', None)]
    for img in soup.find_all('img'):
        if not img.get('src', 'Unknown') == '':
            data['hrefs'] += [(img.get('src', 'Unknown'), 'image', img.get('alt', ''))]
            data['description'] = \
                f"[image {len(data['hrefs'])}: {img.get('alt', '')}] [{len(data['hrefs'])}]\n" + data['description']

    return data

def parse_news(url):
    """
    this function parses news by given url and returns news list and feed title
    """
    feed = feedparser.parse(url)
    if feed.bozo == 1:
        raise ValueError

    news = []
    for post in feed.entries:
        news += [get_post_content(post)]

    return feed.feed.title, news

def display_news(feed, news, limit):
    """
    this function prints news in stdout
    """
    print(f"Feed: {feed}\n")
    for ind, item in enumerate(news):
        if ind >= limit:
            return
        print(f"Title: {item['title']}")
        print(f"Publication date: {item['pub_date']}")
        print(f"Link: {item['link']}\n")
        print(f"{item['description']}\n")
        print("Links:")
        for index, tpl in enumerate(item['hrefs']):
            print(f"[{index + 1}] {tpl[0]} ({tpl[1]})")
        print('\n')
    return

def main():
    """
    an entry point for a program
    """
    logger = init_logger()
    args = init_cli_parser()
    if args.verbose:
        logger.addHandler(logging.StreamHandler(sys.stdout))

    if args.source:

        if args.verbose:
            logger.info(f"verbose notifications are turned on")
        logger.info(f"started fetching data (url - {args.source})..")

        try:
            feed_title, news = parse_news(args.source)
        except ValueError:
            logger.error(f"not well-formed xml or broken access to the Internet")
            logger.info(f"end of work -->|")
            return

        if args.limit:
            logger.info(f"the limit of publications to show - {args.limit}")

        if not args.json:
            logger.info(f"displaying news..\n")
            display_news(feed_title, news, args.limit if args.limit else len(news))
        else:
            logger.info(f"displaying news in json format..\n")
            print(json.dumps({'news': {'feed': feed_title, \
                'publications': news[:args.limit if args.limit else len(news)]}}, indent=2))

        logger.info(f"publications were successfully shown - {args.limit if args.limit else len(news)}")
        logger.info(f"end of work -->|")

    return

if __name__ == "__main__":
    main()
