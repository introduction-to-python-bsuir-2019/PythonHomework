from src.components.parser.arguments import ArgumentsAbstract
from datetime import datetime
import argparse


class Date(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            '--date', type=self._validate_caching_date,
            help='Cached news from the specified date. YYYYMMDD is proper date format.'
        )

    def _validate_caching_date(self, date: str):
        try:
            return datetime.strptime(date, '%Y%m%d').date()
        except ValueError:
            raise argparse.ArgumentTypeError(f'Invalid date typed for caching: {date} \n Use YYYYMMDD format')
