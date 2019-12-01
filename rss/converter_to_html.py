"""This module converts news to HTML and fb2 and saves."""

import os
import logging

from bs4 import BeautifulSoup
from lxml import html
from lxml import etree
from lxml.builder import E


class HTMLConverter:
    """Class provides work with conversation to HTML."""

    def __init__(self, path='rss-news.html'):
        logging.info('HTMLConverter initialization')
        self.path = path

    def convert_to_html(self, list_of_news, list_of_row_descriptions):
        """Return news converted into HTML."""

        logging.info('Start conversion to HTML')
        page = (
            E.html(
                E.head(E.title("RSS news")),
            )
        )

        for single_news, single_description in \
                zip(list_of_news, list_of_row_descriptions):
            logging.info('Convert one news')
            page.append(E.P(
                E.center(E.h2(single_news['title'])),
                E.h2(E.a(single_news['link'], href=single_news['link'])),
                E.h4(single_news['date']),
            ))
            page.append(html.fromstring(single_description))
            page.append(E.BR())
            page.append(E.BR())
            page.append(E.HR())
        return page

    def save_html(self, html_news):
        """Save HTML converted news on the received path."""

        logging.info('Save HTML converted news')
        with open(self.path, 'w') as file:
            file.write(html.tostring(html_news,
                                     pretty_print=True,
                                     encoding='unicode',
                                     method='html',
                                     doctype='<!DOCTYPE html>'))
