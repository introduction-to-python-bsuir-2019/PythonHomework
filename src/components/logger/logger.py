import logging
import logging.config
import yaml
from src.components.helper.singleton import Singleton
import coloredlogs
from pathlib import Path

class Logger(Singleton):

    logger_name = 'standard'

    @classmethod
    def initialize(cls, is_colorize):

        with open(Path(__file__).parent.joinpath('conf.yml'), 'r') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

        cls._logger = logging.getLogger(cls.logger_name)

        if is_colorize:
            coloredlogs.install(
                fmt='%(asctime)s - %(message)s',
                datefmt='%H:%M:%S',
                field_styles={
                    'message' : dict(color='green'),
                    'asctime' : dict(color='red'),
                },
                level='DEBUG', logger=cls._logger
            )

    @classmethod
    def log(cls, message: str):
        if getattr(cls, '_logger', None) is not None:
            cls._logger.info(message)

    @classmethod
    def log_error(cls, message: str):
        if getattr(cls, '_logger', None) is not None:
            cls()._logger.error(message)
