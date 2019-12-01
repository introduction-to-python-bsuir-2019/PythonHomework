"""This module contain class representing cli optional argument"""

from src.components.parser.arguments import ArgumentsAbstract
from datetime import datetime
import argparse


class Date(ArgumentsAbstract):
    """This class representing implementation of ArgumentsAbstract
    interface and init a optional Date for cache parameter"""

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add Date parameter from console for retrieving cache
        :return: argparse
        """
        self._parser.add_argument(
            '--date', type=self._validate_caching_date,
            help='Cached news from the specified date. YYYYMMDD is proper date format.'
        )

    def _validate_caching_date(self, date: str) -> datetime:
        """
        This method validate incoming optional date parameter on
        date format type
        :param date: str
        :return: datetime
        """
        try:
            return datetime.strptime(date, '%Y%m%d').date()
        except ValueError:
            raise argparse.ArgumentTypeError(f'Invalid date typed for caching: {date} \n Use YYYYMMDD format')
