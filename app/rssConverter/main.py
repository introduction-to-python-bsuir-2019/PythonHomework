import argparse
import logging
import app
import os
from datetime import datetime
from app.rssConverter.RssConverter import RssConverter
from app.rssConverter.Exeptions import RssGetError, IncorrectLimit, IncorrectDateOrURL
from app.rssConverter.DataSafer import NewsGetterSafer


def main():
    parser = argparse.ArgumentParser(description='Rss reader', add_help=True)
    log_file = 'rss_converter.log'
    parser = args_adding(parser)
    args = parser.parse_args()
    logger = set_logger(log_file)
    logger.info('Start')
    rss = RssConverter()
    logger.info("try to get news")
    try:
        if args.url:
            if args.date:
                news_list = NewsGetterSafer.get_data(args.date, args.url)
            else:
                not_parsed_news = rss.get_news(args.url)
                logger.info("got news")
                news_list = rss.parse_news(not_parsed_news)
                logger.info("parsed rss to news list")
                NewsGetterSafer.save_data(args.url, news_list, datetime.today().strftime('%Y%m%d'))
                logger.info("news saved")
            if args.json:
                logger.info("print json")
                rss.in_json_format(news_list, args.limit)
                logger.info("json is printed")
            else:
                rss.print_news(news_list, args.limit)
                logger.info("news are printed")
            if args.verbose:
                with open(log_file) as log_file:
                    print(log_file.read())
        else:
            print('please specify url')

    except IncorrectDateOrURL as ex:
        logger.info("incorrect date or url")
        print('You have entered {0} url and {1} date, but it is incorrect or you have network problem.\
        Please check it and try again'.format(ex.url, ex.date))
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


def creating_image_dir():
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, 'images')
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print("create folder with path {0}".format(image_path))
    else:
        print("folder exists {0}".format(image_path))
    return image_path


def set_logger(log_file):
    open(log_file, 'w').close()  # cleaning log file
    logger = logging.getLogger('rss_converter')
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def args_adding(parser):
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
        action="version",
        version=f"%(prog)s {app.__version__}",
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
    parser.add_argument(
        '--date',
        help='input date',
    )
    return parser
