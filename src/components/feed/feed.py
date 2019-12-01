import feedparser
from datetime import timedelta
from src.components.helper import Map

from src.components.feed.feed_entry import FeedEntry
from src.components.feed.feed_formatter import FeedFormatter
from src.components.logger.logger import Logger
from src.components.cache.cache import Cache


class Feed:

    @property
    def entities_list(self):
        return self._entities_list

    @property
    def feeds_title(self):
        return self._feeds_title

    @property
    def feeds_encoding(self):
        return self._feeds_encoding

    def __init__(self, args):
        self._is_json = args.json
        self._is_colorize = args.colorize
        self._cache_date = args.date
        self._limit = args.limit
        self._url = args.source
        self._entities_list = []

        Logger.log('Initialize console variables')

        self._parse_feeds()

    def show_feeds(self) -> object:
        Logger.log(
            f'Preparation for output feeds. '
            f'Output type: {"JSON" if self._is_json else "DEFAULT"}. '
            f'Feeds choosen: {self._limit}'
        )

        FeedFormatter.is_json = self._is_json

        top_data_output = Map({
            'url': self._url,
            'title': self._feeds_title,
            'image': self._feeds_image
        })

        output = FeedFormatter.generate_output(
            self._decide_output(),
            self._limit,
            top_data_output,
            self._is_colorize
        )

        print(output)

    def _decide_output(self):
        if self._cache_date:
            return Cache().load_feeds_entries(self._url, self._cache_date, self._limit)

        return self._entities_list

    def _parse_feeds(self):

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

    def _set_global_feed_data(self, parse_data):
        Logger.log('Setting global feed data')

        self._feeds_title = parse_data.feed.title
        self._feeds_encoding = parse_data.encoding
        self._feeds_image = parse_data.feed.image.href

    def _append_feed_entry(self, item):
        self._entities_list.append(FeedEntry(item))

    def _store_cache_instances(self):

        cache_params = Map({
            'url': self._url,
            'encoding': self._feeds_encoding,
            'image' : self._feeds_image
        })

        Cache().append_feeds(cache_params, self._entities_list)
