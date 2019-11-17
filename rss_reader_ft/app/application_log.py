"""Module contains objects related to logs"""
import logging


class ApplicationLog:
    """"ApplicationLog class"""
    @staticmethod
    def setup_logs() -> None:
        """Method that sets logger configuration parameters"""
        logging.basicConfig(
                filename="apps.log",
                filemode="a",
                format="%(asctime)s - %(levelname)s - %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S',
                level=logging.INFO
            )
        logging.info('Create base config')

    @staticmethod
    def print_log() -> None:
        """Method displays logs to the console"""
        logging.info('We print the logs from the file data from the app.log file to stdout')
        print(2)
        with open("apps.log", "r") as file_handler:
            for line in file_handler:
                print(line)
