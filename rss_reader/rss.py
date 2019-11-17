"""
Main module. Launches the rss reader and output the result
"""
import argparse
import getpass
import logging
import sys
from importlib import import_module

from .utils import RssInterface
from .utils.RssInterface import RssException
from .utils.DataStructures import ConsoleArgs

PROG_VERSION = 2.0


def logger_init(level=None):
    """Logger initialisation

    All logs are printed into ./main.log file
    Other logs in regards of the 'level' are printed into console
    """

    level = level or logging.CRITICAL
    logger = logging.getLogger(getpass.getuser())
    logger.setLevel(level=level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Logging into file
    fh = logging.FileHandler("main.log", encoding="utf-8")  # 6
    fh.setLevel(logging.INFO)  # 7
    fh.setFormatter(formatter)

    # Logging into console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # logger.addHandler(fh)
    logger.addHandler(console_handler)
    return logger


def get_bot_instance(url: str, logger: logging.Logger) -> RssInterface:
    """
    Choosing an appropriate bot to the url
    :param url: url, contained rss feed
    :return: Bot class inherited from RssInterface, appropriate to the url
    """
    if url.find('news.yahoo.com/rss') + 1:
        bot = import_module('rss_reader.bots.yahoo').Bot
        logger.info('Yahoo bot is loaded')
    elif url.find('news.tut.by/rss') + 1:
        bot = import_module('rss_reader.bots.tut').Bot
        logger.info('Tut.by bot is loaded')
    else:
        bot = import_module('rss_reader.bots.default').Bot
        logger.info('Default bot is loaded')
    return bot


def args_parser() -> ConsoleArgs:
    """Parsing console args and returning args class"""

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
                        version=f'%(prog)s {PROG_VERSION}'
                        )
    PARSER.add_argument('--width',
                        help='Define a screen width to display news',
                        default=120,
                        type=int,
                        )

    ARGS = PARSER.parse_args()

    return ConsoleArgs(
        url=ARGS.url,
        limit=ARGS.limit,
        width=ARGS.width,
        json=ARGS.json,
        verbose=ARGS.verbose,
    )


def main() -> None:
    """
     Main func calls rss reader

    :return: None
    """
    # url: str, limit: int, width: int, json: bool, verbose: bool
    args = args_parser()
    # Logger initialisation depends on verbose param
    if args.verbose:
        logger = logger_init(level=logging.DEBUG)
    else:
        logger = logger_init()

    logger.info(f'Lets start! Url={args.url}')

    # Get appropriate to the url bot class
    bot = get_bot_instance(args.url, logger)

    try:
        rss_reader = bot(url=args.url, limit=args.limit, logger=logger, width=args.width)
        if args.json:
            news = rss_reader.get_json()
        else:
            news = rss_reader.get_news()
    except RssException as ex:
        print(ex.args[0])

    except Exception as ex:
        print(f'Unhandled exception!\n{ex}\nExiting...')
    else:
        print(news)


if __name__ == "__main__":
    main()
