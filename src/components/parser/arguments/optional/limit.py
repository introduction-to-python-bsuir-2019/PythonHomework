"""This module contain class representing cli optional argument"""

from src.components.parser.arguments import ArgumentsAbstract
import argparse


class Limit(ArgumentsAbstract):
    """This class representing implementation of ArgumentsAbstract
    interface and init a optional Json for json output parameter"""

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add Limit parameter from console for limit feed entries
        :return: argparse
        """
        self._parser.add_argument(
            '--limit', type=self._validate_limit, default=3, help='Limit news topics if this parameter provided'
        )

    def _validate_limit(self, limit: int) -> int:
        """
        This method validate incoming optional limit parameter on equals to zero or less
        :param limit: int
        :return: int
        """
        try:
            if not int(limit) > 0:
                raise argparse.ArgumentTypeError

            return int(limit)

        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError('Argument limit equal or less 0')
