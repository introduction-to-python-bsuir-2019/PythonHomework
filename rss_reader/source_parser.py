"""Contain all news parse related objects."""
import logging
import os
import urllib
from datetime import datetime
from html import unescape
from operator import itemgetter
from urllib.parse import urljoin, urlparse

from typing import Dict, List, Optional, Union

import bs4
import feedparser
from dateutil import parser
from feedparser import FeedParserDict
from bs4.element import Tag, NavigableString

from rss_reader.exceptions import RSSReaderParseException


class SourceParser:
    """Class parse data of source RSS."""

    def __init__(self, source: str) -> None:
        """Initialze RSS source parser."""
        self._source = source
        self._empty_published = datetime.now()
        self.__news = {'title': '', 'published': '', 'link': '', 'text': '', 'links': []}
        self.__cache_news = {'source': source, 'feed': '', 'id': '', 'date': self._empty_published, 'news': {}}
        self.cache_data = []

    def parse_source_data(self, source_data: FeedParserDict) -> None:
        """Parse RSS source link data into a dictionary with feed title and list of news."""
        def return_news() -> Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]:
            """Return news data structures."""
            news = self.__news.copy()
            news.update({'title': title,
                         'published': published,
                         'link': link,
                         'text': ' '.join(element for element in description.text),
                         'links': description.links,
                         'description': description.structure})
            return news

        def add_news_cache_data() -> None:
            """Add news cache data to parser data structures."""
            cache_news = self.__cache_news.copy()
            cache_update = {'id': cache_id, 'news': news}
            try:
                cashe_date = parser.parse(published).replace(tzinfo=None)
            except ValueError:
                cache_update.update({'date': self._empty_published})
            else:
                cache_update.update({'date': cashe_date})
            finally:
                cache_news.update(cache_update)
                self.cache_data.append(cache_news)

        logging.info('Start parse RSS source data')
        feed_title = unescape(source_data.get('feed', {}).get('title', ''))
        self.__cache_news.update({'feed': feed_title})
        for item in sorted(source_data.get('entries', []), key=itemgetter('published_parsed'), reverse=True):
            title = unescape(item.get('title', ''))
            link = urllib.parse.quote(item.get('link', ''), safe=':/')
            published = item.get('published', '')
            cache_id = item.get('id', '')
            description = DescriptionParser(link)
            description.parse_description(item.get('description'))
            news = return_news()
            add_news_cache_data()
        logging.info('RSS news has been parsed successfully')

    def get_source_data(self) -> FeedParserDict:
        """Parse source link RSS into dictionary."""
        source_data = feedparser.parse(self._source)
        if source_data.bozo == 1:
            raise RSSReaderParseException('Invalid or inaccessible RSS URL')
        logging.info('Successful get RSS data from RSS URL')
        return source_data


class DescriptionParser:
    """Class parse news description."""

    def __init__(self, news_link: str) -> None:
        """Initialze RSS description parser."""
        self.__element = {'text': '', 'type': '', 'link': ''}
        self._news_link = news_link
        link_parse = urlparse(news_link)
        self._host_name = os.path.join(f'{link_parse.scheme}://', link_parse.hostname)
        self.links = []
        self.text = []
        self.structure = []

    def parse_description(self, data: str) -> None:
        """Parse news description into well-formed text and list of links."""
        self._parse_description_data(bs4.BeautifulSoup(data, features='html.parser'))

    def _parse_description_data(self, data: Union[Tag, NavigableString], skip_text: Optional[bool] = False) -> None:
        """Parse tag to well-formed text."""
        for tag in data.childGenerator():
            if not skip_text and not tag.name and not tag.string.isspace():
                formated_text = self.format_string(unescape(tag.string))
                self.text.append(formated_text)
                self._update_structure({'text': formated_text, 'type': 'text'})
            elif tag.name == 'a':
                self._parse_description_tag(tag, 'href', 'link')
            elif tag.name == 'img':
                self._parse_description_tag(tag, 'src', 'image')
            if tag.name:
                self._parse_description_data(tag, tag.name in ('a', 'img'))

    def _parse_description_tag(self, tag: Tag, tag_attr: str, tag_type: str) -> None:
        """Parse link or image tag to well-formed text and add link or image link to list of links."""
        def control_last_link() -> None:
            """Remove last link if it led to an image embedded in this link."""
            last_link = self.links.pop()
            if not (last_link.get('type', '') == 'link' and last_link.get('link', '') == link):
                self.links.append(last_link)

        def get_tag_link() -> None:
            """Return tag link."""
            link = urllib.parse.quote(tag.attrs.get(tag_attr, ''), safe=':/')
            if not link or self._news_link == link:
                return None
            elif not urlparse(link).hostname:
                link = urljoin(self._host_name, link)
            return link

        link = get_tag_link()
        if not link:
            return
        if tag_type == 'image' and self.links:
            control_last_link()
        self.links.append({'link': link, 'type': tag_type})
        tag_number = len(self.links)
        tag_text = self.format_string(unescape(str(tag.string or ''))).strip()
        self.text.append('{0}{1}'.format(f'[{tag_type} {tag_number}',
                                         f': {tag_text}][{tag_number}]' if tag_text else ']'))
        self._update_structure({'text': tag_text, 'type': tag_type, 'link': link})

    def _update_structure(self, element_structure: Dict[str, str]) -> None:
        """Update description structure."""
        element = self.__element.copy()
        element.update(element_structure)
        self.structure.append(element)

    @staticmethod
    def format_string(string: str) -> str:
        """Format a string to string with one space between words."""
        return ' '.join(string.split())
