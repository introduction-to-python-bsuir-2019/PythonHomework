"""Application main module."""
import argparse
import logging
from datetime import datetime
from sys import exit

from rss_reader.cache_storage import ReadCache, WriteCache
from rss_reader.config import NAME, VERSION
from rss_reader.display_news import DisplayNewsText, DisplayNewsJson
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
        def _cache_date(cache_date: str) -> datetime:
            try:
                return datetime.strptime(cache_date, '%Y%m%d')
            except ValueError:
                raise argparse.ArgumentTypeError(f'Incorrect cache date: {cache_date}')

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
                                     type=_cache_date)
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
            logging.info(error)
            exit('RSS reader has beed completed unsuccessfully')
        else:
            logging.info('RSS reader has beed completed successfully')

    def execute_rss_reader(self) -> None:
        """Execute RSS reader application."""
        logging.info('Data acquisition has been started')
        if self.arguments.date:
            read_cache = ReadCache(self.arguments.source, self.arguments.date)
            cache_data = read_cache.read_cache()
            logging.info('News reading from cache has been completed successfully')
            display_data = read_cache.format_data(cache_data)
        else:
            source_parser = SourceParser(self.arguments.source)
            source_data = source_parser.get_source_data()
            source_parser.parse_source_data(source_data)
            display_data = source_parser.news_data
            logging.info('Cache writing has been started')
            WriteCache(source_parser.cache_data).cache_news_list()
            logging.info('Cache writing has been finished')
        logging.info('Data acquisition has been finished')
        logging.info('Start display news from a RSS URL')
        if self.arguments.json:
            display_news = DisplayNewsJson(display_data, self.arguments.limit)
        else:
            display_news = DisplayNewsText(display_data, self.arguments.limit)
        display_news.set_news_limit()
        display_news.print_news()
        logging.info('End display news from a RSS URL')


def run() -> None:
    """Allow to run CLI apllication 'RSS reader' as 'rss-reader' in console. Uses in 'setup.py'."""
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()


if __name__ == '__main__':
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()
