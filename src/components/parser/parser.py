import argparse
import importlib


class Parser:

    _arguments_list = (
        'source',
        'version',
        'json',
        'verbose',
        'limit',
        'date',
        'colorize',
        'to_html',
    )

    def __init__(self, description, usage):
        self._parser = argparse.ArgumentParser(description=description, usage=usage)
        self._init_arguments()

    def get_args(self):
        return self._parser.parse_args()

    def _init_arguments(self):
        module = importlib.import_module('src.components.parser.arguments')

        for argument in self._arguments_list:
            argument_class = getattr(module, self.to_camel_case(argument))
            argument_class(self._parser).add_argument()

    @staticmethod
    def to_camel_case(string: str) -> str:
        parts = string.split('_')
        return parts[0].capitalize() + ''.join(part.title() for part in parts[1:])
