"""Contain all news display related objects."""
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

import colorama
import jsonschema
from colorama import Fore

from rss_reader.config import JSON_SCHEMA
from rss_reader.containers import DictionaryValues
from rss_reader.exceptions import RSSNewsDisplayError


class DisplayNewsText:
    """Class display news in text format."""

    def __init__(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]],
                 colorize: Optional[bool] = False) -> None:
        """Initialze news displaing."""
        self._news_data = news_data
        self._colorize = colorize
        colorama.init()

    def print_news(self) -> None:
        """Print news in text format."""
        news_text = self._get_news_feed(self._news_data.get('feed', ''))
        for number, news in enumerate(self._news_data.get('news', []), start=1):
            news_text += self._get_news_text(number, news)
        print(news_text.rstrip())
        logging.info('All news have been printed in stdout in text format')

    def _get_news_feed(self, feed_title: str) -> str:
        """Format news feed title to correct text string."""
        return '{0}Feed: {2}:{1}\n\n'.format(
            Fore.GREEN if self._colorize else Fore.RESET,
            Fore.RESET,
            feed_title)

    def _get_news_text(self, number: int, news: Dict[str, Union[str, List[Dict[str, str]]]]) -> str:
        """Format news to correct text string."""
        links_values = DictionaryValues(news.get('links', {}))

        return '{7}[News: {0}]{6}\nTitle: {1}\nDate: {2}\nLink: {3}\n\n{4}\n\n{8}Links:{6}\n{5}\n\n'.format(
            number,
            news.get('title', ''),
            news.get('published', ''),
            news.get('link', ''),
            news.get('text', ''),
            ''.join(f'[{number}]: {link} ({key})\n' for number, (link, key) in enumerate(links_values, start=1)),
            Fore.RESET,
            Fore.RED if self._colorize else Fore.RESET,
            Fore.CYAN if self._colorize else Fore.RESET)


class DisplayNewsJson:
    """Class display news in json format."""

    def __init__(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Initialze news displaing."""
        self._news_data = news_data

    def print_news(self) -> None:
        """Print news in JSON format."""
        print(json.dumps(self._news_data, ensure_ascii=False, indent=4))
        logging.info('All news are printed in stdout in JSON format')

    def validate_json(self) -> None:
        """Validate news data through JSON schema."""
        schema = self.read_json_schema_file()
        try:
            jsonschema.Draft7Validator.check_schema(schema)
            jsonschema.Draft7Validator(schema).validate(self._news_data)
        except jsonschema.exceptions.SchemaError as error:
            raise RSSNewsDisplayError('Invalid JSON schema', error)
        except jsonschema.exceptions.ValidationError as error:
            raise RSSNewsDisplayError('Well-formed but invalid JSON', error)
        else:
            logging.info('Successful validation of JSON schema and data')

    @staticmethod
    def _read_json_schema_file() -> Dict[str, List[Dict[str, Any]]]:
        """Read JSON schema file and load them."""
        if not os.path.isfile(JSON_SCHEMA):
            raise RSSNewsDisplayError('Can\'t read json schema.')

        with open(JSON_SCHEMA, 'r') as schema_file:
            try:
                schema = json.load(schema_file)
            except json.decoder.JSONDecodeError as error:
                raise RSSNewsDisplayError('Poorly-formed text, not JSON', error)
            else:
                logging.info('Successful read and load JSON schema file')
                return schema


def format_to_display(data: List[Dict[Any, Any]]) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    """Format cache data do display data."""
    display_data = {'feed': '', 'news': []}
    news_temp = {'title': '', 'published': '', 'link': '', 'text': '', 'links': []}
    if data:
        display_data.update({'feed': next(iter(data)).get('feed', '')})
    news_list = []
    for feed_data in data:
        news_data = feed_data.get('news', {})
        news = news_temp.copy()
        news.update({'title': news_data.get('title', ''),
                     'published': news_data.get('published', ''),
                     'link': news_data.get('link', ''),
                     'text': news_data.get('text', ''),
                     'links': news_data.get('links', [])})
        news_list.append(news)
    display_data.update({'news': news_list})

    return display_data
