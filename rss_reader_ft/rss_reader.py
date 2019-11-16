from app.application import Application
import logging as log


def main():
    """
    main
    """
    try:
        Application.init_config_log()
        app = Application()
        app.run_app()
    except Exception as ex:
        log.error(f'Error \n Close application.', exc_info=False)


if __name__ == '__main__':
    main()
