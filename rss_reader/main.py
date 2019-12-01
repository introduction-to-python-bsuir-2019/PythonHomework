import argparse
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

from rss_reader.feed_parser import FeedParser
from rss_reader.printer import Printer
from rss_reader.exceptions import RSS_reader_error, SourceConnectingError, ArgError
from rss_reader.cache import CacheHandler
from rss_reader.converters import FormatsConverter

APP_VERSION = '3.0'


class RSS_reader:
    """Main programm class"""
    def __init__(self, source, limit=None, json_mode=False, date=None, html_file_path=None, fb2_file_path=None):
        self.source = source
        self.limit = limit
        self.json_mode = json_mode
        self.html_file_path = html_file_path
        self.fb2_file_path = fb2_file_path

        self.parser = FeedParser()
        self.printer = Printer()
        self.coverter = FormatsConverter()
        self.logger = logging.getLogger('rss_reader.RSS_reader')
        self.cache = CacheHandler(Path().home().joinpath('.rss'))
        if date:
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

        if self.html_file_path:
            self.coverter.convert_to_html(self.feed, self.html_file_path, self.limit)
        elif self.fb2_file_path:
            self.coverter.convert_to_fb2(self.feed, self.fb2_file_path, self.limit)
        else:
            self.print_feed()

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

    def get_feed_cache(self):
        "Get cached articles from DB"
        self.feed = self.cache.load_articles(self.source, self.date)
        if not self.limit:
            self.limit = len(self.feed['articles']) + 1

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
    cmd_arg_parser.add_argument('--to-html', dest='to_html', type=str, help='Write RSS feed in html file by path')
    cmd_arg_parser.add_argument('--to-fb2', dest='to_fb2', type=str, help='Write RSS feed to fb2 by path')
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
    try:
        if cmd_args.to_html and not Path(cmd_args.to_html).exists():
            raise ArgError(f'Invalid path "{cmd_args.to_html}"')
        if cmd_args.to_fb2 and not Path(cmd_args.to_fb2).exists():
            raise ArgError(f'Invalid path "{cmd_args.to_fb2}"')
        reader = RSS_reader(cmd_args.source,
                            limit=cmd_args.limit,
                            json_mode=cmd_args.json,
                            html_file_path=cmd_args.to_html,
                            fb2_file_path=cmd_args.to_fb2)
        reader.get_feed()
    except RSS_reader_error as e:
        print(e.msg)
        sys.exit(1)


if __name__ == "__main__":
    main()
