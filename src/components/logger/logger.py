import os
import logging
import logging.config
import yaml
from src.components.helper.singleton import Singleton


class Logger(Singleton):

    logger_name = 'standard'

    @classmethod
    def initialize(cls):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'conf.yml'), 'r') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

        cls._logger = logging.getLogger(cls.logger_name)

    @classmethod
    def log(cls, message: str):
        if getattr(cls, '_logger', None) is not None:
            cls._logger.info(message)

    @classmethod
    def log_error(cls, message: str):
        if getattr(cls, '_logger', None) is not None:
            cls()._logger.error(message)
