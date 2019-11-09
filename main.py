#!/usr/bin/python3
import argparse
from RssConverter import RssConverter
import logging

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rss reader', add_help=True)
    current_version = "1.0.0"
    log_file = 'rss_converter.log'
    parser.add_argument(
        '--url',
        help='url address'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help=' Limit news topics if this parameter provided'
    )
    parser.add_argument(
        '--version',
        type=int,
        help=' Print version info'
    )
    parser.add_argument(
        '--json',
        help='Print result as JSON in stdout'
    )
    parser.add_argument(
        '--verbose',
        help='Outputs verbose status messages'
    )
    args = parser.parse_args()
    logger = logging.getLogger('rss_converter')
    logger.setLevel(logging.INFO)
    logger.info('Start')
    rss = RssConverter()
    logger.info("try to get news")
    if args.url:
        not_parsed_news = rss.get_news(args.url)
        logger.info("got news")
        news_list = rss.parse_news(not_parsed_news)
        logger.info("parse rss to news list")
        logger.info("print news")
        rss.print_news(news_list, args.limit)
        logger.info("news are printed")
        if args.version:
            pass
        if args.json:
            logger.info("print json")
            rss.in_json_format(news_list, args.limit)
            logger.info("json is printed")
        if args.verbose:
            with open(log_file) as log_file:
                print(log_file.read())
    else:
        print('please specify url')
