import argparse as argp
import logging as log
import sys

from rss import rss_feed


class Application:
    """app class"""

    def __init__(self):
        """Parsing arguments"""
        parser = argp.ArgumentParser(description='Python command-line RSS reader.')
        parser.add_argument('source', help='Enter the link to the information portal(RSS url)', type=str)
        parser.add_argument('--version', help='Print version info', action='version', version='1.0')
        parser.add_argument('--json', help='Print result as JSON in stdout', action='store_true')
        parser.add_argument('--verbose', help='Outputs verbose status messages', action='store_true')
        parser.add_argument('--limit', help='Limit news topics if this parameter is provided', type=int)
        self.dict_args = vars(parser.parse_args())
        log.info(f'Init class Application')

    @staticmethod
    def init_config_log():
        log.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=log.INFO)
        log.info(f'The init_config_log method worked')

    def run_app(self):
        log.info(f'Run app')
        feed = rss_feed.RSSFeed(self.dict_args)
        feed.receiving_rss_data()
        feed.rss_data_processing()
        if self.dict_args["verbose"]:
            feed.print_log()
            log.info(f'Close application')
            sys.exit(1)
        if self.dict_args["json"]:
            feed.convert_rss_to_json()
        else:
            feed.print_rss()
        log.info(f'The run_app method worked')
