"""Contain all news parse related objects."""
from datetime import datetime
from html import unescape
from logging import info as logging_info
from operator import itemgetter

from typing import Dict, List, Optional, Union

from bs4 import BeautifulSoup
from dateutil import parser
from feedparser import parse, FeedParserDict
from bs4.element import Tag, NavigableString

from rss_reader.exceptions import RSSReaderParseException


class SourceParser:
    """Class parse data of source RSS."""

    def __init__(self, source: str) -> None:
        """Initialze RSS source parser."""
        self.__source = source
        self.__empty_published = datetime.now()
        self.__news = {'title': '', 'published': '', 'link': '', 'text': '', 'links': []}
        self.__cache_news = {'source': source, 'feed': '', 'id': '', 'date': self.__empty_published, 'news': {}}
        self.__coversation_news = {'title': '', 'published': '', 'link': '', 'description': []}
        self.news_data = {'feed': '', 'news': []}
        self.cache_data = []
        self.conversion_data = {'feed': '', 'news': []}

    def parse_source_data(self, source_data: FeedParserDict) -> None:
        """Parse RSS source link data into a dictionary with feed title and list of news."""
        def add_feed_title() -> None:
            """Add feed title to parser data structures."""
            self.news_data.update({'feed': feed_title})
            self.__cache_news.update({'feed': feed_title})
            self.conversion_data.update({'feed': feed_title})

        def add_news_display_data() -> Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]:
            """Add news display data to parser data structures."""
            news = self.__news.copy()
            news.update({'title': title,
                         'published': published,
                         'link': link,
                         'text': unescape(' '.join(element for element in description.text)),
                         'links': description.links})
            news_list.append(news)
            return news

        def add_news_cache_data() -> None:
            """Add news cache data to parser data structures."""
            cache_news = self.__cache_news.copy()
            cache_update = {'id': cache_id, 'news': news}
            try:
                cashe_date = parser.parse(published).replace(tzinfo=None)
            except ValueError:
                cache_update.update({'date': self.__empty_published})
                pass
            else:
                cache_update.update({'date': cashe_date})
            finally:
                cache_news.update(cache_update)
                self.cache_data.append(cache_news)

        def add_news_conversion_data() -> None:
            """Add news conversion data to parser data structures."""
            conversion_news = self.__coversation_news.copy()
            conversion_news.update({'title': title,
                                    'published': published,
                                    'link': link,
                                    'description': description.structure})
            conversion_list.append(conversion_news)

        logging_info('Start parse RSS source data')
        feed_title = unescape(source_data.get('feed', {}).get('title', ''))
        add_feed_title()
        news_list = []
        conversion_list = []
        for item in sorted(source_data.get('entries', []), key=itemgetter('published'), reverse=True):
            title = unescape(item.get('title', ''))
            link = item.get('link', '')
            published = item.get('published', '')
            cache_id = item.get('id', '')
            description = DescriptionParser()
            description.parse_description(item.get('description'))
            news = add_news_display_data()
            add_news_cache_data()
            add_news_conversion_data()
            logging_info(f'Successful get {len(news_list)} RSS news items from RSS feed')
        self.news_data.update({'news': news_list})
        self.conversion_data.update({'news': conversion_list})
        logging_info('RSS news has been parsed successfuly')

    def get_source_data(self) -> FeedParserDict:
        """Parse source link RSS into dictionary."""
        source_data = parse(self.__source)
        if source_data.bozo == 1:
            raise RSSReaderParseException('Invalid or inaccessible RSS URL')
        logging_info('Successful get RSS data from RSS URL')
        return source_data


class DescriptionParser:
    """Class parse news description."""

    def __init__(self) -> None:
        """Initialze RSS description parser."""
        self.__element = {'text': '', 'type': '', 'link': '', 'number': 0}
        self.links = []
        self.text = []
        self.structure = []

    def parse_description(self, data: str) -> None:
        """Parse news description into well-formed text and list of links."""
        self._parse_description_data(BeautifulSoup(data, features='html.parser'))

    def _parse_description_data(self, data: Union[Tag, NavigableString], skip_text: Optional[bool] = False) -> None:
        """Parse tag to well-formed text."""
        for tag in data.childGenerator():
            if not skip_text and not tag.name and not tag.string.isspace():
                formated_text = self.format_string(tag.string)
                self.text.append(formated_text)
                self.__update_structure({'text': formated_text, 'type': 'text'})
            elif tag.name == 'a':
                self.__parse_description_tag(tag, 'href', 'link')
            elif tag.name == 'img':
                self.__parse_description_tag(tag, 'src', 'image')
            if tag.name:
                self._parse_description_data(tag, tag.name in ('a', 'img'))

    def __parse_description_tag(self, tag: Tag, tag_link: str, tag_type: str) -> None:
        """Parse link or image tag to well-formed text and add link or image link to list of links."""
        attrs_dict = dict(tag.attrs)
        link = attrs_dict.get(tag_link, '')
        link = link if link else 'Empty URL'
        self.links.append({'link': link, 'type': tag_type})
        tag_number = len(self.links)
        tag_title = attrs_dict.get('title', '')
        tag_string = str(tag.string or '')
        tag_text = '{0} {1}'.format(self.format_string(tag_title),
                                    self.format_string(tag_string)).strip()
        self.text.append('{0}{1}'.format(f'[{tag_type} {tag_number}',
                                         f': {tag_text}][{tag_number}]' if tag_text else ']'))
        self.__update_structure({'text': tag_text, 'type': tag_type, 'number': tag_number, 'link': link})

    def __update_structure(self, element_structure: Dict[str, Union[str, int]]) -> None:
        element = self.__element.copy()
        element.update(element_structure)
        self.structure.append(element)

    @staticmethod
    def format_string(string: str) -> str:
        """Format a string to string with one space between words."""
        return ' '.join(string.split())
