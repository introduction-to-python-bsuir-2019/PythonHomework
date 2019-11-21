"""
    Contains ArgParser class which allows parse arguments from cmd
"""

import argparse


__version__ = '0.3.0'


class ArgParser:
    """ Reads arguments """

    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        """ Reads arguments from the cmd and returns them """

        argparser = argparse.ArgumentParser(description='One-shot command-line RSS reader', prog='rss-reader')
        argparser.add_argument(
            'url',
            type=str,
            help='Input RSS url containing news'
        )
        argparser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Sets a limit for news output (default - no limit)'
        )
        argparser.add_argument(
            '--json',
            action='store_true',
            help='Prints feed in JSON format in stdout'
        )
        argparser.add_argument(
            '--version',
            action='version',
            version=f'%(prog)s version {__version__}',
            default=None,
            help='Prints version of program'
        )
        argparser.add_argument(
            '--verbose',
            action='store_true',
            help='Prints all logs in stdout'
        )
        argparser.add_argument(
            '--date',
            type=str,
            help='It should take a date in %Y%m%d format. For example: --date 20191020'
                 'The new from the specified day will be printed out. If the news are not found error will be returned.'
        )
        args = argparser.parse_args()
        return args

    def get_args(self):
        """ Returns arguments """
        return self.args
