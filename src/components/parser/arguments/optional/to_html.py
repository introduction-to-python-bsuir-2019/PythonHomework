from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse

class ToHtml(ArgumentsAbstract):

    _extensions = ['.html', '.htm']

    def add_argument(self):
        self._parser.add_argument(
            '--to-html', type=self._validate_converter_path, help='Convert to HTML format. Please provide path to file create'
        )

