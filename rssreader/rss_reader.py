"""Application entry point module"""
import argparse
import logging
import sys
from datetime import datetime, date
from pathlib import Path

from termcolor import colored

from rssreader import conf
from rssreader.base import BaseClass
from rssreader.feed import Feed
from rssreader.converter import HTMLConverter, FB2Converter


class Application(BaseClass):
    """Main application class"""

    def __init__(self) -> None:
        """Initialize an application based on passed parameters"""
        self._parse_args()

        self._init_verbose_mode()
        logging.info(f'Initial arguments of the application are ({self.settings})')

        self._init_storage()

    def _parse_args(self):
        """Parse provided arguments to be used for application initialization"""
        def valid_date(val: str) -> date:
            try:
                return datetime.strptime(val, '%Y%m%d').date()
            except ValueError:
                raise argparse.ArgumentTypeError(f'Invalid date: {val}')

        def valid_file_path(val: str) -> Path:
            try:
                file_path = Path(val)
                if file_path.exists():
                    raise argparse.ArgumentTypeError('Another file with the same name already exists.')
                else:
                    return file_path
            except TypeError:
                raise argparse.ArgumentTypeError(f'Invalid file path: {val}')

        parser = argparse.ArgumentParser(prog=conf.__package__, description='Pure Python command-line RSS reader.')
        parser.add_argument('source', help='RSS URL', type=str)
        parser.add_argument('--version', help='Print version info', action='version', version='%(prog)s {0}'.
                            format(conf.__version__))
        parser.add_argument('--verbose', help="Output verbose status messages", action='store_true')
        parser.add_argument('--limit', help='Limit news topics if this parameter is provided', type=int)
        parser.add_argument('--date', help='Return cached news from the specified day. Format is YYYYMMDD.',
                            type=valid_date)
        group = parser.add_mutually_exclusive_group()
        group.add_argument('--json', help="Print result as JSON in stdout", action='store_true')
        group.add_argument('--to-html', dest='to_html',
                           help="Convert news to html format and save a file to the specified path.",
                           type=valid_file_path)
        group.add_argument('--to-fb2', dest='to_fb2',
                           help="Convert news to FictionBook2 format and save a file to the specified path.",
                           type=valid_file_path)
        parser.add_argument('--colorize', help="Print the result in colorized mode", action='store_true')
        self.settings = parser.parse_args()

    def _init_storage(self):
        """Initialize the local cache directory which is used to store downloaded data (like cached news and images)"""
        self.cache_dir = Path.home().joinpath('.rssreader')
        if self.cache_dir.exists():
            logging.info('Application local cache directory already exists')
        else:
            self.cache_dir.mkdir(parents=False)
            logging.info('Application local cache directory has been created')

    def _init_verbose_mode(self):
        """Initialize verbose mode. Log level is set to INFO."""
        if self.settings.verbose:
            logging.basicConfig(format='%(asctime)s %(module)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)

    def run(self) -> None:
        """Run the application: process feed and print results"""
        logging.info(f'Run the application')
        feed = Feed(self.settings.source, self.settings.limit, self.settings.date)

        if self.settings.date is None:
            feed.request(self.cache_dir)
        else:
            feed.load_from_cache(self.cache_dir)
            if len(feed.news) == 0:
                raise Exception(f'There is no cached news on this source published from {self.settings.date}.')

        if self.settings.to_html:
            HTMLConverter(self.cache_dir, Path(self.settings.to_html)).perform(feed)
        elif self.settings.to_fb2:
            FB2Converter(self.cache_dir, Path(self.settings.to_fb2)).perform(feed)
        else:
            feed.print(
                self.settings.json,
                paint=lambda text, color=None: colored(text, color, attrs=['bold']) if self.settings.colorize else text)


def main() -> None:
    """Entry point function to start the application"""
    try:
        app = Application()
        app.run()
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
