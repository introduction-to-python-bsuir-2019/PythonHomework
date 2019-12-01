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


class DirError(Exception):
    """
    This class should be raised, if received path is not a directory.
    """
    pass


class DirExistsError(Exception):
    """
    This class should be raised, if directory which was received by bath not exists.
    """
    pass


class DBConnectError(Exception):
    """
    This class should be raised, if received some problems with connection with database.
    """
    pass
