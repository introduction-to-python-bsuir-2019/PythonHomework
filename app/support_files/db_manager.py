"""
This module contains class to work with database.
"""
import os
from dataclasses import asdict
from time import strptime, mktime, altzone, localtime, struct_time
from typing import Optional

from pymongo import MongoClient, errors

from app.support_files.app_logger import get_logger
from app.support_files.config import APP_NAME
from app.support_files.dtos import Feed, Item
from app.support_files.exeptions import FindFeedError, DateError, DBConnectError


class DBManager:
    """
    Class to work with database.
    """

    def __init__(self) -> None:
        mongo_host = os.getenv('MONGO_HOST', '127.0.0.1')
        client = MongoClient(f"mongodb://{mongo_host}:27017/")
        try:
            client.server_info()
        except errors.ServerSelectionTimeoutError:
            raise DBConnectError(f"Can't connect to database with host - {mongo_host} and port - 27017")
        self._db = client["feed_db"]
        self._collection = self._db["feed_collection"]
        self._logger = get_logger(APP_NAME)

    def insert_feed(self, feed: Feed) -> None:
        """
        Insert feed in database.
        If this feed exists in the database, then news is added that was not there.
        :param feed: Feed, which should be inserted.
        """
        self._logger.info("Loading data from database to join with inserted data is started")
        cashed_feed = self.find_feed_by_link(feed.rss_link)
        self._logger.info("Loading data from database to join with inserted data is finished")

        if cashed_feed is not None:
            items = set(feed.items)
            cashed_items = set(cashed_feed.items)
            result_items = list(set(items).union(set(cashed_items)))
            result_items = list(map(asdict, result_items))
            self._collection.update_one({"rss_link": feed.rss_link}, {"$set": {"items": result_items}})
        else:
            self._collection.insert_one(asdict(feed))
        self._logger.info("New and old data are joined")

    def find_feed_by_link(self, link: str) -> Optional[Feed]:
        """
        Looks for feed in the database by rss link and returns it.
        :param link: Rss link.
        :return: Feed, if it exist, otherwise None.
        """
        dict_feed = self._collection.find_one({"rss_link": link})
        if dict_feed is None:
            return None
        del dict_feed["_id"]
        feed = Feed(**dict_feed)
        feed.items = [Item(**item) for item in dict_feed["items"]]
        return feed

    def find_feed_by_link_and_date(self, link: str, date: str, limit: int = -1) -> Feed:
        """
        Looks for feed in the database by rss link and date and returns it.
        Raise DateError, in it not exist.
        :param link: Rss link.
        :param date: Need date.
        :param limit: Limit count of returned items.
        :return: Feed, if it exist.
        """
        try:
            date = strptime(date, "%Y%m%d")
        except ValueError as err:
            raise DateError(err.__str__())
        feed = self.find_feed_by_link(link)
        if feed is None:
            raise FindFeedError("This feed is not cashed")
        result_items = []
        count = limit
        for item in feed.items:
            item_date = struct_time(item.published_parsed)
            l_i_date = localtime(mktime(tuple(item_date)) - altzone)
            if (l_i_date.tm_year, l_i_date.tm_mon, l_i_date.tm_mday) == (date.tm_year, date.tm_mon, date.tm_mday):
                result_items.append(item)
                count -= 1
            if count == 0:
                break
        feed.items = result_items
        return feed

    def truncate_collection(self) -> None:
        """
        Truncate database.
        """
        self._collection.delete_many({})


if __name__ == "__main__":
    DBManager()
