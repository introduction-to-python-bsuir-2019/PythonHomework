"""This module contain class representing cli optional argument"""

from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse


class ToHtml(ArgumentsAbstract):
    """
        This class representing implementation of ArgumentsAbstract interface
        and init a optional ToHtml parameter

        Attributes:
            _extensions attribute contains all permitted extension for this parameter
    """

    _extensions: list=['.html', '.htm']

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add ToHtml parameter from console for converter feeds entities into html
        :return: argparse
        """
        self._parser.add_argument(
            '--to-html', type=self._validate_converter_path,
            help='Convert to HTML format. Please provide path to file create'
        )

