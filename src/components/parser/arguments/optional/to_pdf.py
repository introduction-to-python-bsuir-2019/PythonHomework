from src.components.parser.arguments.arguments_abstract import ArgumentsAbstract
import argparse
from pathlib import Path


class ToPdf(ArgumentsAbstract):

    _extensions = ['.pdf']

    def add_argument(self):
        self._parser.add_argument(
            '--to-pdf', type=self._validate_converter_path, help='Convert to Pdf format. Please provide path to file create'
        )
