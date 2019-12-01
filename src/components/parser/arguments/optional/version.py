"""This module contain class representing cli optional argument"""

from .. import ArgumentsAbstract
import conf
import argparse


class Version(ArgumentsAbstract):
    """This class representing implementation of ArgumentsAbstract
    interface and init a optional Version parameter"""

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add Version parameter from console for output version of rss-reader
        :return: argparse
        """
        self._parser.add_argument(
            '-v', '--version', action='version', version=conf.__version__, help='Print version info'
        )
