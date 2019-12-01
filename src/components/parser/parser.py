"""This module contain class for wrap Argparse"""

import argparse
import importlib


class Parser:
    """
        This class represents wrap on argparse for more convenient way to parse params and validate them

        Attributes:
            _arguments_list attribute contains all presenting cli options in utility
    """

    _arguments_list:  tuple=(
        'source',
        'version',
        'json',
        'verbose',
        'limit',
        'date',
        'colorize',
        'to_html',
        'to_pdf',
    )

    def __init__(self, description: str, usage: str) -> None :
        """
        This constructor implements, argparse module and init param from console
        :param description: str
        :param usage: str
        """
        self._parser = argparse.ArgumentParser(description=description, usage=usage)
        self._init_arguments()

    def get_args(self) -> argparse:
        """
        This method retrieve cli parameters and return them
        :return: argparse
        """
        return self._parser.parse_args()

    def _init_arguments(self) -> None:
        """
        This method load arparse parameters classes bound with _arguments_list list
        :return: None
        """
        module = importlib.import_module('src.components.parser.arguments')

        for argument in self._arguments_list:
            argument_class = getattr(module, self.to_camel_case(argument))
            argument_class(self._parser).add_argument()

    @staticmethod
    def to_camel_case(string: str) -> str:
        """
        This staticmethod help convert snake_case parameters to CamelCase for load classes
        :param string: str
        :return: str
        """
        parts = string.split('_')
        return parts[0].capitalize() + ''.join(part.title() for part in parts[1:])
