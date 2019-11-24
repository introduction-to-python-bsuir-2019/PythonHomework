"""Module contains objects related to logs"""
import sys
from typing import Dict

from rss_reader_ft.app.application_log import ApplicationLog
from rss_reader_ft.app.argument_parser import ArgumentParser
from rss_reader_ft.rss.data_loader import DataLoader
from rss_reader_ft.rss.output import Output
from rss_reader_ft.rss.rss_feed import RSSFeed
from rss_reader_ft.db.mongodb import MongoDatabase


class Application:
    """Application class"""
    def __init__(self):
        """Init Application class"""
        self.dict_args: Dict = ArgumentParser.parse_args()

    def run_app(self) -> None:
        """Мethod sets application behavior"""

        if self.dict_args["verbose"]:
            ApplicationLog.print_log()
            sys.exit(1)

        mongo_db = MongoDatabase()
        mongo_db.database_connection()

        data = DataLoader(self.dict_args['source']).upload()

        feed = RSSFeed(self.dict_args, data)

        process_data = feed.data_processing()

        mongo_db.cache_news_feed(process_data)

        news = mongo_db.get_news(self.dict_args["limit"], self.dict_args["date"], self.dict_args["source"])
        if news is not None:
            if self.dict_args["json"]:
                Output.to_json_format(news)
            else:
                Output.to_rss_format(news)
