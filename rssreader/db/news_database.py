"""Database caching module"""

import logging
from pymongo import MongoClient
from datetime import datetime


class NewsDatabase():
    """Сlass for cache"""
    def __init__(self, url: str, date: int, limit: int = None) -> None:
        """Creates a database connection and a collection of news"""
        self.client = MongoClient("mongodb://mongo:27017/")
        self.db = self.client.news
        self.collection = self.db.news_received
        self.url = url
        self.date = date
        self.limit = limit
        logging.debug("Connected to the database")

    def __template_news(self, date: int, current_news: dict) -> dict:
        """Template for news in this format news is stored in the database"""
        return {"source": self.url, "date": date, "news": current_news}

    def __convert_date_format(self, date: str) -> str:
        """Convert date to format YYYYMMDD"""
        format_time = "%a, %d %b %Y %H:%M:%S %Z"
        if date.find("GMT") == -1:
            format_time = format_time.replace("Z", "z")

        return format_time

    def update_news(self, news: list) -> None:
        """Adding new news to the database. News replay check"""
        if news:
            for current_news in news:
                db_date = current_news["Date"]
                format_time = self.__convert_date_format(db_date)
                try:
                    date = int(str(datetime.strptime(
                            db_date,
                            format_time
                            ).date()).replace("-", ""))
                    template = self.__template_news(date, current_news)
                except ValueError:
                    logging.error("Date not in format UTC or GMT")

                if not self.collection.find_one(template):
                    self.collection.insert_one(template)

            logging.debug("Database news updated")

    def __search_caching_news(self) -> list:
        """Search for news in the database"""
        template = {"source": self.url, "date": self.date}
        find_news = self.collection.find(template, {"_id": 0})

        logging.debug("Search news in database")
        logging.info("Show caching news from database")
        if self.limit is not None:
            return find_news.limit(self.limit) if self.limit else []
        else:
            return find_news

    def show_news(self):
        """Getting news from the database"""
        return[curr_news["news"] for curr_news in self.__search_caching_news()]
