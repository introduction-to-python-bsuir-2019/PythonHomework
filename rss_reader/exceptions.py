import sys


class RSS_reader_error(Exception):
    pass


class SourceConnectingError(RSS_reader_error):
    def __init__(self, source, msg):
        print(f"ERROR: Can't get feed from '{source}': {msg}")
        sys.exit(1)


class ParsingError(RSS_reader_error):
    def __init__(self, msg):
        print(f"ERROR: Can't to parse feed: {msg}")
