"""Module contains objects related to arguments parsing"""
import logging
from typing import Dict, Any
import argparse

from rss_reader_ft.config import __version__


class ArgumentParser:
    """ArgumentParser class"""

    @staticmethod
    def parse_args() -> Dict[str, Any]:
        """
        The method in which we set the parser,
        indicate what objects we expect from it,
        and return the dictionary
        """
        parser = ErrorCatchingArgumentParser(description='Python command-line RSS reader.')
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
        parser.add_argument(
            '--date',
            help='The cashed news can be read with it. The new from the specified day will be printed out.\
                  If the news are not found return an error.',
            type=int
        )
        parser.add_argument(
            '--to-html',
            help='Print result as HTML file',
            action='store_true'
        )
        parser.add_argument(
            '--to-pdf',
            help='Print result as PDF file',
            action='store_true'
        )
        parser.add_argument(
            '--colorize',
            help='Add color for print',
            action='store_true'
        )
        logging.info('Parsed arguments')
        return vars(parser.parse_args())


class ArgParserError(Exception):
    """The exception class"""

    def __init__(self, message):
        self.message = message


class ErrorCatchingArgumentParser(argparse.ArgumentParser):
    """Overloading method error()"""

    def error(self, message) -> None:

        raise ArgParserError('Ooops.. Error))) check link and arguments (-h)')
