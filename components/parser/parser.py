import argparse
import importlib


class Parser:

    _arguments_list = (
        'source',
        'version',
        'json',
        'verbose',
        'limit',
    )

    # @property
    # def _parser(self):
    #     return self._parser
    #
    # @_parser.setter
    # def _parser(self, description):
    #     self._parser = argparse.ArgumentParser(description)

    def __init__(self, description, usage, **kwargs):
       self._parser = argparse.ArgumentParser(description=description, usage=usage)
       self.init_arguments()
       self._parser.parse_args()

    def init_arguments(self):
        for argument in self._arguments_list:
            module = importlib.import_module('components.parser.arguments')
            argument_class = getattr(module, argument[0].upper() + argument[1:])
            argument_class(self._parser).add_argument()

