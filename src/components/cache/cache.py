from src.components.cache.db.sqlite import Sqlite
from src.components.logger import Logger
from src.components.helper import Singleton
from src.components.helper import Map
from src.components.feed.feed_entry import FeedEntry
from fabulous import color

from datetime import timedelta
from datetime import datetime
from pathlib import Path
import conf
import html


class Cache(Singleton):

    _db_name = 'cache.db'

    def __init__(self) -> None :

        self._cache_db_file = self._storage_initialize()
        self._db = Sqlite(str(self._cache_db_file))

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

    def append_feeds(self, feed: Map, feed_entities_list: list) -> None:

        Logger.log(f'Check on feed cache exist on url: {feed.url}')

        feed_id = self._db.find_where('feeds', 'url', feed.url, 'like')

        if not feed_id:
            feed_id = self._insert_feed_data(feed)

        Logger.log('Start caching feeds: \n')

        for feed_entry in feed_entities_list:
            if not self._db.find_where('feeds_entries', 'link', feed_entry.link, 'like'):
                Logger.log(f'Caching feed  {color.blue(feed_entry.title)}  INSERTED')
            else:
                Logger.log(f'Caching feed  {color.blue(feed_entry.title)}  UPDATED')

            self._insert_feed_entry_into_cache(feed_id, feed_entry)

        print("\n")
        Logger.log('Cached feeds was updated')

        self._db.close()

    def _insert_feed_entry_into_cache(self, feed_id, entry: FeedEntry):

        self._write_feed_entry_general(entry, feed_id)

        feed_entry_id = self._db.cursor.lastrowid

        self._write_feed_entry_links(feed_entry_id, entry)
        self._write_feed_entry_media(feed_entry_id, entry)

    def _insert_feed_data(self, feed: Map):
        Logger.log(f'Add feed cache exist on url: {feed.url}')

        self._db.write('feeds', [
            'url',
            'encoding',
            'image'
        ], [
            feed.url,
            feed.encoding,
            feed.image
        ])

        return self._db.cursor.lastrowid

    def _write_feed_entry_general(self, entry: FeedEntry, feed_id):
        return self._db.write(
            'feeds_entries',
            ['feed_id','title','description','link','published'],
            [feed_id,html.escape(entry.title),html.escape(entry.description),entry.link,entry.published,]
        )

    def _write_feed_entry_links(self, feed_entry_id, entry: FeedEntry):

        for link in entry.links:
            return self._db.write(
                'feed_entry_links',
                ['feed_entry_id','href','type',],
                [feed_entry_id, link.href,link.type,]
            )

    def _write_feed_entry_media(self, feed_entry_id, entry: FeedEntry):

        for media in entry.media:
            return self._db.write('feed_entry_media',
                ['feed_entry_id', 'url','additional',],
                [feed_entry_id,media.url,html.escape(media.alt),]
        )

    def load_feeds_entries(self, url: str, date: str, limit=100) -> list:
        Logger.log(
            f'Load file from cache storage '
            f'{date.strftime("from %d, %b %Y")}'
            f'{(date + timedelta(days=1)).strftime(" to %d, %b %Y")}'
        )

        date = datetime.combine(date, datetime.min.time())

        cache_list = self._get_specify_by_date(url, date, limit)

        if not cache_list:
            raise Exception(
                f'Cache retrive nothing. Storage for specified data is empty '
                f'{date.strftime("from %d, %b %Y")}'
                f'{(date + timedelta(days=1)).strftime(" to %d, %b %Y")}'
            )

        return self._db.map_data(cache_list)

    def _get_specify_by_date(self, url, date, limit=100):

        feed_id = self._db.find_where('feeds', 'url', url, 'like')

        cache_general_data = self._db.where('feeds_entries',
           ['feed_id', '=', feed_id],
           ['published','>=', date],
           ['published','<=', date + timedelta(days=1)],
           limit=limit
        )

        output_cache = []

        for cache_entry in self._db.map_data(cache_general_data):
            cache_entry['links'] = self._db.map_data(
                self._db.where('feed_entry_links', ['feed_entry_id', '=', cache_entry['id']])
            )

            cache_entry['media'] = self._db.map_data(
                self._db.where('feed_entry_media', ['feed_entry_id', '=', cache_entry['id']])
            )

            output_cache.append(cache_entry)

        return output_cache
