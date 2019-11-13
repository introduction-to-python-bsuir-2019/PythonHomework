import argparse


class ArgParser:
    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        argparser = argparse.ArgumentParser(description='One-shot command-line RSS reader')
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
        args = argparser.parse_args()
        return args

    def get_args(self):
        return self.args
