"""
This module provides one-shot command-line RSS rss_reader
"""
import os
import sys
import argparse
import json
import logging
from rss_reader.news import News


current_version = "1.0"
log_file_name = 'rss_reader.log'


def print_json(news, indent):
    """
    This function prints news in JSON format
    :param news: RSS news (class News)
    :param indent: indent size of nested structures (int)
    :return: None
    """
    print(json.dumps(news.to_json(), indent=indent))


def print_error(message):
    """
    This function prints errors to stdout in specified format
    :param message: message to be printed
    :return: None
    """
    print(f'{os.path.basename(sys.argv[0])}: error: {message}')


def main():
    """
    This function parse program arguments, gets and outputs RSS news and makes logs
    :return: None
    """

    parser = argparse.ArgumentParser(description='Pure Python command-line RSS rss_reader.')
    parser.version = current_version
    parser.add_argument('source', type=str, help='RSS URL')
    parser.add_argument('--version', help='Print version info', action='version')
    parser.add_argument('--json', help='Print result as JSON in stdout', action="store_true")
    parser.add_argument('--verbose', help='Output verbose status messages', action="store_true")
    parser.add_argument('--limit', type=int, help='Limit news topics if this parameter provided', default=-1)
    args = parser.parse_args()

    logger = logging.getLogger('rss_reader')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if args.verbose:
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

    logger.info(f'Program started with URL "{args.source}"')

    is_error = False
    rss_news = News(args.source, args.limit)
    try:
        rss_news.get_news()
    except Exception as err:
        is_error = True
        error_message = err
        logger.error(error_message)
        if not args.verbose:
            print_error(error_message)

    if not is_error:
        if args.json:
            print_json(rss_news, 2)
            logger.info(f'{rss_news.get_count()} news were displayed in the console in json format')
        else:
            print(rss_news)
            logger.info(f'{rss_news.get_count()} news were displayed in the console')

    logger.info('Program completed')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_error(e)
