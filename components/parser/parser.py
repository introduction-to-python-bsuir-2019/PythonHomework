import importlib
import argparse
import os

from .arguments.version import Version

class Parser:

    _arguments_list = (
        'version',
    )

    # @property
    # def _parser(self):
    #     return self._parser
    #
    # @_parser.setter
    # def _parser(self, description):
    #     self._parser = argparse.ArgumentParser(description)

    def __init__(self, description, **kwargs):
       self._parser = argparse.ArgumentParser(description)
       self.init_arguments()
       self._parser.parse_args()

    def init_arguments(self):
        Version(self._parser).add_argument()
        # for argument in self._arguments_list:
        #     module = importlib.import_module(
        #         '.arguments.version', '.'
        #     )
        #     argument_class = getattr(module, argument)
        #     instance = argument_class(self._parser).add_argument()

