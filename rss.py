#!/usr/local/opt/python/bin/python3.7
import argparse
import logging
import sys
import getpass

from bots.tut import Bot
from utils.RssInterface import RssException


python_wiki_rss_url = "http://www.python.org/cgi-bin/moinmoin/" \
                      "RecentChanges?action=rss_rc"
tut_by_rss = 'https://news.tut.by/rss/index.rss'
google_rss = 'https://news.google.com/news/rss'
one_news_item = 'https://news.tut.by/world/658449.html?utm_campaign=news-feed&utm_medium=rss&utm_source=rss-news'
yahoo = 'https://news.yahoo.com/rss/'


def logger_init(level=None):
    """Logger initialisation

    All logs are printed into ./main.log file
    Other logs in regards of the 'level' are printed into console
    """

    level = level or logging.WARNING
    logger = logging.getLogger(getpass.getuser())
    logger.setLevel(level=level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Logging into file
    fh = logging.FileHandler("main.log", encoding="utf-8")  # 6
    fh.setLevel(logging.INFO)  # 7
    fh.setFormatter(formatter)

    # Logging into console
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(level)

    logger.addHandler(fh)
    logger.addHandler(consoleHandler)
    # coloredlogs.install(level=level, logger=logger)
    return logger


def main(url, logger, limit=10):

    parser = Bot(tut_by_rss, limit, logger)
    try:
        news = parser.get_news()
    except RssException as ex:
        logger.error(ex.args[0])
        logger.info('Exiting...')
    else:

        print(news)


if __name__ == "__main__":
    """
        usage: python test_task.py  KEF NCE 2019-11-13

        - finds the cheapest flight of different APIs;
        - sorts itineraries;
        - converts the flight price in BYN;
        """
    PARSER = argparse.ArgumentParser(
        description='''
                Rss reader. 
                Just enter rss url from your favorite site and app will print 
                latest news.
                '''
    )

    PARSER.add_argument('url', type=str,
                        help='url of rss',
                        )

    PARSER.add_argument('--verbose',
                        help='Outputs verbose status messages',
                        action='store_true',
                        )
    PARSER.add_argument('--limit',
                        help='Limit news topics if this parameter provided',
                        default=10,
                        type=int,
                        )
    PARSER.add_argument('--json',
                        help='Print result as JSON in stdout',
                        action='store_true',
                        )
    PARSER.add_argument('-v', '--version',
                        help='Print version info',
                        action='version',
                        version='%(prog)s 1.0'
                        )

    ARGS = PARSER.parse_args()

    if ARGS.verbose:
        logger = logger_init(level=logging.DEBUG)
    else:
        logger = logger_init()

    logger.info(f'Lets start! Url={ARGS.url}')

    main(url=ARGS.url, logger=logger, limit=ARGS.limit)


