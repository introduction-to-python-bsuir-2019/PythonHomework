"""Module contains objects related to work database"""
import datetime
import logging
from typing import Dict, Any

import pymongo


class MongoDatabase:
    """MongoDatabase class"""
    def __init__(self, URL_CONNECTION: str, DB_NAME: str, COLLECTION_NAME: str):
        """Init MongoDatabase class"""
        self.url_connection: str = URL_CONNECTION
        self.db_name: str = DB_NAME
        self.collection_name: str = COLLECTION_NAME

    def database_connection(self) -> None:
        """Method for connecting to the database"""
        try:
            client = pymongo.MongoClient(self.url_connection)
            db = client[self.db_name]
            self.feed_collection = db[self.collection_name]
        except ConnectionError as ex:
            logging.error('Error connection to database')

    def _check_news_feed(self, data: Dict[str, Any]) -> bool:
        """Method for checking if an object is in the database"""
        return self.feed_collection.find(
            {"Feed": data["Feed"], "Url": data["Url"], "Date_Parsed": data["Date_Parsed"]}).count() == 0

    def _update_news_feed(self, new_news_feed: Dict[str, Any]) -> None:
        """
        Method for updating old news in the database
        when parsing a news feed again
        """
        old_news_feed = self.feed_collection.find_one(
            {"Feed": new_news_feed["Feed"], "Url": new_news_feed["Url"], "Date_Parsed": new_news_feed["Date_Parsed"]})

        news_update = []

        for new_news in new_news_feed["News"]:
            if new_news not in old_news_feed["News"]:
                news_update.append(new_news)

        update_old_news_feed = old_news_feed["News"] + news_update

        self.feed_collection.update_one({"Feed": old_news_feed["Feed"],
                                         "Url": old_news_feed["Url"],
                                         "Date_Parsed": old_news_feed["Date_Parsed"]},
                                        {"$set": {"News": update_old_news_feed}})

    def cache_news_feed(self, data: Dict[str, Any]) -> None:
        """Method for caching data.
        In which we determine whether the object exists and select an update or add
        """
        if self._check_news_feed(data):
            self.feed_collection.insert_one(data)
        else:
            self._update_news_feed(data)
        logging.info('Сached data')

    def get_news(self, limit: int, date: int, source: str) -> Dict:
        """Method for finding news in a database and issuing them according to parameters"""
        if date is None and limit is None:
            return self.feed_collection.find_one(
                {"Url": source, "Date_Parsed": datetime.datetime.today().strftime("%Y%m%d")}
            )
        elif date is None and limit is not None:
            news_feed = self.feed_collection.find_one(
                {"Url": source, "Date_Parsed": datetime.datetime.today().strftime("%Y%m%d")}
            )
            if 0 < limit <= news_feed["News"]:
                news_feed["News"] = news_feed["News"][:limit]
            return news_feed
        else:
            news_feed = self.feed_collection.find_one(
                {"Url": source, "Date_Parsed": str(date)}
            )
            if news_feed is None:
                print('Nothing found for a given date')
            else:
                if 0 < limit <= news_feed["News"]:
                    news_feed["News"] = news_feed["News"][:limit]
            return news_feed
