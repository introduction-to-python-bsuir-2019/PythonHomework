"""
    Controls the launch of the rss-reader program
"""

import logging

import dateutil.parser as dateparser

from app.argparser import ArgParser
from app.RSSReader import RSSReader
from app.pdf_converter import PDFConverter
from app.html_converter import HTMLConverter
from app.rss_exception import RSSException


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

    rss_reader = RSSReader(args.url, args.limit, args.date, logger, args.colorize)

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
                pdf_converter = PDFConverter(args.url, args.limit, args.date, args.to_pdf, logger)
                pdf_converter.write_json_to_pdf()
            if args.to_html:
                html_converter = HTMLConverter(args.url, args.limit, args.date, args.to_html, logger)
                html_converter.write_to_html()
        logger.info('Exit')
        return

    try:
        feed = rss_reader.get_feed()
    except RSSException as rss_exc:
        print(rss_exc)
        return

    if args.to_pdf:
        pdf_converter = PDFConverter(args.url, args.limit, args.date, args.to_pdf, logger, news=feed)
        pdf_converter.write_to_pdf()

    if args.to_html:
        html_converter = HTMLConverter(args.url, args.limit, args.date, args.to_html, logger)
        html_converter.write_to_html()

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
