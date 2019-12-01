"""This module contain class representing cli optional argument"""

from src.components.parser.arguments import ArgumentsAbstract
import argparse


class Verbose(ArgumentsAbstract):
    """This class representing implementation of ArgumentsAbstract
    interface and init a optional Verbose parameter"""

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add Verbose parameter from console for output verbose data
        :return: argparse
        """
        self._parser.add_argument(
            '--verbose', default=False, action='store_true', help='Outputs verbose status messages'
        )

