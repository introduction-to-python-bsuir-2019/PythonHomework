import requests
import argparse
import logging
import os

from feed_parser import FeedParser
from printer import Printer
from exceptions import SourceConnectingError


APP_VERSION = '1.0'


class RSS_reader:
    ''' Main programm class '''
    def __init__(self, cmd_args):
        self.source = cmd_args.source
        self.limit = cmd_args.limit or None
        self.json_mode = cmd_args.json or False
        self.parser = FeedParser()
        self.printer = Printer()
        self.logger = logging.getLogger('rss_reader.RSS_reader')

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
        if not self.limit:
            self.limit = len(self.feed['articles']) + 1

    def print_feed(self):
        if self.json_mode:
            self.printer.json_print(self.parser.get_json_feed(self.limit))
        else:
            self.printer.stdout_print(self.feed, self.limit)


def main():
    cmd_arg_parser = argparse.ArgumentParser(description='Pure Python comandline RSS reader')
    cmd_arg_parser.add_argument('source', help='RSS URL')
    cmd_arg_parser.add_argument('--version', help='Print version info',
                                action='version', version=f'RSS reader v{APP_VERSION} by Alex_Yan')
    cmd_arg_parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
    cmd_arg_parser.add_argument('--limit', type=int, help='Limit news topics if this parameter privided')
    cmd_arg_parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
    cmd_args = cmd_arg_parser.parse_args()

    log_handlers = [
        logging.FileHandler('rss_reader.log'),
    ]
    if cmd_args.verbose:
        log_handlers.append(logging.StreamHandler())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=log_handlers)

    reader = RSS_reader(cmd_args)
    reader.get_feed_from_source()
    reader.print_feed()
    

if __name__ == "__main__":
    main()
