"""Module which provides interface of translating news to .pdf."""
import logging
import os
import sys
from fpdf import FPDF
from image_handle import save_image_by_url

# from fpdf.py3k import PY3K

ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.to_pdf_converter'


TITLE_IMG_NAME = 'title.png'


class PDF(FPDF):
    """Class, which allows to translate news to .pdf format."""

    CLASS_LOGGER_NAME = MODULE_LOGGER_NAME + '.PDF'

    def set_meta_info(self, title: str, title_img_url: str) -> None:
        """Set information of rss-resource."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.set_meta_info')
        logger.info('Set information of rss-resource')

        self.title = title
        self.title_img_url = title_img_url

        self.iter = 0

    def _garbage_collect(self) -> None:
        """Remove temp img-files."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._garbage_collect')
        logger.info('Remove temp img-files')

        for index in range(self.iter):
            os.remove('temp' + str(index) + '.png')
        if self.title_img_url != '':
            os.remove(TITLE_IMG_NAME)

    def write_to_file(self, filepath: str) -> None:
        """Write to file pdf items."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.write_to_file')
        logger.info('Write to file pdf items')

        self._garbage_collect()
        self.output(filepath)

    def header(self) -> None:
        """Set header of each page."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.header')
        logger.info('Set header of each page')

        if self.title_img_url != '':
            save_image_by_url(self.title_img_url, TITLE_IMG_NAME)
            self.image(TITLE_IMG_NAME, 10, 8, 33)

        self.set_font("FreeSans", size=12)
        self.cell(100)
        self.cell(0, 5, txt=self.title)

        self.ln(10)

    def footer(self) -> None:
        """Set footer of each page."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.footer')
        logger.info('Set footer of each page')

        self.set_y(-10)

        self.set_font('FreeSans', size=8)

        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')

    def _add_title_of_news(self, title: str) -> None:
        """Insert title of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_title_of_news')
        logger.info('Insert title of piece of news')

        self.set_font('FreeSans', size=13)
        self.multi_cell(0, 10, txt=title, align='C')

    def _add_date_of_news(self, date: str) -> None:
        """Insert date of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_date_of_news')
        logger.info('Insert date of piece of news')

        self.set_font('FreeSans', size=12)
        self.multi_cell(0, 10, txt=date)

    def _add_link_of_news(self, link: str) -> None:
        """Insert link of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_link_of_news')
        logger.info('Insert link of piece of news')

        self.set_font('FreeSans', size=11)
        self.multi_cell(0, 10, txt=link)

    def _add_content_of_news(self, content: str) -> None:
        """Insert content of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_content_of_news')
        logger.info('Insert content of piece of news')

        self.set_font('FreeSans', size=12)
        self.multi_cell(0, 10, txt=content)

    def _add_img_of_news(self, img_url: str) -> None:
        """Insert image of piece of news."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '._add_img_of_news')
        logger.info('Insert image of piece of news')

        save_image_by_url(img_url, 'temp' + str(self.iter) + '.png')
        self.image('temp' + str(self.iter) + '.png', x=50, y=None, w=100, h=0)

        self.iter += 1

    def add_piece_of_news(self, title: str, date: str, link: str, img_url: str, content: str):
        """Insert piece of news to pdf."""
        logger = logging.getLogger(self.CLASS_LOGGER_NAME + '.add_piece_of_news')
        logger.info('Insert piece of news to pdf')

        self.alias_nb_pages()
        self.add_page()
        # self.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)

        self._add_title_of_news(title)
        self._add_date_of_news(date)
        self._add_link_of_news(link)
        if img_url != '':
            self._add_img_of_news(img_url)
        self._add_content_of_news(content)
