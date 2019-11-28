"""Application main module."""
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union
from sys import exit

from rss_reader.cache_storage import ReadCache, WriteCache
from rss_reader.config import NAME, VERSION
from rss_reader.display_news import DisplayNewsText, DisplayNewsJson, format_to_display
from rss_reader.exceptions import RSSReaderException
from rss_reader.format_converter import Converter, format_to_convert
from rss_reader.source_parser import SourceParser


class RSSReader:
    """Application main class."""

    def __init__(self) -> None:
        """Initialze RSSReader class. Parses an arguments string and initialize verbose mode."""
        self.arguments = self._parse_arguments()
        if self.arguments.verbose:
            self._init_verbose()
        logging.info('Successful initialze RSS reader')
        logging.info('Application arguments: source = {0}; json = {1}; verbose = {2}; limit = {3}'.format(
                self.arguments.source,
                self.arguments.json,
                self.arguments.verbose,
                self.arguments.limit))

    @staticmethod
    def _parse_arguments() -> None:
        """Parse application arguments."""
        def validate_date(cache_date: str) -> datetime:
            """Validate cache date for '--date' argument."""
            try:
                return datetime.strptime(cache_date, '%Y%m%d')
            except ValueError:
                raise argparse.ArgumentTypeError(f'Incorrect cache date: {cache_date}')

        def validate_file_path(path: str) -> str:
            try:
                file_path = Path(path)
                if os.path.isdir(file_path):
                    raise argparse.ArgumentTypeError(f'The path is a directory: {path}')
                elif os.path.islink(file_path):
                    raise argparse.ArgumentTypeError(f'The path is a link: {path}')
                else:
                    return file_path
            except TypeError:
                raise argparse.ArgumentTypeError(f'Invalid folder path: {path}')

        argument_parser = argparse.ArgumentParser(prog=NAME, description='Pure Python command-line RSS reader.')
        argument_parser.add_argument('source',
                                     help='RSS URL',
                                     type=str)
        argument_parser.add_argument('--version',
                                     help='Print version info',
                                     action='version',
                                     version='%(prog)s v{0}'.format(VERSION))
        argument_parser.add_argument('--json',
                                     help='Print result as JSON in stdout',
                                     action='store_true')
        argument_parser.add_argument('--verbose',
                                     help='Outputs verbose status messages',
                                     action='store_true')
        argument_parser.add_argument('--limit',
                                     help='Limit news topics if this parameter provided',
                                     type=int)
        argument_parser.add_argument('--date',
                                     help=r'Display cached news for the specified date (date format - \'YYYYmmDD\')',
                                     type=validate_date)
        argument_parser.add_argument('--to-html', dest='to_html',
                                     help="Convert news to HTML format and save '.html' file to the specified path.",
                                     type=validate_file_path)
        argument_parser.add_argument('--to-pdf', dest='to_pdf',
                                     help="Convert news to PDF format and save '.pdf' file to the specified path.",
                                     type=validate_file_path)
        argument_parser.add_argument('--colorize',
                                     help="Print text result in colorized mode",
                                     action='store_true')
        return argument_parser.parse_args()

    @staticmethod
    def _init_verbose() -> None:
        """Initialze verbose mode."""
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s | %(module)s]: %(message)s',
                            datefmt='%m.%d.%Y %H:%M:%S')

    def run_rss_reader(self) -> None:
        """Run RSS reader application."""
        logging.info('Run RSS reader')
        try:
            self.execute_rss_reader()
        except Exception as error:
            if not issubclass(type(error), RSSReaderException):
                RSSReaderException('Unidentified error', error)
            exit('RSS reader has beed completed unsuccessfully')
        else:
            logging.info('RSS reader has beed completed successfully')

    def execute_rss_reader(self) -> None:
        """Execute RSS reader application."""
        def get_news_data() -> List[Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]]:
            """Get news data from souce or from cache."""
            if self.arguments.date:
                read_cache = ReadCache(self.arguments.source, self.arguments.date)
                cache_data = read_cache.read_cache()
                logging.info('News reading from cache has been completed successfully')
            else:
                source_parser = SourceParser(self.arguments.source)
                source_data = source_parser.get_source_data()
                source_parser.parse_source_data(source_data)
                cache_data = source_parser.cache_data
            return cache_data

        def display_news_data() -> None:
            """Display news data in text or JSON formats."""
            display_data = format_to_display(news_data)
            if self.arguments.json:
                display_news = DisplayNewsJson(display_data)
            else:
                display_news = DisplayNewsText(display_data, self.arguments.colorize)
            display_news.print_news()

        def cache_news_data() -> None:
            """Cache news data to database."""
            WriteCache(self.arguments.source, cache_data).cache_news_list()

        def convert_news_data() -> None:
            """Cache news data to database."""
            conversion_data = format_to_convert(news_data)
            converter = Converter(conversion_data, self.arguments.to_html, self.arguments.to_pdf)
            converter.convert_news()

        logging.info('Data obtain has been started')
        cache_data = get_news_data()
        logging.info('Data obtain has been finished')
        if not cache_data:
            print('No news in the selected source with specified application parameters')
            return
        news_data = cache_data[:self.arguments.limit]
        logging.info('Start display news from a RSS URL')
        display_news_data()
        logging.info('End display news from a RSS URL')
        if self.arguments.to_html or self.arguments.to_pdf:
            logging.info('Start converting news')
            convert_news_data()
            logging.info('End converting news')
        if not self.arguments.date:
            logging.info('Cache writing has been started')
            cache_news_data()
            logging.info('Cache writing has been finished')


def run() -> None:
    """Allow to run CLI apllication 'RSS reader' as 'rss-reader' in console. Uses in 'setup.py'."""
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()


if __name__ == '__main__':
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()
