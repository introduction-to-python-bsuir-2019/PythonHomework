"""Contain all RSS news cache related objects."""
from datetime import datetime
from logging import info as logging_info
from operator import itemgetter
from os import path
from typing import Any, Dict, List, Union

from tinydb import TinyDB, Query
from tinydb_serialization import SerializationMiddleware

from rss_reader.config import CACHE_DB
from rss_reader.containers import DateTimeSerializer
from rss_reader.exceptions import RSSNewsCacheError


class CacheStorage:
    """Class cache RSS news."""

    def __init__(self) -> None:
        """Initialze cache storage."""
        self.cache_db = self._init_cache_db()
        logging_info('Successful initialze RSS cache database')

    def _init_cache_db(self) -> TinyDB:
        """Initialze TinyDB."""
        if path.isfile(CACHE_DB):
            serialization = SerializationMiddleware()
            serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
            return TinyDB(CACHE_DB, storage=serialization)


class WriteCache(CacheStorage):
    """Class write cache news."""

    def __init__(self,
                 news: List[Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]]) -> None:
        """Initialze cache writing."""
        super().__init__()
        self.news_list = news

    def cache_news_list(self) -> None:
        """Verify cache data and cache news list to cache DB."""
        for news in self.news_list:
            try:
                self.verify_news_data(news)
            except RSSNewsCacheError:
                pass
            else:
                self.cache_news(news)

    def cache_news(self, news: Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Cache or update news in cache DB."""
        news_source = news.get('source', '')
        news_id = news.get('id', '')
        search = Query()
        if news_id and self.cache_db.search((search.source == news_source) & (search.id == news_id)):
            self.cache_db.update(news, (search.source == news_source) & (search.id == news_id))
        else:
            self.cache_db.insert(news)

    @staticmethod
    def verify_news_data(news: Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Verify cache data."""
        if not news.get('source', ''):
            raise RSSNewsCacheError(f'Cache error: news don\'t have \'Source\'')
        if not news.get('id', ''):
            raise RSSNewsCacheError('Cache error: news don\'t have \'ID\'')
        news_date = news.get('date')
        if not isinstance(news_date, datetime):
            raise RSSNewsCacheError(f'Cache error: news have invalid date type {type(news_date)}')


class ReadCache(CacheStorage):
    """Class read cache news."""

    def __init__(self, source: str, date: datetime) -> None:
        """Initialze cache reading."""
        super().__init__()
        self.date = date
        self.source = source

    def read_cache(self) -> Dict[Any, Any]:
        """Read cache data from 'date' to the end of the 'date' day."""
        search = Query()
        news_cache = self.cache_db.search(
            (search.source == self.source) &
            ((self.date <= search.date) & (search.date <= self.get_end_of_the_date(self.date)))
        )
        return sorted(news_cache, key=itemgetter('date'), reverse=True)

    @staticmethod
    def format_data(data: List[Dict[Any, Any]]) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
        """Format cache data do display data."""
        display_data = {'feed': '', 'news': []}
        news_temp = {'title': '', 'published': '', 'link': '', 'text': '', 'links': []}
        if data:
            display_data.update({'feed': data[0].get('feed', '')})
        news_list = []
        for feed_data in data:
            news_data = feed_data.get('news', {})
            news = news_temp.copy()
            news.update({'title': news_data.get('title', ''),
                         'published': news_data.get('published', ''),
                         'link': news_data.get('link', ''),
                         'text': news_data.get('text', ''),
                         'links': news_data.get('links', [])})
            news_list.append(news)
        display_data.update({'news': news_list})

        return display_data

    @staticmethod
    def get_end_of_the_date(date: datetime) -> datetime:
        """Return end of the 'date' day."""
        return datetime(date.year, date.month, date.day, 23, 59, 59)
