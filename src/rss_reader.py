from .components.helper.singleton import Singleton
from .components.parser.parser import Parser
from .components.feed import *
from .components.logger.logger import Logger
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

    @classmethod
    def start(cls) -> object:
        return cls()._feed.show_feeds()


def main():
    try:
        App.start()
    except KeyboardInterrupt:
        Logger.log_error('Stop reader')


if __name__ == "__main__":
    main()
