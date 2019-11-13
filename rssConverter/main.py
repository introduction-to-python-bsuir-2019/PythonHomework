#!/usr/bin/python3
import argparse
from rssConverter.RssConverter import RssConverter
from rssConverter.Exeptions import RssGetError, IncorrectLimit
import logging


def main():
    parser = argparse.ArgumentParser(description='Rss reader', add_help=True)
    current_version = "1.0.0"
    log_file = 'rss_converter.log'
    parser.add_argument(
        'url',
        help='url address'
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help=' Limit news topics if this parameter provided'
    )
    parser.add_argument(
        '--version',
        action="store_true",
        help=' Print version info',
        default=False
    )
    parser.add_argument(
        '--json',
        action="store_true",
        help='Print result as JSON in stdout',
        default=False
    )
    parser.add_argument(
        '--verbose',
        action="store_true",
        help='Outputs verbose status messages',
        default=False
    )
    args = parser.parse_args()
    logger = logging.getLogger('rss_converter')
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.info('Start')
    rss = RssConverter()
    logger.info("try to get news")
    try:
        if args.url:
            not_parsed_news = rss.get_news(args.url)
            logger.info("got news")
            news_list = rss.parse_news(not_parsed_news)
            logger.info("parse rss to news list")
            logger.info("print news")
            rss.print_news(news_list, args.limit)
            logger.info("news are printed")
            if args.version:
                print(current_version)
            if args.json:
                logger.info("print json")
                rss.in_json_format(news_list, args.limit)
                logger.info("json is printed")
            if args.verbose:
                with open(log_file) as log_file:
                    print(log_file.read())
        else:
            print('please specify url')
    except RssGetError as ex:
        logger.info("incorrect url")
        print('You have entered {0} url, but it is incorrect or you have network problem. Please check it and try again'
              .format(ex.url))
    except IncorrectLimit as ex:
        logger.info("incorrect limit")
        print(
            'Limit should not be more than {0}'.format(ex.max_quantity))
    except Exception as ex:
        logger.info("Something has gone wrong. Exception is  {0}".format(ex))
    else:
        logger.info("Everything have worked without problems")
