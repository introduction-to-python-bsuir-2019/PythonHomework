from src.components.parser.arguments import ArgumentsAbstract
import argparse
import sys

class Limit(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            '--limit', type=self._validate_limit, default=3, help='Limit news topics if this parameter provided'
        )

    def _validate_limit(self, limit):
        try:
            if not int(limit) > 0:
                raise argparse.ArgumentTypeError

            return int(limit)

        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError('Argument limit equal or less 0')
