import feedparser
from components.feed.feed_entry import FeedEntry


class Feed:

    def __init__(self, args):
        self._args = args
        self._entry_list = []
        self._title = []

        self._parse_feeds()

    def show_feeds(self):
        return

    def _parse_feeds(self):
        feeds = feedparser.parse(self._args.source)

        for feed in feeds.entries:
            self._append_feed_entry(feed)

    def _append_feed_entry(self, feed):
        self._entry_list.append(FeedEntry(feed))

    def get_entries(self):
        return type(self._feeds)
