"""Module contains objects related to logs"""
import logging
import sys
from typing import Dict

from app.application_log import ApplicationLog
from app.argument_parser import ArgumentParser
from rss.data_loader import DataLoader
from rss.output import Output
from rss.rss_feed import RSSFeed


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

        process_data = feed.data_processing()
        logging.info('Get the final output data')

        if self.dict_args["json"]:
            Output.to_json_format(process_data )
        else:
            Output.to_rss_format(process_data )
