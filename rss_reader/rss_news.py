"""Contain all news display related objects."""
import json as jsonmodule
from logging import info as logging_info
from typing import Any, Dict, List, Union

import jsonschema

from rss_reader.config import JSON_SCHEMA
from rss_reader.containers import DictionaryValues
from rss_reader.rss_parser import RSSParser
from rss_reader.exceptions import RSSNewsJSONSchemaReadError, RSSNewsJSONSchemaValidationError


class RSSNews:
    """Class display news."""

    def __init__(self, source: str, limit: int, json: bool) -> None:
        """Initialze RSSNews class."""
        self.source = source
        self.json = json
        self.limit = limit
        logging_info('Initialze RSS news')

    def display_news(self) -> None:
        """Display news in text or JSON format."""
        logging_info('Started display news from a RSS URL')
        rss_parser = RSSParser()
        rss_parser.get_news(self.source)
        if self.json:
            self._print_news_json(rss_parser.news_data)
        else:
            self._print_news(rss_parser.news_data)
        logging_info('Ended display news from a RSS URL')

    def _print_news(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Print news in text format."""
        news_text = 'Feed: {0}:\n\n\n'.format(news_data.get('feed', ''))
        logging_info('Added RSS feed title to printing text')
        for number, news in enumerate(news_data.get('news', [])[:self.limit], start=1):
            news_text += self._get_news_text(number, news)
            logging_info(f'Added {number} news to printing text')
        print(news_text.rstrip())
        logging_info('All news are printed in stdout in text format')

    def _print_news_json(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Print news in JSON format."""
        self._validate_json(news_data)
        print(jsonmodule.dumps(news_data, ensure_ascii=False, indent=4))
        logging_info('All news are printed in stdout in JSON format')

    def _validate_json(self, news_data: Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Validate news data through JSON schema."""
        schema = self._read_json_schema_file()
        try:
            jsonschema.Draft7Validator.check_schema(schema)
            jsonschema.Draft7Validator(schema).validate(news_data)
        except jsonschema.exceptions.SchemaError as error:
            raise RSSNewsJSONSchemaValidationError('Invalid JSON schema', error)
        except jsonschema.exceptions.ValidationError as error:
            raise RSSNewsJSONSchemaValidationError('Well-formed but invalid JSON', error)
        else:
            logging_info('Successful validation of JSON schema and data')

    @staticmethod
    def _read_json_schema_file() -> Dict[str, List[Dict[str, Any]]]:
        """Read JSON schema file and load them."""
        try:
            with open(JSON_SCHEMA, 'r') as schema_file:
                schema = jsonmodule.load(schema_file)
        except IOError as error:
            raise RSSNewsJSONSchemaReadError('Can\'t read json schema.', error)
        except jsonmodule.decoder.JSONDecodeError as error:
            raise RSSNewsJSONSchemaValidationError('Poorly-formed text, not JSON', error)
        else:
            logging_info('Successful read and load JSON schema file')
            return schema

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
