"""Application entry point module"""
import argparse
import logging
import sys
from datetime import datetime

from rssreader import conf
from rssreader.base import BaseClass
from rssreader.feed import Feed


class Application(BaseClass):
    """Main application class"""

    def __init__(self) -> None:
        """Parse provided arguments to be used for application initialization"""

        def valid_date(val: str) -> datetime:
            try:
                return datetime.strptime(val, '%Y%m%d').date()
            except ValueError:
                raise argparse.ArgumentTypeError(f'Invalid date: {val}')

        parser = argparse.ArgumentParser(prog=conf.__package__, description='Pure Python command-line RSS reader.')
        parser.add_argument('source', help='RSS URL', type=str)
        parser.add_argument('--version', help='Print version info', action='version', version='%(prog)s {0}'.
                            format(conf.__version__))
        parser.add_argument('--json', help="Print result as JSON in stdout", action='store_true')
        parser.add_argument('--verbose', help="Outputs verbose status messages", action='store_true')
        parser.add_argument('--limit', help='Limit news topics if this parameter is provided', type=int)
        parser.add_argument('--date', help='Return cached news from the specified day. Format is YYYYMMDD.',
                            type=valid_date)
        self.settings = parser.parse_args()
        self._init_verbose_mode()
        logging.info(f'Initial arguments of the application are ({self.settings})')

    def _init_verbose_mode(self):
        """Initialize verbose mode. Log level is set to INFO."""
        if self.settings.verbose:
            logging.basicConfig(format='%(asctime)s %(module)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)

    def run(self) -> None:
        """Run the application: process feed and print results"""
        logging.info(f'Run the application')
        feed = Feed(self.settings.source, self.settings.limit, self.settings.date)

        if self.settings.date is None:
            feed.request()
        else:
            feed.load_from_cache()
            if len(feed.news) == 0:
                raise Exception(f'There is no cached news on this source published from {self.settings.date}.')

        feed.print(self.settings.json)


def main() -> None:
    """Entry point function to start the application"""
    try:
        app = Application()
        app.run()
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
