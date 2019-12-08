"""This module contain class representing cli optional argument"""

from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse


class ToPdf(ArgumentsAbstract):
    """
        This class representing implementation of ArgumentsAbstract interface
        and init a optional Pdf parameter

        Attributes:
            _extensions attribute contains all permitted extension for this parameter
    """

    _extensions: list=['.pdf']

    def add_argument(self) -> argparse:
        """
        This method is implementation of add_argument abstract method
        add ToPdf parameter from console for converter feeds entities into pdf
        :return: argparse
        """
        self._parser.add_argument(
            '--to-pdf', type=self._validate_converter_path,
            help='Convert to Pdf format. Please provide path to file create'
        )
