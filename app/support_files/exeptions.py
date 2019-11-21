"""
This module provides exception classes.
"""


class FindFeedError(Exception):
    """
    This class should be raised, if received some problems with getting feed.
    """
    pass


class DateError(ValueError):
    """
    This class should be raised, if received some problems with converting date.
    """
    pass
