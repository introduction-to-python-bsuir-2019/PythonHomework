from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse
from pathlib import Path


class ToHtml(ArgumentsAbstract):

    def add_argument(self):
        self._parser.add_argument(
            '--to-html', type=self._validate_path, help='Convert to HTML format. Please provide path to file create'
        )

    def _validate_path(self, path):
        try:
            return Path(path)

        except argparse.ArgumentTypeError:
            raise argparse.ArgumentTypeError(f'Invalid provided path: {path}')
