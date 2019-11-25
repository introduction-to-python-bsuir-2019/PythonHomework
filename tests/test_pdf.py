"""
Pdf tester file
"""
import fpdf
import os
import unittest
from fpdf import FPDF
from unittest.mock import patch
from pathlib import Path

from rss_reader.rss import logger_init
from rss_reader.bots import default
from rss_reader.utils.data_structures import ConsoleArgs
from rss_reader.utils.pdf import PdfWriter


class TestMainModule(unittest.TestCase):
    def setUp(self) -> None:
        url_google = './tests/data/google_news.xml'

        args = ConsoleArgs(
            url=url_google,
            limit=1,
        )
        self.bot_google = default.Bot(args, logger=logger_init())

    def test_bot_limit(self):
        self.assertEqual(self.bot_google.limit, 1)

    def test_pdf_and_html_writers(self):
        file_pdf_path = Path('tests/data/test.pdf')
        file_html_path = Path('tests/data/test.html')
        ttf_pickle_files_to_remove = Path('rss_reader/utils/dejavu_font/').glob('**/*.pkl')
        PdfWriter.djvu_font_path = Path('rss_reader/utils/dejavu_font/DejaVuSansCondensed.ttf')

        for pkl in ttf_pickle_files_to_remove:
            os.remove(pkl)

        url_google = Path('tests/data/google_news.xml')
        args = ConsoleArgs(
            url=url_google,
            limit=1,
            to_pdf=file_pdf_path.as_posix(),
            to_html=file_html_path.as_posix(),
        )
        bot_google = default.Bot(args, logger=logger_init())
        bot_google.print_news()

        with open(file_pdf_path, 'rb') as f:
            self.assertEqual(len(f.read()), 16649)

        with open(file_html_path, 'r') as f:
            self.assertEqual(len(f.read()), 3718)
