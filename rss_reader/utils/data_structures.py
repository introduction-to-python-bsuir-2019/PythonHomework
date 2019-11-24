import attr
from json import JSONEncoder
import pickle
import typing


def _default(self, obj):
    """ monkey-patches json module when it's imported so
    JSONEncoder.default() automatically checks for a special "to_json()"
    method and uses it to encode the object if found.
    """
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default


@attr.s(frozen=True)
class ConsoleArgs:
    """
    Structured class to store console args

    : url: news rss url
    : limit: limit of printed news
    : width: width of the screen to print the news
    : json: bool flag to print in json format
    : verbose: bool flag to set logger level
    """
    url: str = attr.ib()
    date: str = attr.ib(default='')
    to_pdf: str = attr.ib(default='')
    limit: int = attr.ib(default=10)
    width: int = attr.ib(default=120)
    json: bool = attr.ib(default=False)
    verbose: bool = attr.ib(default=False)


@attr.s()
class NewsItem:
    """
    Based structured class to store a news item

    : title: news' item title
    : link: news' link
    : published: string date
    : imgs: list of links to imgs
    : links: list of links to news' refs
    : html: html content of the news
    """

    title: str = attr.ib()
    link: str = attr.ib()
    published: str = attr.ib()
    imgs: typing.List[str] = attr.ib()
    links: typing.List[str] = attr.ib()
    html: str = attr.ib()

    def to_json(self):
        return self.__dict__


@attr.s(frozen=True)
class News:
    """
    Based structured class to store all news

    : title: feed's title
    : link: feed's link
    : news_items: news_items
    """
    feed: str = attr.ib()
    link: str = attr.ib()
    items: typing.Sequence[NewsItem] = attr.ib()

    def to_json(self):
        return self.__dict__
