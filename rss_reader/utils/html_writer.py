import bs4
import urllib
import tempfile

from copy import deepcopy
from lxml import html
from lxml.html import builder as E
from pathlib import Path

from ..utils.IConverter import IConverter
from ..utils.data_structures import News
from ..utils.exceptions import RssException


class HtmlWriter(IConverter):

    def store_news(self, news: News, path_to_file: str) -> None:
        """Converts News obj to html and stores it to path_to_file"""

        self.logger.debug('Start html converter')
        news_items_ = deepcopy(news.items)
        page = self._add_feed_header_to_html(news.feed, news.link)

        # page = E.HTML(
        #     E.HEAD(
        #         E.TITLE(f'{news.feed}')
        #     ),
        #     E.BODY(
        #         E.CENTER(E.H1(f'Title: {news.feed}'),),
        #
        #         E.P(E.H2('Link: '),
        #             E.A(f'{news.link}', href=news.link),
        #             ),
        #         E.HR(),
        #     )
        # )

        for news_number, item in enumerate(news_items_):

            page.append(E.CENTER(f'[{news_number}]'))
            page.append(E.P(
                E.H3(f'Title: {item.title}'),
                E.H4(f'Link:'), E.A(f'{item.link}', href=item.link),
                E.H4(f'Published: {item.published}'),
            ))
            # html_content = bs4.BeautifulSoup(item.html, "html.parser")
            page.append(
                html.fromstring(item.html)
            )
            page.append(E.BR())
            page.append(E.BR())
            page.append(E.HR())

        with open(Path(path_to_file), 'w') as f:
            f.write(html.tostring(page, pretty_print=True, encoding='unicode', method='html', doctype='<!DOCTYPE html>'))

        self.logger.debug('End html converter')

    def _add_feed_header_to_html(self, feed: str, link: str) -> html.Element:
        """Adds feed's title and link to the html page obj"""

        return E.HTML(
            E.HEAD(
                E.TITLE(f'{feed}')
            ),
            E.BODY(
                E.CENTER(E.H1(f'Title: {feed}'),),

                E.P(E.H2('Link: '),
                    E.A(f'{link}', href=link),
                    ),
                E.BR(), E.HR(),
            )
        )

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
