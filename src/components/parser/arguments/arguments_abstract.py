"""This module contain interface for implementation by cli utility params"""

from abc import ABC, abstractmethod
from pathlib import Path
import argparse


class ArgumentsAbstract(ABC):
    """
    This interface provided general data for implemented by argparse params
    """
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        """
        This interface constructor init argparse parser instance for further usage in options implementations
        :param parser: argparse.ArgumentParser
        """
        self._parser = parser

    @abstractmethod
    def add_argument(self) -> argparse:
        """This abstract method should be implemented for adding represented options"""
        pass

    def _validate_converter_path(self, path: str) -> Path:
        """
        This method validate incoming path for converter module on
        path extension and path valid
        :param path: str
        :return: Path
        """
        if not Path(path).suffix in self._extensions:
            raise argparse.ArgumentTypeError(
                f'Wrong extension type. Proper extension\\s: {", ".join(self._extensions)}'
            )

        try:
            return Path(path)

        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError(f'Invalid provided path: {path}')
