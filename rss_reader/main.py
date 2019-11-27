import requests
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

from rss_reader.feed_parser import FeedParser
from rss_reader.printer import Printer
from rss_reader.exceptions import SourceConnectingError, ArgError
from rss_reader.cache import CacheHandler

APP_VERSION = '3.0'


class RSS_reader:
    ''' Main programm class '''
    def __init__(self, cmd_args):
        self.source = cmd_args.source
        self.limit = cmd_args.limit or None
        self.json_mode = cmd_args.json or False
        self.parser = FeedParser()
        self.printer = Printer()
        self.logger = logging.getLogger('rss_reader.RSS_reader')
        self.cache = CacheHandler(Path().home().joinpath('.rss'))
        if cmd_args.date:
            try:
                self.date = datetime.strptime(cmd_args.date, '%Y%m%d').date()
            except ValueError:
                self.logger.error('ArgError: Invalid date! The date should be in YYYYmmdd format.')
                raise ArgError('Invalid date! The date should be in "YYYYmmdd" format.')

        else:
            self.date = None

    def get_feed(self):
        if self.date:
            self.get_feed_cache()
        else:
            self.get_feed_from_source()

    def get_feed_from_source(self):
        '''Get rss xml file from source and parse by FeedParser'''
        try:
            self.logger.info(f'Connect to {self.source}')
            request = requests.get(self.source)
        except requests.ConnectionError:
            self.logger.error(f"Can't connect to '{self.source}'. Check URL and network connection.")
            raise SourceConnectingError(self.source, "Check URL and network connection.")
        except (requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
            self.logger.error("Invalid source URL.")
            raise SourceConnectingError(self.source, "Invalid source URL.")
        else:
            if not request.ok:
                self.logger.error(f"Can't get feed from '{self.source}', code: {request.status_code}")
                raise SourceConnectingError(self.source, f"code: {request.status_code}")

        self.feed = self.parser.parse(request.content)
        self.cache.dump_articles(self.feed, self.source)
        if not self.limit:
            self.limit = len(self.feed['articles']) + 1
        self.print_feed()

    def get_feed_cache(self):
        "Get cached articles from DB"
        self.feed = self.cache.load_articles(self.source, self.date)
        self.print_feed()

    def print_feed(self):
        if self.json_mode:
            self.printer.json_print(self.parser.get_json_feed(self.limit))
        else:
            self.printer.stdout_print(self.feed, self.limit)


def app_dir_init():
    "Initializing app work directory for db and logs"
    cache_dir = Path().home().joinpath('.rss')
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)


def main():
    cmd_arg_parser = argparse.ArgumentParser(description='Pure Python comandline RSS reader')
    cmd_arg_parser.add_argument('source', help='RSS URL')
    cmd_arg_parser.add_argument('--version', help='Print version info',
                                action='version', version=f'RSS reader v{APP_VERSION} by Alex_Yan')
    cmd_arg_parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    cmd_arg_parser.add_argument('--limit', type=int, help='Limit news topics if this parameter privided')
    cmd_arg_parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    cmd_arg_parser.add_argument('--date', type=str, help='Return new for requested date and source')
    cmd_args = cmd_arg_parser.parse_args()

    app_dir_init()

    log_handlers = [
        logging.FileHandler(Path.home().joinpath('.rss/rss_reader.log')),
    ]
    if cmd_args.verbose:
        log_handlers.append(logging.StreamHandler())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=log_handlers)

    reader = RSS_reader(cmd_args)
    reader.get_feed()


if __name__ == "__main__":
    main()
