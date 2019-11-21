"""Custom Rss Exceptions"""


class RssException(Exception):
    """
    Custom Exception class raised by RssBots classes
    """
    pass


class RssValueException(ValueError):
    """
    Custom Exception raised if date format is incorrect
    """
    pass


class RssNewsException(ValueError):
    """
    Custom Exception class raised if no news by date
    """
    pass