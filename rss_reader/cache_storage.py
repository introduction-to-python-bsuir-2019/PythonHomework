"""Contain all RSS news cache related objects."""
import logging
import os
from datetime import datetime
from operator import itemgetter
from typing import Any, Dict, List, Union

import tinydb
from tinydb_serialization import SerializationMiddleware
from tqdm import tqdm

from rss_reader.containers import DateTimeSerializer
from rss_reader.exceptions import RSSNewsCacheError


class CacheStorage:
    """Class cache RSS news."""

    def __init__(self, source: str) -> None:
        """Initialze cache storage."""
        self.source = source

    def init_cache_db(self, cache_file: str) -> tinydb.database.Table:
        """Initialze TinyDB and return source table."""
        if os.path.isfile(cache_file):
            serialization = SerializationMiddleware()
            serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
            cache_db = tinydb.TinyDB(cache_file, storage=serialization)
            logging.info('Successful initialze RSS cache database')
            return cache_db.table(self.source)
        else:
            raise RSSNewsCacheError('Can\'t read cache JSON file.')


class WriteCache(CacheStorage):
    """Class write cache news."""

    def __init__(self, source: str,
                 news: List[Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]]) -> None:
        """Initialze cache writing."""
        super().__init__(source)
        self.news_list = news

    def cache_news_list(self, db_table: tinydb.database.Table) -> None:
        """Verify cache data and cache news list to cache DB."""
        def add_to_change() -> None:
            """Add news to insert or update items in cache DB."""
            search = tinydb.Query()
            search_items = db_table.search((search.source == self.source) & (search.id == news_id))
            if search_items and not next(iter(search_items)).get('news') == news_data.get('news', ''):
                news_update.append(news_data)
            elif not search_items:
                news_insert.append(news_data)

        def add_changes_to_database() -> None:
            """Add news changes to cache DB."""
            db_table.insert_multiple(news_insert)
            search = tinydb.Query()
            for news in news_update:
                db_table.update(
                    news,
                    (search.source == self.source) & (search.id == news.get('id', ''))
                )

        news_insert = []
        news_update = []
        for news_data in tqdm(self.news_list, desc='Caching; ', leave=False):
            news_id = news_data.get('id', '')
            if self.verify_data(news_data):
                add_to_change()
        add_changes_to_database()

    @staticmethod
    def verify_data(news_data: Dict[str, Union[str, datetime, Dict[str, Union[str, List[Dict[str, str]]]]]]) -> None:
        """Verify cache data."""
        if not news_data.get('id', ''):
            return False
        published = news_data.get('date')
        if not isinstance(published, datetime):
            return False
        return True


class ReadCache(CacheStorage):
    """Class read cache news."""

    def __init__(self, source: str, date: datetime) -> None:
        """Initialze cache reading."""
        super().__init__(source)
        self.date = date

    def read_cache(self, db_table: tinydb.database.Table) -> Dict[Any, Any]:
        """Read cache data from 'date' to the end of the 'date' day."""
        search = tinydb.Query()
        news_cache = db_table.search(
            (search.source == self.source) &
            ((self.date <= search.date) & (search.date <= self.get_end_of_the_period(self.date)))
        )
        return sorted(news_cache, key=itemgetter('date'), reverse=True)

    @staticmethod
    def get_end_of_the_period(date: datetime) -> datetime:
        """Return end of the 'date' day."""
        return datetime(date.year, date.month, date.day, 23, 59, 59)
