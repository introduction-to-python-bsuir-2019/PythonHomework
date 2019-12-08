"""This module contain class representing cli optional argument"""

from src.components.parser.arguments import ArgumentsAbstract
import argparse


class Json(ArgumentsAbstract):
    """This class representing implementation of ArgumentsAbstract
    interface and init a optional Json for json output parameter"""

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add Json parameter from console for json output
        :return: argparse
        """
        self._parser.add_argument(
            '--json', action='store_true', help='Print result as JSON in stdout'
        )
