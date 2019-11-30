import feedparser
from datetime import timedelta

from src.components.feed.feed_entry import FeedEntry
from src.components.feed.feed_formatter import FeedFormatter
from src.components.logger.logger import Logger
from src.components.cache.cache import Cache


class Feed:

    def __init__(self, args):
        self._is_json = args.json
        self._cache_date = args.date
        self._limit = args.limit
        self._url = args.source
        self._entities_list = []

        Logger.log('Initialize console variables')

        self._pre_validate_params()

        self._parse_feeds()

    def _pre_validate_params(self):
        if self._limit <= 0:
            Logger.log_error('Limit must be up to zero')
            raise ValueError('limit equal or less 0')

        if not Cache().get_specify_by_date(self._cache_date, self._limit):
            raise Exception(f'There is no cached news '
                            f'{self._cache_date.strftime("from %d, %b %Y")}'
                            f'{(self._cache_date + timedelta(days=1)).strftime(" to %d, %b %Y")}')

    def show_feeds(self) -> object:
        Logger.log(f'Preparation for output feeds. '
                   f'Output type: {"JSON" if self._is_json else "DEFAULT"}. '
                   f'Feeds choosen: {self._limit}')

        FeedFormatter.is_json = self._is_json

        output = FeedFormatter.generate_output(
            self._decide_output(), self._limit, self._feeds_title
        )

        print(output)

    def _decide_output(self):
        if self._cache_date:
            return Cache().load_feeds_entries(self._cache_date, self._limit)

        return self._entities_list

    def _parse_feeds(self):

        Logger.log(f'Start parsing data from url: {self._url}')

        feed = feedparser.parse(self._url)

        self._set_global_feed_data(feed)

        Logger.log('Generate feeds instances')

        for item in feed.entries:
            self._append_feed_entry(item)

        if self._entities_list:
            self._store_cache_instances()

    def _set_global_feed_data(self, feed):
        Logger.log('Setting global feed data')

        self._feeds_title = feed.feed.title
        self._feeds_encoding = feed.encoding

    def _append_feed_entry(self, item):
        self._entities_list.append(FeedEntry(item))

    def _store_cache_instances(self):
        Cache().append_feeds({
            'url': self._url,
            'encoding': self._feeds_encoding,
        }, self._entities_list)
