import feedparser
from components.feed.feed_entry import FeedEntry
from components.feed.feed_formatter import FeedFormatter
from components.logger.logger import Logger


class Feed:

    def __init__(self, args):
        self._is_json = args.json
        self._limit = args.limit
        self._url = args.source
        self._entities_list = []
        self._feeds_title = ''

        Logger.log('Initialize console variables')

        if self._limit <= 0:
            Logger.log_error('Limit must be up to zero')
            raise ValueError('limit equal or less 0')

        self._parse_feeds()

    def show_feeds(self) -> object:
        Logger.log(f'Preparation for output feeds. '
                   f'Output type: {"JSON" if self._is_json else "DEFAULT"}. '
                   f'Feeds choosen: {self._limit}')

        FeedFormatter.is_json = self._is_json
        output = FeedFormatter.generate_output(
            self._entities_list, self._limit, self._feeds_title
        )

        print(output)

    def _parse_feeds(self):

        Logger.log(f'Start parsing data from url: {self._url}')
        feeds = feedparser.parse(self._url)

        self._set_global_feed_data(feeds.feed)

        Logger.log('Generate feeds instances')
        for feed in feeds.entries:
            self._append_feed_entry(feed)

    def _set_global_feed_data(self, feed):
        Logger.log('Setting global feed data')

        self._feeds_title = feed.title

    def _append_feed_entry(self, feed):
        self._entities_list.append(FeedEntry(feed))
