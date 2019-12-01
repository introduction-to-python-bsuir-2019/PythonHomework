"""This module contain main rss-reader class App and entry point to utility"""

from .components.helper.singleton import Singleton
from .components.parser.parser import Parser
from .components.feed import *
from .components.logger.logger import Logger
from .components.converter.html import HtmlConverter
from .components.converter.pdf import PdfConverter
import conf


class App(Singleton):
    """General class of rss-reader. Implements all classes and run utility"""

    def __init__(self) -> None:
        """
        This constructor parse program arguments,
        initialize all module params decide witch logic to run
        """
        console = Parser(
            'Pure Python command-line RSS reader.',
            conf.__description__
        )

        self._console_args = console.get_args()

        if self._console_args.verbose:
            Logger.initialize(self._console_args.colorize)

        self._feed = Feed(self._console_args)

        if self._console_args.to_html:
            HtmlConverter(self._console_args.to_html, self._console_args.limit).render(self._feed)

        if self._console_args.to_pdf:
            PdfConverter(self._console_args.to_pdf, self._console_args.limit).render(self._feed)

    @classmethod
    def start(cls) -> None:
        return cls()._feed.show_feeds()


def main():
    """
    Entry point of rss-reader.
    """
    try:
        App.start()
    except KeyboardInterrupt:
        Logger.log_error('\nStop Rss-Reader')


if __name__ == "__main__":
    main()
