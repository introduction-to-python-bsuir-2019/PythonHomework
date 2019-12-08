"""This module contain class for structuring feeds cache entries"""

from src.components.feed.feed_entry import FeedEntry


class CacheEntry(FeedEntry):
    """
        This class implementing FeedEntry class.
        This is done because the class contains similar data and can
        be extended for cached entries
    """
    pass

