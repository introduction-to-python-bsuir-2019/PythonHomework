from src.components.cache.db.sqlite import Sqlite
from src.components.logger import Logger
from src.components.helper import Singleton
from src.components.helper import Map
from src.components.feed.feed_entry import FeedEntry
from .db.sqlite_scripts import scripts

from datetime import timedelta
from datetime import datetime
from pathlib import Path
import conf
import html


class Cache(Singleton):

    _db_name = 'cache.db'

    def __init__(self) -> None :

        self._cache_db_file = self._storage_initialize()

        self.db = Sqlite(str(self._cache_db_file))

    def _storage_initialize(self):

        cache_path = Path.home().joinpath('.' + conf.__package__)

        if not cache_path.exists():
            cache_path.mkdir()
            Logger.log(f'Created {conf.__package__} local dir with path: {cache_path}')

        cache_file = cache_path.joinpath(self._db_name)

        if not cache_file.exists():
            Sqlite.create_database(str(cache_file))
            Logger.log(f'Created local storage with path: {cache_file}')

        Logger.log(f'Cache local storage with path: {cache_file}')

        return cache_file

    def append_feeds(self, feed: dict, feed_entities_list: list) -> None:

        Logger.log(f'Check on feed cache exist on url: {feed.get("url")}')

        feed_id = self.db.find_where('feeds', 'url', feed.get("url"))

        if not feed_id:
            feed_id = self._insert_feed_data(feed)

        Logger.log('Start caching feeds: \n')

        for feed_entry in feed_entities_list:
            if not self.db.find_where('feeds_entries', 'link', feed_entry.link):
                Logger.log(f'Caching feed [[{feed_entry.title}]] INSERTED')
            else:
                Logger.log(f'Caching feed [[{feed_entry.title}]] UPDATED')

            self._insert_feed_entry_into_cache(feed_entry, feed_id)

        print("\n")
        Logger.log('Cached feeds was updated')

        self.db.close()

    def _insert_feed_entry_into_cache(self, entry: FeedEntry, feed_id):
        return self.db.write('feeds_entries', [
            'feed_id',
            'title',
            'description',
            'link',
            'links',
            'date',
            'published'
        ], [
            feed_id,
            html.escape(entry.title),
            html.escape(entry.description),
            entry.link,
            entry.links,
            entry.date,
            entry.published,
        ])

    def _insert_feed_data(self, feed):
        Logger.log(f'Add feed cache exist on url: {feed.get("url")}')

        self.db.write('feeds', ['url', 'encoding'], [feed.get('url'), feed.get("encoding")])

        return self.db.cursor.lastrowid

    def load_feeds_entries(self, date: str, limit=100) -> list:
        Logger.log(f'Load file from cache storage '
                   f'{date.strftime("from %d, %b %Y")}'
                   f'{(date + timedelta(days=1)).strftime(" to %d, %b %Y")}')

        date = datetime.combine(date, datetime.min.time())

        cache_list = self.get_specify_by_date(date, limit)

        return [Map(row) for row in cache_list]

    def get_specify_by_date(self, date, limit=100):
        cache_list = self.db.query(scripts.get('load_news'), date, date + timedelta(days=1), limit)
        return cache_list.fetchall()
