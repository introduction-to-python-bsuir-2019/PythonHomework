"""
    Controls the launch of the rss-reader program
"""

import logging

import dateutil.parser as dateparser

from app.argparser import ArgParser
from app.RSSreader import RSSreader
from app.pdf_converter import PDFConverter


def main():
    """ Reads arguments and displays news """

    arguments = ArgParser()
    args = arguments.get_args()

    if args.verbose:
        logger = get_logger()
    else:
        logger = logging.getLogger()

    logger.info('Start')

    if args.version:
        print(args.version)
        logger.info('Exit')

    rss_reader = RSSreader(arguments, logger)

    if args.date:
        try:
            dateparser.parse(args.date, fuzzy=True).strftime('%Y%m%d')
        except dateparser._parser.ParserError:
            print('Invalid date format')
            logger.info('Exit')
            return
        cached_feed = rss_reader.get_cached_json_news()
        if cached_feed:
            print('Cached news', args.date)
            if args.json:
                rss_reader.print_cached_feed_json(cached_feed)
            else:
                rss_reader.print_cached_feed(cached_feed)
            if args.to_pdf:
                converter = PDFConverter(arguments, logger)
                converter.write_json_to_pdf()
        logger.info('Exit')
        return

    feed = rss_reader.get_feed()

    if args.to_pdf:
        converter = PDFConverter(arguments, logger, news=feed)
        converter.write_to_pdf()

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
