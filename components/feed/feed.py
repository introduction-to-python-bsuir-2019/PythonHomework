import feedparser
import sys
from components.feed.feed_entry import FeedEntry
from components.feed.feed_formatter import FeedFormatter


class Feed:

    def __init__(self, args):
        self._is_json = args.json
        self._limit = args.limit
        self._url = args.source
        self._entities_list = []
        self._feeds_title = ''

        if args.verbose :
            sys.exit('[--verbose] did\'t implement yet')

        self._parse_feeds()

    def show_feeds(self):
        FeedFormatter.is_json = self._is_json
        output = FeedFormatter.generate_output(
            self._entities_list, self._limit, self._feeds_title
        )

        print(output)

    def _parse_feeds(self):
        feeds = feedparser.parse(self._url)

        self._set_global_feed_data(feeds.feed)

        for feed in feeds.entries:
            self._append_feed_entry(feed)

    def _set_global_feed_data(self, feed):
        self._feeds_title = feed.title

    def _append_feed_entry(self, feed):
        self._entities_list.append(FeedEntry(feed))
