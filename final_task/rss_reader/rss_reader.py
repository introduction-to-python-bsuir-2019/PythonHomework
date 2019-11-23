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
import cacher

def init_cli_parser():
    """
    this function initializes command line parser with all nessecary arguments
    """
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.', prog='rss-reader')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("source", type=str, nargs='?', default=None, help="RSS URL")
    parser.add_argument('--version', help="print version info", action='version', version='%(prog)s 1.3')
    parser.add_argument("--json", help="print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="output verbose status messages", action="store_true")
    group.add_argument("--date", type=str,  help="print news with provided publish date in stdout")
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

def get_post_content(post, feed_title):
    """
    this function fetches nessecary elements of a publication from post
    """
    data = {}
    data['feed'] = feed_title
    data['title'] = html.unescape(post.title)
    data['pub_date'] = post.published
    data['pub_parsed'] = f"{post.published_parsed.tm_year}{post.published_parsed.tm_mon}{post.published_parsed.tm_mday}"
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
        news += [get_post_content(post, feed.feed.title)]

    return news

def display_news(news):
    """
    this function prints news in stdout
    """
    if len(news) == 0:
        return

    is_same_feed = all([news[0]['feed'] == item['feed'] for item in news])
    if is_same_feed:
        print(f"Feed: {news[0]['feed']}\n")

    for item in news:
        if not is_same_feed:
            print(f"Feed: {item['feed']}\n")
        print(f"Title: {item['title']}")
        print(f"Publication date: {item['pub_date']}")
        print(f"Link: {item['link']}\n")
        print(f"{item['description']}\n")
        print("Links:")
        for index, tpl in enumerate(item['hrefs']):
            print(f"[{index + 1}] {tpl[0]} ({tpl[1]})")
        print('\n')

    return

def to_json(news):
    """
    this function represents news in json format
    """
    for ind, item in enumerate(news):
        del item['pub_parsed']
        news[ind] = item

    return json.dumps({'news': news}, indent=2)

def main():
    """
    an entry point for a program
    """
    logger = init_logger()
    args = init_cli_parser()
    connection, cursor = cacher.init_database()

    if args.verbose:
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.info(f"verbose notifications are turned on")

    if args.limit:
        if args.limit < 1:
            if not args.verbose:
                print("error: invalid limit value")
            logger.error(f"invalid limit value")
            logger.info(f"end of work -->|")
            return

    if args.date:
        try:
            logger.info(f"checking date..")
            if not cacher.is_valid_date(args.date):
                raise ValueError
            logger.info(f"started fetching data from cache..")
            news = cacher.get_cached_news(cursor, args.date)
            if len(news) == 0:
                raise IndexError
            news = news[:args.limit if args.limit else len(news)]
        except ValueError:
            if not args.verbose:
                print("error: invalid date")
            logger.error(f"invalid date")
            logger.info(f"end of work -->|")
            return
        except IndexError:
            if not args.verbose:
                print("no news for this date")
            logger.info(f"no news for this date")
            logger.info(f"end of work -->|")
            return

    if args.source:
        logger.info(f"started fetching data (url - {args.source})..")
        try:
            news = parse_news(args.source)
            logger.info(f"started caching data..")
            cacher.cache_news(connection, cursor, news)
            news = news[:args.limit if args.limit else len(news)]
        except ValueError:
            if not args.verbose:
                print(f"error: not well-formed xml or broken access to the Internet")
            logger.error(f"not well-formed xml or broken access to the Internet")
            logger.info(f"end of work -->|")
            return

    if args.limit:
        logger.info(f"the limit of publications to show - {args.limit}")

    if not args.json:
        logger.info(f"displaying news..\n")
        display_news(news)
    else:
        logger.info(f"displaying news in json format..\n")
        print(to_json(news))

    logger.info(f"\npublications were successfully shown - {len(news)}")
    logger.info(f"end of work -->|")

    return

if __name__ == "__main__":
    main()
