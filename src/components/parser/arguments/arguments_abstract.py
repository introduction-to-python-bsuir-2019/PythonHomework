from abc import ABC, abstractmethod
from pathlib import Path
import argparse


class ArgumentsAbstract(ABC):

    def __init__(self, parser):
        self._parser = parser

    @abstractmethod
    def add_argument(self):
        pass

    def _validate_converter_path(self, path):

        if not Path(path).suffix in self._extensions:
            raise argparse.ArgumentTypeError(
                f'Wrong extension type. Proper extension\\s: {", ".join(self._extensions)}'
            )

        try:
            return Path(path)

        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError(f'Invalid provided path: {path}')
