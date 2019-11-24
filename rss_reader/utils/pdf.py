import bs4
from copy import deepcopy
from fpdf import FPDF
from logging import Logger

import urllib
from pathlib import Path
import tempfile

from ..utils.IConverter import IConverter
from ..utils.data_structures import News
from ..utils.exceptions import RssException


class PdfWriter(IConverter):
    def __init__(self, logger: Logger):
        self.row_space = 5
        self.font_size = 10
        self.page_width = 162
        self.pdf = FPDF()
        self.pdf.add_font('DejaVu', '', Path('utils/dejavu_font/DejaVuSansCondensed.ttf').as_posix(), uni=True)
        self.pdf.set_font('DejaVu', '', self.font_size)
        self.pdf.add_page()
        super().__init__(logger)

    def store_news(self, news: News, path_to_file: str) -> None:
        """Converts News obj to pdf and stores it to path_to_file"""
        self.logger.debug('Start pdf converter')
        news_items_ = deepcopy(news.items)

        self._add_feed_header_to_pdf(news.feed, news.link)

        for news_number, item in enumerate(news_items_):

            self.pdf.cell(w=0, h=15,  txt=f'[{news_number + 1}]', align='C', ln=self.row_space)

            news_title = f'Title: {item.title}\n' \
                         f'Date: {item.published}\n' \
                         f'Link: {item.link}\n'

            self._add_txt_to_pdf(news_title)

            links = item.links
            imgs = item.imgs

            html = bs4.BeautifulSoup(item.html, "html.parser")

            for tag in html.descendants:
                if tag.name == 'a':
                    link = tag.attrs.get('href', '')
                    if link not in links:
                        links.append(link)
                    self._add_txt_to_pdf(link)

                elif tag.name == 'img':
                    src = tag.attrs.get('src', '')
                    if src not in imgs:
                        imgs.append(src)
                    self._add_img(tag)

            news_body = f'{html.getText()}\n'

            self._add_txt_to_pdf(news_body)

            self._text_color_green()
            self._add_txt_to_pdf('Links:', align='center')
            self._text_color_black()

            self._add_txt_to_pdf('\n'.join([f'[{i + 1}]: {link} (link)' for i, link in enumerate(links)]) + '\n')

            self._add_txt_to_pdf('\n'.join([f'[{i + len(links) + 1}]: '
                                            f'{link} (image)' for i, link in enumerate(imgs)]) + '\n')

            self._add_line()

        self.logger.info('Pdf creation has finished')
        try:
            self.pdf.output(Path(path_to_file))
        except Exception as ex:
            raise RssException(f'Something went wrong while generating and storing pdf file\n{ex}')

        self.logger.debug('End pdf converter')

    def _add_feed_header_to_pdf(self, feed: str, link: str) -> None:
        """Adds feed's title and link to the self.pdf obj"""

        self.pdf.cell(200, self.font_size + 4, txt=feed, ln=1, align="C", fill=0, border=1)
        self._text_color_blue()

        self.pdf.cell(200, self.font_size, txt=link, ln=1, align="C")
        self._text_color_black()

        self._add_line()

    def _add_txt_to_pdf(self, text: str, align='justify') -> None:
        """Splits a text by \n and print each row to pdf

        align can be: justify, center or none (left)
        """
        if align == 'justify':
            self.pdf.multi_cell(w=0, h=self.row_space, txt=text, align='J')
        elif align == 'center':
            self.pdf.multi_cell(w=0, h=self.row_space, txt=text, align='C')
        else:
            self.pdf.multi_cell(w=0, h=self.row_space, txt=text)

    def _add_line(self) -> None:
        """Adds a line with width length = self.page_width"""

        self._text_color_red()
        self.pdf.write(self.row_space, '-' * self.page_width)
        self.pdf.ln(self.row_space)
        self._text_color_black()

    def _add_img(self, tag: bs4.element.Tag) -> None:
        """Adds img to pdf obj

        Create an NamedTemporaryFile with .jpg suffix;
        get img's url;
        download img via urllib module;
        add downloaded img to pdf;
        """
        try:
            tf = tempfile.NamedTemporaryFile(suffix='.jpg', )
            path = Path(tf.name)
        except Exception as ex:
            self.logger.error('Temp file store error')
            raise RssException(f'Error while creating a temp file to store news img\n{ex}')

        with open(path, 'wb') as f:
            f.write(urllib.request.urlopen(tag.attrs.get('src', '')).read())

        self.pdf.image(path.as_posix(), w=0, h=0)
        self.pdf.ln(self.row_space)

    def _text_color_blue(self) -> None:
        """Set blue text color"""
        self.pdf.set_text_color(0, 0, 255)

    def _text_color_black(self) -> None:
        """Set black text color"""
        self.pdf.set_text_color(0, 0, 0)

    def _text_color_red(self) -> None:
        """Set red text color"""
        self.pdf.set_text_color(255, 0, 0)

    def _text_color_green(self) -> None:
        """Set green text color"""
        self.pdf.set_text_color(0, 255, 0)
