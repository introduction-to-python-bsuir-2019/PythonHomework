"""Module provides work with command line."""

import argparse
import logging
import sys

from rss.news import News
from rss.cache import Cache

VERSION = "3.0"


def add_args(parser):
    """Add arguments and return new parser."""

    logging.info('Add arguments')
    parser.add_argument('source', help='RSS URL', type=str)
    parser.add_argument('--version', help='Print version info', action='version')
    parser.add_argument('--json', help='Print result as JSON in stdout', action="store_true")
    parser.add_argument('--verbose', help='Outputs verbose status messages', action="store_true")
    parser.add_argument('--limit', help='Limit news topics if this parameter provided', type=int)
    parser.add_argument('--date', help="""Take a date in %%Y%%m%%d format.
                         The news from the specified day will be printed out.""", type=str)
    return parser


def start_parsing(url: str, limit: int, json_mode: bool):
    """This function create rss feed and print news.

    :param url: RSS URL
    :param limit: news amount that will be printed
    :param json_mode: if true then news will be printed in JSON format
    """

    logging.info('Create feed')
    feed = News(url, limit)
    if json_mode:
        print(feed.convert_to_json(limit))
    else:
        feed.print_news(limit)


def set_verbose_mode(verbose_mode: bool):
    """Set logging level and format"""

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    if verbose_mode:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logging.info('Set verbose mode')


def main():
    """This function works with arguments, starts parsing."""

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser = add_args(parser)
    parser.version = VERSION
    args = parser.parse_args()

    set_verbose_mode(args.verbose)

    if args.date:
        try:
            cache = Cache()
            cache.set_printing_news(args.source, args.date, args.limit, args.json)
        except Exception as e:
            print('Errors with cache:', e)
    else:
        try:
            start_parsing(args.source, args.limit, args.json)
        except Exception as e:
            print('Errors with parsing:', e)

    logging.info('Program is completed')


def run():
    """Entry point"""

    try:
        main()
    except Exception as e:
        print('There are some errors: ', e)
