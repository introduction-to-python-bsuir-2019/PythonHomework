"""Contain all news display related objects."""
import json as jsonmodule
from logging import info as logging_info
from os import path
from typing import Any, Dict, List, Optional, Union

import jsonschema

from rss_reader.config import JSON_SCHEMA
from rss_reader.containers import DictionaryValues
from rss_reader.exceptions import RSSNewsJSONSchemaException


class DisplayNews:
    """Class display news."""

    def __init__(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]],
                 limit: Optional[int] = 0) -> None:
        """Initialze news displaing."""
        self._limit = limit
        self._news_data = news_data

    def set_news_limit(self) -> None:
        """Set limit number of news."""
        news = self._news_data.get('news', [])[:self._limit]
        self._news_data.update({'news': news})


class DisplayNewsText(DisplayNews):
    """Class display news in text format."""

    def print_news(self) -> None:
        """Print news in text format."""
        news_text = 'Feed: {0}:\n\n\n'.format(self._news_data.get('feed', ''))
        for number, news in enumerate(self._news_data.get('news', []), start=1):
            news_text += self._get_news_text(number, news)
        print(news_text.rstrip())
        logging_info('All news have been printed in stdout in text format')

    @staticmethod
    def _get_news_text(number: int, news: Dict[str, Union[str, List[Dict[str, str]]]]) -> str:
        """Format news to correct text string."""
        links_values = DictionaryValues(news.get('links', {}))

        return '[News: {0}]\nTitle: {1}\nPublished: {2}\nLink: {3}\n\n{4}\n\nLinks:\n{5}\n\n'.format(
            number,
            news.get('title', ''),
            news.get('published', ''),
            news.get('link', ''),
            news.get('text', ''),
            ''.join(f'[{number}]: {link} ({key})\n' for number, (link, key) in enumerate(links_values, start=1)))


class DisplayNewsJson(DisplayNews):
    """Class display news in json format."""

    def print_news(self) -> None:
        """Print news in JSON format."""
        print(jsonmodule.dumps(self._news_data, ensure_ascii=False, indent=4))
        logging_info('All news are printed in stdout in JSON format')

    def validate_json(self) -> None:
        """Validate news data through JSON schema."""
        schema = self.read_json_schema_file()
        try:
            jsonschema.Draft7Validator.check_schema(schema)
            jsonschema.Draft7Validator(schema).validate(self._news_data)
        except jsonschema.exceptions.SchemaError as error:
            raise RSSNewsJSONSchemaException('Invalid JSON schema', error)
        except jsonschema.exceptions.ValidationError as error:
            raise RSSNewsJSONSchemaException('Well-formed but invalid JSON', error)
        else:
            logging_info('Successful validation of JSON schema and data')

    @staticmethod
    def _read_json_schema_file() -> Dict[str, List[Dict[str, Any]]]:
        """Read JSON schema file and load them."""
        if not path.isfile(JSON_SCHEMA):
            raise RSSNewsJSONSchemaException('Can\'t read json schema.')

        with open(JSON_SCHEMA, 'r') as schema_file:
            try:
                schema = jsonmodule.load(schema_file)
            except jsonmodule.decoder.JSONDecodeError as error:
                raise RSSNewsJSONSchemaException('Poorly-formed text, not JSON', error)
            else:
                logging_info('Successful read and load JSON schema file')
                return schema
