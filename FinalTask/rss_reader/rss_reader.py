import argparse
import json
from .rss_parser import RssParser
from .rss_parser import create_logger

current_version = 0.25


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
        logger = create_logger('rss-reader')
        logger.info('logging enabled.')
    verbose = args.verbose
    if args.version:
        print(f'Current version: {current_version}')
        if verbose:
            logger.info('current utility version was printed')
        exit()
    if args.limit:
        limit = args.limit
        if verbose:
            logger.info(f'news limit was set to {limit}')
    else:
        limit = 10
        if verbose:
            logger.info(f'news limit was set to {limit}')
    my_parser = RssParser(args.source, limit, verbose)
    if args.json:
        my_parser.parse_rss()
        print(json.dumps(my_parser.feed_to_json(), indent=1))
        if verbose:
            logger.info(f'{limit} news have been printed in JSON format')
    else:
        print(my_parser.parse_rss())
        if verbose:
            logger.info(f'{limit} news have been printed')


if __name__ == '__main__':
    main()
