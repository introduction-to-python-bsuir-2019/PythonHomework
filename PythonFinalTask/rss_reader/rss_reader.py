import sys
import json
import argparse
import logging
from news_feed import News

PROJECT_VERSION = "1.0"
log_file_name = 'rss_reader.log'


def to_json(news, indent):
    print(json.dumps(news.to_json(), indent=indent))


def get_parser():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS rss_reader.')
    parser.version = PROJECT_VERSION
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', help='Print version info', action='version')
    parser.add_argument('--json', help='Print result as JSON in stdout', action="store_true")
    parser.add_argument('--verbose', help='Output verbose status messages', action="store_true")
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided', default=-1)
    return parser.parse_args()


def main():
    args = get_parser()

    logger = logging.getLogger('rss_reader')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if args.verbose:
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

    rss_news = News(args.source, args.limit)
    rss_news.parse_news()

    if args.json:
        to_json(rss_news, 2)
        logger.info(f'{rss_news.get_count()} news were displayed in the console in json format')
    else:
        print(rss_news)
        logger.info(f'{rss_news.get_count()} news were displayed in the console')

    logger.info('Program completed')


if __name__ == '__main__':
    main()
