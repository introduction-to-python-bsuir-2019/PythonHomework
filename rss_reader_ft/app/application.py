"""Module contains objects related to logs"""
import sys
import logging
from typing import Dict

from rss.data_loader import DataLoader
from rss.rss_feed import RSSFeed
from rss.print_data import Output
from app.argument_parser import ArgumentParser
from app.application_log import ApplicationLog


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

        data = DataLoader(self.dict_args['source']).upload()

        logging.info('Transfer data to RSSFeed class')
        feed = RSSFeed(self.dict_args, data)

        rss_data_dict = feed.data_processing()
        logging.info('Get the final output data')

        if self.dict_args["json"]:
            Output.to_json_format(rss_data_dict)
        else:
            Output.to_rss_format(rss_data_dict)
