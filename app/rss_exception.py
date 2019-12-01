"""
    Contains RSSException class for exceptions
"""


class RSSException(Exception):
    """ For rss exceptions """
    def __init__(self, message=''):
        self.message = message
