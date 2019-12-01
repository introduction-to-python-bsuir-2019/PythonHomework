"""A module which is responsible for the logic of logs"""

import os
import logging


class AppLogging:
    """A class that contains methods responsible for logs"""
    @staticmethod
    def setup_logs(file_path) -> None:
        """
        Method that configures the log config
        storage location, output format
        """
        logging.basicConfig(
                filename=file_path,
                filemode="a",
                format="%(asctime)s - %(levelname)s - %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S',
                level=logging.DEBUG
            )

    @staticmethod
    def log_setup() -> None:
        """
        Method that configures the logs and checks
        whether the application has already been launched
        """
        file_path = "app_logging.log"

        with open("app_logging.log", "w") as wf:
            AppLogging.setup_logs(file_path)

    @staticmethod
    def show_logs() -> str:
        """Method that returns all the logs"""
        with open("app_logging.log", "r") as rf:
            logging.info("Show logs")
            return "Logs:\n" + "".join([line for line in rf])
