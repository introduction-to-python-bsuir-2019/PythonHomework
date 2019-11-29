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

        for news_number, item in enumerate(news_items_):

            page.append(E.CENTER(f'[{news_number + 1}]'))
            page.append(E.P(
                E.H3(f'Title: {item.title}'),
                E.H4(f'Link:'), E.A(f'{item.link}', href=item.link),
                E.H4(f'Published: {item.published}'),
            ))

            page.append(
                html.fromstring(item.html)
            )
            page.append(E.BR())
            page.append(E.BR())
            page.append(E.HR())

        with open(Path(path_to_file), 'w') as f:
            f.write(html.tostring(page,
                                  pretty_print=True,
                                  encoding='unicode',
                                  method='html',
                                  doctype='<!DOCTYPE html>'))

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
