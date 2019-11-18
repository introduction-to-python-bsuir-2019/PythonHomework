import attr


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
    limit: int = attr.ib(default=10)
    width: int = attr.ib(default=120)
    json: bool = attr.ib(default=False)
    verbose: bool = attr.ib(default=False)
