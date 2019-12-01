from .components.helper.singleton import Singleton
from .components.parser.parser import Parser
from .components.feed import *
from .components.logger.logger import Logger
from .components.converter.html import HtmlConverter
import conf


class App(Singleton):

    def __init__(self) -> None:
        console = Parser(
            'Pure Python command-line RSS reader.',
            conf.__description__
        )

        self._console_args = console.get_args()

        if self._console_args.verbose:
            Logger.initialize(self._console_args.colorize)

        self._feed = Feed(self._console_args)

        if self._console_args.to_html:
            HtmlConverter(self._console_args.to_html, self._console_args.limit).render(
                self._feed.entities_list, self._console_args.source, self._feed.feeds_title, self._feed.feeds_encoding
            )

    @classmethod
    def start(cls) -> object:
        return cls()._feed.show_feeds()


def main():
    try:
        App.start()
    except KeyboardInterrupt:
        Logger.log_error('\nStop Rss-Reader')


if __name__ == "__main__":
    main()
