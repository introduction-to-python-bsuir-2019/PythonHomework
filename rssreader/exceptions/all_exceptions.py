"""A module with custom exceptions"""

import argparse


class ArgumentParserError(Exception):
    """The exception class

    The exception that is thrown when
    the arguments are entered incorrectly

    """
    def __init__(self, message):
        self.message = message


class ThrowingArgumentParser(argparse.ArgumentParser):
    """
    The class that causes exclusion by overloading
    method error() of class ArgumentParser
    """
    def error(self, message) -> None:
        """
        Method that throws an exception in response
        to a built-in error of the module argparse
        """
        raise ArgumentParserError(message)


class InvalidLinkOrInternetConnectionError(Exception):
    """The exception class

    The exception that is thrown when
    the link are entered incorrectly

    """
    def __init__(self, message):
        self.message = message


class ParsingNewsError(Exception):
    """The exception class

    An exception that is thrown when it is not possible
    to receive news from rss

    """
    def __init__(self, message):
        self.message = message
