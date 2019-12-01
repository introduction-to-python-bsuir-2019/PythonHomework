"""Module contains objects related to logs"""
import logging


class ApplicationLog:
    """"ApplicationLog class"""
    @staticmethod
    def setup_logs() -> None:
        """Method that sets logger configuration parameters"""
        logging.basicConfig(
            filename="apps.log",
            filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        logging.info('Create base config for log')

    @staticmethod
    def print_log() -> None:
        """Method displays logs to the console"""
        logging.info('Print the logs from the apps.log file to stdout')

        with open("apps.log", "r") as file_handler:
            for line in file_handler:
                print(line)
