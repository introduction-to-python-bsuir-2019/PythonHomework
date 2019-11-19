"""Application entry point module"""
import logging

from app.application import Application
from app.application_log import ApplicationLog


def main() -> None:
    """The main entry point of the application"""
    try:
        ApplicationLog.setup_logs()
        app = Application()
        app.run_app()
    except Exception as ex:
        logging.error('Error. Close application.', exc_info=False)
        print(ex)
