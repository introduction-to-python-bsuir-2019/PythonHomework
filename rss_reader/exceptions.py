#!/usr/bin/env python3

"""
Exceptions for rss-reader
"""


class RSSFeedException(Exception):
    """ Custom exception class for RSSFeed errors """

    def __init__(self, message):
        super(RSSFeedException, self).__init__(message)
        self.message = message
