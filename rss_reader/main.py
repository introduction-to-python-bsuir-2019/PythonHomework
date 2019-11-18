"""Main module of RssReader which starts program."""

import logging
import argparse
from logging import config

from rss_parser import RssReader
import caching_news

VERSION = '4.0'

LOGS_FILENAME = "rss_reader.log"

ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.main'

CORRECT_END_LOG = 'END (correct)'

# LINK = 'https://www.reddit.com/.rss'

# LINK = 'https://news.yahoo.com/rss/'
# LINK = 'https://www.newsisfree.com/rss/'
# LINK = 'https://news.tut.by/rss/index.rss'


def create_args_parser() -> argparse.ArgumentParser:
    """Func which creats parser of arguments of command-line.

    Return: argparse.ArgumentParser
    """
    logger = logging.getLogger(MODULE_LOGGER_NAME + '.create_args_parser')
    logger.info("Create parser of arguments")

    parser = argparse.ArgumentParser(description='Command-line RSS reader.')
    return parser


def init_args(parser: argparse.ArgumentParser) -> None:
    """Func which takes parser and adds arguments."""
    logger = logging.getLogger(MODULE_LOGGER_NAME + '.init_args')
    logger.info('Initialize arguments of command-line')

    parser.add_argument(
        '-v',
        '--version',
        help='Print version info',
        action='version',
        version=('version ' + VERSION)
    )
    parser.add_argument(
        '--json',
        help='Print result as JSON in stdout',
        action='store_true'
    )
    parser.add_argument(
        "-l",
        '--limit',
        type=int,
        help='Limit news topics if this parameter provided'
    )
    parser.add_argument(
        "--date",
        type=str,
        help='Argument, which allows to get !cashed! news by date. Format: YYYYMMDD'
    )
    parser.add_argument(
        "link",
        type=str,
        nargs='?',
        help='Link on RSS resource'
    )
    parser.add_argument(
        "-V",
        "--verbose",
        help='Print all logs in stdout',
        action='store_true'
    )
    parser.add_argument(
        "--to_fb2",
        type=str,
        help="Convert news to fb2 format.\
        Path must contain exsisting directories\
        Supports LIMIT",
        metavar='PATH'
    )
    parser.add_argument(
        "--to_pdf",
        type=str,
        help="Convert news to pdf format.\
        Convertation to PDF supports only latin resource.\
        Path must contain exsisting directories\
        Supports LIMIT. Unsupports non-latin resources.",
        metavar='PATH'
    )


if __name__ == "__main__":
    logging.config.fileConfig('logger_config.conf')
    logger = logging.getLogger(MODULE_LOGGER_NAME)
    logger.info('START')

    parser = create_args_parser()
    init_args(parser)
    args = parser.parse_args()

    if args.verbose is True:
        logger.info('Output logs')

        with open(LOGS_FILENAME, 'r') as file:
            print(file.read())

        logger.info(CORRECT_END_LOG)
    elif args.link is not None:
        logger.info('Entrance to get news case')

        rss_reader = RssReader(link=args.link)

        if args.limit is not None:
            limit = args.limit
        else:
            limit = 0

        try:
            if args.json is True:
                news = rss_reader.get_news_as_json(limit=limit)
                print(news)
            elif args.to_fb2 is not None:
                rss_reader.get_news_as_fb2(limit=limit, filepath=args.to_fb2)
            elif args.to_pdf is not None:
                rss_reader.get_news_as_pdf(limit=limit, filepath=args.to_pdf)
            else:
                news = rss_reader.get_news_as_string(limit=limit)
                print(news)
            logger.info(CORRECT_END_LOG)
        except AttributeError:
            print("Incorrect link on resource!")
            logger.info('END (incorrect link)')
    elif args.date is not None:
        logger.info(f'Getting cashed news by date: {args.date}')

        try:
            print(caching_news.db_read(args.date))
            logger.info(CORRECT_END_LOG)
        except caching_news.sqlite3.OperationalError:
            print('Incorrect value of date!')
            print('You may enter next values: ')
            print(caching_news.get_list_of_tables())
            logger.info('Was entered incorrect value of date')
    else:
        logger.error('END (no args)')
        print('Missing argument: LINK\n')
        parser.parse_args(['-h'])
