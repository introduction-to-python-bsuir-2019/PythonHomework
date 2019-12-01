import sys


class RSS_reader_error(Exception):
    pass


class ArgError(RSS_reader_error):
    def __init__(self, msg):
        self.msg = f'ArgError: {msg}'


class SourceConnectingError(RSS_reader_error):
    def __init__(self, source, msg):
        self.msg = f"SourceConnectingError: Can't get feed from '{source}': {msg}"


class ParsingError(RSS_reader_error):
    def __init__(self, msg):
        self.msg = f"ParsingError: Can't to parse feed: {msg}"


class CacheError(RSS_reader_error):
    def __init__(self, msg):
        self.msg = f"CacheError: {msg}"
