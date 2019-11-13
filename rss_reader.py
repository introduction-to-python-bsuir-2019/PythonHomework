"""Module provides work with command line"""

import argparse
import logging
import sys

from news import RssReader

VERSION = "1.0"


def add_args(parser) -> parser:
    """Add arguments and return new parser."""

    parser.add_argument('source', help='RSS URL', type=str)
    parser.add_argument('--version', help='Print version info', action='version')
    parser.add_argument('--json', help='Print result as JSON in stdout', action="store_true")
    parser.add_argument('--verbose', help='Outputs verbose status messages', action="store_true")
    parser.add_argument('--limit', help='Limit news topics if this parameter provided', type=int)
    return parser

def start_parsing(url: str, limit: int, json_mode: bool):
    """This function create rss feed and print news.

    Arguments:
        url - RSS URL
        limit - news amount that will be printed
        json_mode - if true then news will be printed in JSON format
    """

    logging.info('Create feed')
    feed = RssReader(url, limit)

    if json_mode:
        print(feed.convert_to_json())
    else:
        feed.print_news()

def main():
    """This function works with arguments, starts parsing."""

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader')
    parser = add_args(parser)
    parser.version = VERSION
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    try:
        start_parsing(args.source, args.limit, args.json)
    except Exception as e:
        logging.ERROR("Something wrong with parsing: {e}")

    logging.info('Program is completed')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Something went wrong: ', e)
        sys.exit(1)
