"""Module contain classes for feed parsing logic and formatting feeds into appropriate mods"""

import feedparser
from argparse import ArgumentParser
from abc import ABC
from src.components.helper import Map
from src.components.feed.feed_entry import FeedEntry
from src.components.feed.feed_formatter import FeedFormatter
from src.components.logger.logger import Logger
from src.components.cache.cache import Cache


class FeedProperty(ABC):
    """Trait for Feed class.Contain all properties, which Feed use out of class """

    @property
    def entities_list(self) -> list:
        """Property provide value of feed parsed or cached entities"""
        return self._decide_output()

    @property
    def feeds_title(self) -> str:
        """Property provide value of feed general title"""
        return self._feeds_title

    @property
    def feeds_url(self) -> str:
        """Property provide value of feed origin url"""
        return self._url

    @property
    def feeds_image(self) -> str:
        """Property provide value of feed image url"""
        return self._feeds_image

    @property
    def feeds_encoding(self)-> str:
        """Property provide value of feed encoding"""
        return self._feeds_encoding


class Feed(FeedProperty):
    """This class represent parsing feed process,
    manage caching module, output data in proper way to console output"""

    def __init__(self, args: ArgumentParser) -> None:
        """
        This method initialize start required data for Feed class and call parser to parse feeds
        :param args: ArgumentParser
        """
        self._is_json = args.json
        self._is_colorize = args.colorize
        self._cache_date = args.date
        self._limit = args.limit
        self._url = args.source
        self._entities_list = []

        Logger.log('Initialize console variables')

        self._parse_feeds()

    def show_feeds(self) -> None:
        """
        This method using for output processed data into console into appropriate way
        :return: None
        """
        Logger.log(
            f'Preparation for output feeds. '
            f'Output type: {"JSON" if self._is_json else "DEFAULT"}. '
            f'Feeds choosen: {self._limit}'
        )

        FeedFormatter.is_json = self._is_json

        top_data_output = Map({
            'url': self._url,
            'title': self._feeds_title,
            'image': self._feeds_image,
            'encoding': self._feeds_encoding
        })

        output = FeedFormatter.generate_output(
            self._decide_output(),
            self._limit,
            top_data_output,
            self._is_colorize
        )

        print(output)

    def _decide_output(self) -> list:
        """
        This method realize which data will be ensure to use - cache or just parsed
        :return: List
        """
        if self._cache_date:
            return Cache().load_feeds_entries(self._url, self._cache_date, self._limit)

        return self._entities_list

    def _parse_feeds(self) -> None:
        """
        This method parsing feeds from provided url and process calls
        append entries to entries list and store to cache
        :return: None
        """
        Logger.log(f'Start parsing data from url: {self._url}')

        parse_data = feedparser.parse(self._url)

        if parse_data['bozo']:
            raise ValueError("Bozo Exception. Wrong validate or no access to the Internet")

        self._set_global_feed_data(parse_data)

        Logger.log('Generate feeds instances')

        for item in parse_data.entries:
            self._append_feed_entry(item)

        if self._entities_list:
            self._store_cache_instances()

    def _set_global_feed_data(self, parse_data: feedparser.FeedParserDict) -> None:
        """
        This method set all global feed data to Feed instatance
        :param parse_data: feedparser.FeedParserDict
        :return: None
        """
        Logger.log('Setting global feed data')

        self._feeds_title = parse_data.feed.title
        self._feeds_encoding = parse_data.encoding

        try:
            self._feeds_image = parse_data.feed.image.href

        except (AttributeError, KeyError):
            self._feeds_image = ''
            Logger.log('Cannot find feed image.')

    def _append_feed_entry(self, entry: feedparser.FeedParserDict) -> None:
        """
        This method wrap feed parser entry into FeedEntry class and append it to Feed list
        :param entry: feedparser.FeedParserDict
        :return: None
        """
        self._entities_list.append(FeedEntry(entry))

    def _store_cache_instances(self) -> None:
        """
        This method initialize Cache module and provide data to store in cache storage
        :return: None
        """
        cache_params = Map({
            'url': self._url,
            'encoding': self._feeds_encoding,
            'image' : self._feeds_image
        })

        Cache().append_feeds(cache_params, self._entities_list)
