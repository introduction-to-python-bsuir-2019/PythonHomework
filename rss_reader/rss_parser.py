"""Contain all news parse related objects."""
from logging import info as logging_info
from html import unescape
from typing import Any, Dict, Optional, Union

from bs4 import BeautifulSoup
from feedparser import parse
from bs4.element import Tag, NavigableString

from rss_reader.containers import FormatSpaces
from rss_reader.exceptions import RSSReaderParseException


class RSSParser():
    """Class parse source RSS URL."""

    def __init__(self) -> None:
        """Initialze RSSParser class."""
        self._news = {'title': '', 'published': '', 'link': '', 'text': '', 'links': []}
        self.news_data = {'feed': '', 'news': []}
        logging_info('Initialze RSS parser')

    def get_news(self, source: str) -> None:
        """Parse source link RSS into a dictionary with feed title and list of news."""
        logging_info('Started get RSS news from RSS URL')
        rss_data = self._get_rss_data(source)
        self.news_data.update({'feed': unescape(rss_data.get('feed', {}).get('title', ''))})
        logging_info('Successful get RSS feed title')
        for item in rss_data.get('entries', []):
            description = RSSDescriptionParser()
            description.get_description(item.get('description'))
            self._news.update({'title': unescape(item.get('title', '')),
                               'published': unescape(item.get('title', '')),
                               'link': unescape(item.get('link', '')),
                               'text': unescape(description.text),
                               'links': description.links})
            news = self.news_data.get('news', [])
            news.append(self._news.copy())
            self.news_data.update({'news': news})
            logging_info(f'Successful get {len(news)} RSS news from items from RSS feed')
        logging_info('Ended get RSS news from RSS URL')

    @staticmethod
    def _get_rss_data(source: str) -> Dict[Any, Any]:
        """Parse source link RSS into dictionary."""
        rss_data = parse(source)
        if rss_data.bozo == 1:
            raise RSSReaderParseException('Invalid or inaccessible RSS URL')
        logging_info('Successful get RSS data from RSS URL')
        return rss_data


class RSSDescriptionParser():
    """Class parse news description."""

    def __init__(self) -> None:
        """Initialze RSSDescriptionParser class."""
        self.text = ''
        self.links = []
        logging_info('Initialze RSSDescriptionParser')

    def get_description(self, data: str) -> None:
        """Parse news description into well-formed text and list of links."""
        logging_info('Started get description')
        if not isinstance(data, str):
            raise RSSReaderParseException('Invalid description data')
        self._get_description_data(BeautifulSoup(data, features='html.parser'))
        self.text.strip()
        logging_info('Successful get a news description')

    def _get_description_data(self, data: Union[Tag, NavigableString], skip_text: Optional[bool] = False) -> None:
        """Parse tag to well-formed text."""
        for tag in data.childGenerator():
            if not skip_text and not tag.name and not tag.string.isspace():
                self.text += f'{self._format_string(tag.string)} '
            elif tag.name == 'a':
                self._get_description_tag(tag, 'href', 'link')
            elif tag.name == 'img':
                self._get_description_tag(tag, 'src', 'image')
            if tag.name:
                self._get_description_data(tag, tag.name in ('a', 'img'))

    def _get_description_tag(self, tag: Tag, tag_link: str, tag_type: str) -> None:
        """Parse link or image tag to well-formed text and add link or image link to list of links."""
        attrs_dict = dict(tag.attrs)
        self.links.append({'link': attrs_dict.get(tag_link, 'Empty URL'), 'type': tag_type})
        tag_number = len(self.links)
        tag_title = attrs_dict.get('title', '')
        tag_string = str(tag.string or '')
        tag_text = '{0} {1}'.format(self._format_string(tag_title), self._format_string(tag_string)).strip()
        self.text += '{0}{1} '.format(f'[{tag_type} {tag_number}', f': {tag_text}][{tag_number}]' if tag_text else ']')

    @staticmethod
    def _format_string(string: str) -> str:
        """Format a string to string with one space between words."""
        return FormatSpaces(str(string))
