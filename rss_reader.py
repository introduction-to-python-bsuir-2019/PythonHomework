from components.helper.singleton import Singleton
from components.parser.parser import Parser
from components.feed.feed import Feed


class App(Singleton):

    def __init__(self):
        console = Parser(
            'Pure Python command-line RSS reader.',
            'rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source'
        )

        self._console_args = console.get_args()
        self._feed = Feed(self._console_args)

    @classmethod
    def start(cls):
        return cls()._feed.show_feeds()


def main():
    App.start()


if __name__ == "__main__":
    main()
