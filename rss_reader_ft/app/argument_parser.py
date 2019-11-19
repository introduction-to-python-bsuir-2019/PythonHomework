"""Module contains objects related to arguments parsing"""
import logging
from typing import Dict

import argparse

from rss_reader_ft.config import __version__


class ArgumentParser:
    """ArgumentParser class"""
    @staticmethod
    def parse_args() -> Dict:
        """
        The method in which we set the parser,
        indicate what objects we expect from it,
        and return the dictionary
        """
        parser = argparse.ArgumentParser(description='Python command-line RSS reader.')
        parser.add_argument(
            'source',
            help='Enter the link to the information portal(RSS url)',
            type=str
        )
        parser.add_argument(
            '--version',
            help='Print version info',
            action='version', version=__version__
        )
        parser.add_argument(
            '--json',
            help='Print result as JSON in stdout',
            action='store_true'
        )
        parser.add_argument(
            '--verbose',
            help='Outputs verbose status messages',
            action='store_true'
        )
        parser.add_argument(
            '--limit',
            help='Limit news topics if this parameter is provided',
            type=int
        )
        logging.info('Parsed arguments')
        return vars(parser.parse_args())
