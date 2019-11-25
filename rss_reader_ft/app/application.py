"""Module contains objects related to logs"""
import sys
from typing import Dict, Any

from rss_reader_ft.app.application_log import ApplicationLog
from rss_reader_ft.app.argument_parser import ArgumentParser
from rss_reader_ft.rss.data_loader import DataLoader
from rss_reader_ft.rss.output import Output
from rss_reader_ft.rss.rss_feed import RSSFeed
from rss_reader_ft.db.mongodb import MongoDatabase
from rss_reader_ft.db.mongodb_config import URL_CONNECTION, DB_NAME, COLLECTION_NAME


class Application:
    """Application class"""
    def __init__(self):
        """Init Application class"""
        self.dict_args: Dict[str, Any] = ArgumentParser.parse_args()

    def run_app(self) -> None:
        """Мethod sets application behavior"""

        mongo_db = MongoDatabase(URL_CONNECTION, DB_NAME, COLLECTION_NAME)
        mongo_db.database_connection()

        data = DataLoader(self.dict_args['source']).upload()

        feed = RSSFeed(self.dict_args, data)

        process_data = feed.data_processing()

        mongo_db.cache_news_feed(process_data)

        news = mongo_db.get_news(self.dict_args["limit"], self.dict_args["date"], self.dict_args["source"])
        if news is not None:
            if self.dict_args["json"]:
                Output.to_json_format(news)
            elif self.dict_args["to_html"]:
                Output.to_html_format(news)
            else:
                Output.to_rss_format(news)

        if self.dict_args["verbose"]:
            ApplicationLog.print_log()
            sys.exit(1)
