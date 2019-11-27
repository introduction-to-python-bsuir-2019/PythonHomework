import sys


class RSS_reader_error(Exception):
    pass


class ArgError(RSS_reader_error):
    def __init__(self, msg):
        print(f'ArgError: {msg}')
        sys.exit(1)


class SourceConnectingError(RSS_reader_error):
    def __init__(self, source, msg):
        print(f"SourceConnectingError: Can't get feed from '{source}': {msg}")
        sys.exit(1)


class ParsingError(RSS_reader_error):
    def __init__(self, msg):
        print(f"ParsingError: Can't to parse feed: {msg}")
        sys.exit(1)


class CacheError(RSS_reader_error):
    def __init__(self, msg):
        print(f"CacheError: {msg}")
        sys.exit(1)
