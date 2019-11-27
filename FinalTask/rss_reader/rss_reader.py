import argparse
import json
import logging
from .rss_parser import RssParser

current_version = 0.24


def main():
    parser = argparse.ArgumentParser(description='Brand new euseand\'s RSS-parser written in Python')
    parser.version = current_version
    parser.add_argument("source", help="RSS URL")
    parser.add_argument("--version", help="Print version info", action="store_true")
    parser.add_argument("--json", help="Print result as JSON in stdout", action="store_true")
    parser.add_argument("--verbose", help="Output verbose status messages", action="store_true")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    args = parser.parse_args()
    if args.verbose:
        logger = create_logger()
        logger.info('logging enabled.')
    verbose = args.verbose
    if args.version:
        print(f'Current version: {current_version}')
        logger.info('current utility version was printed')
        exit()
    if args.limit:
        limit = args.limit
        logger.info(f'news limit was set to {limit}')
    else:
        limit = 10
        logger.info(f'news limit was set to {limit}')
    my_parser = RssParser(args.source, limit, verbose)
    if args.json:
        my_parser.parse_rss()
        logger.info(f'{limit} news have been fetched from {args.source}')
        print(json.dumps(my_parser.feed_to_json(), indent=1))
        logger.info(f'{limit} news limit have been printed in JSON format')
    else:
        print(my_parser.parse_rss())
        logger.info(f'{limit} news limit have been printed')


def create_logger():
    logger = logging.getLogger('rss-reader')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


if __name__ == '__main__':
    main()
