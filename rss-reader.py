"""
    Controls the launch of the rss-reader program
"""

from argparser import ArgParser
from RSSreader import RSSreader
import logging


def main():
    """ Reads arguments and displays news """

    arguments = ArgParser()
    args = arguments.get_args()

    if args.verbose:
        logger = get_logger()
    else:
        logger = logging.getLogger()

    rss_reader = RSSreader(arguments, logger)
    feed = rss_reader.get_feed()

    if args.version:
        print(args.version)
    if args.json:
        rss_reader.print_feed_json(feed)
    else:
        rss_reader.print_feed(feed)

    logger.info('Exit')


def get_logger():
    """ Returns logger with DEBUG level for creating logs in stdout """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s: %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


if __name__ == '__main__':
    main()
