from abc import ABCMeta, abstractmethod, abstractproperty
import typing
import json
import feedparser
import logging


class RssException(Exception):
    """
    Custom Exception class raised by RssBots classes
    """
    pass


class BaseRssBot(metaclass=ABCMeta):

    def __init__(self, url: str, limit: int, logger: logging.Logger):
        self.limit = limit
        self.logger = logger
        self.url = url
        feed = self._parse_raw_rss()
        self.news = self.get_news_as_dict(feed)  # news as dict

    def _parse_raw_rss(self) -> feedparser.FeedParserDict:
        """
        Parsing news by url

        Result stores into internal attribute self.feed
        :return: None
        """

        feed = feedparser.FeedParserDict()

        self.logger.info(f'Lets to grab news from {self.url}')

        feed = feedparser.parse(self.url)

        if feed.get('bozo_exception'):
            #
            exception = feed.get('bozo_exception').getMessage()
            raise RssException(f'Error while parsing xml: \n {exception}')

        self.logger.info(f'well formed xml = {feed["bozo"]}\n'
                         f'url= {feed["url"]}\n'
                         f'title= {feed["channel"]["title"]}\n'
                         f'description= {feed["channel"]["description"]}\n'
                         f'link to recent changes= {feed["channel"]["link"]}\n'
                         )
        return feed

    @abstractmethod
    def get_news(self) -> str:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """

    @abstractmethod
    def get_news_as_dict(self, feed: feedparser.FeedParserDict) -> typing.Dict[str, typing.Any]:
        """
        Returns str containing formatted news from internal attr self.feed

        :return: str with news
        """

    def get_json(self) -> str:
        """
        Return json formatted news
        :param news: news
        :return: json formatted string
        """

        return json.dumps(self.news, indent=4)

