import argparse
import importlib


class Parser:

    _arguments_list = (
        'source',
        'version',
        'json',
        'verbose',
        'limit',
        'colorize',
    )

    def __init__(self, description, usage):
        self._parser = argparse.ArgumentParser(description=description, usage=usage)
        self._init_arguments()

    def get_args(self):
        return self._parser.parse_args()

    def _init_arguments(self):
        module = importlib.import_module('components.parser.arguments')

        for argument in self._arguments_list:
            argument_class = getattr(module, argument[0].upper() + argument[1:])
            argument_class(self._parser).add_argument()

