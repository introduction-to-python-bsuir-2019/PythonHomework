"""Application entry point module"""
from app.application import Application
import logging


def main() -> None:
    """The main entry point of the application"""
    try:
        app = Application()
        app.run_app()
    except Exception as ex:
        logging.error('Error. Close application.', exc_info=False)
        print(ex)


if __name__ == '__main__':
    main()
