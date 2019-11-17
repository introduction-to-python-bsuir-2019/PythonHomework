"""Application main module."""
import argparse
import logging
from sys import exit

from rss_reader.rss_news import RSSNews
from rss_reader.config import NAME, PACKAGE, VERSION


class RSSReader:
    """Application main class."""

    def __init__(self) -> None:
        """Initialze RSSReader class. Parses an arguments string and initialize verbose mode."""
        self.arguments = self._parse_arguments()
        if self.arguments.verbose:
            self._init_verbose()
        logging.info('Initialze RSS reader. Parameters: source = {0}; json = {1}; verbose = {2}; limit = {3}'.format(
                self.arguments.source,
                self.arguments.json,
                self.arguments.verbose,
                self.arguments.limit))

    @staticmethod
    def _parse_arguments() -> None:
        """Parse application arguments."""
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
            rss_parser = RSSNews(self.arguments.source, self.arguments.limit, self.arguments.json)
            rss_parser.display_news()
        except Exception as error:
            logging.info(error)
            exit('RSS reader has completed unsuccessfully')


def run() -> None:
    """Allow to run CLI apllication 'RSS reader' as 'rss-reader' in console. Uses in 'setup.py'."""
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()


if __name__ == '__main__':
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()
