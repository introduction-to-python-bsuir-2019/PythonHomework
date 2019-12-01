"""this module contain logger module for logging in console"""

import logging
import logging.config
import yaml
from src.components.helper.singleton import Singleton
import coloredlogs
from pathlib import Path


class Logger(Singleton):

    """
        Logger class using for wrap logger and provide more convenient approach for logging

        Attributes:
            logger_name  logger_name containt logger settings default name
    """

    logger_name:  str='standard'

    @classmethod
    def initialize(cls, is_colorize: bool) -> None :
        """
        This method initalize logger module for logging in project. Is_colorize using
        for decide is color cli output. Also logger config store in conf.yml
        :param is_colorize: bool
        :return: None
        """
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
    def log(cls, message: str) -> None:
        """
        This method wrap Logger info method
        :param message: str
        :return: None
        """
        if getattr(cls, '_logger', None) is not None:
            cls._logger.info(message)

    @classmethod
    def log_error(cls, message: str) -> None:
        """
        This method wrap Logger error method
        :param message: str
        :return: None
        """
        if getattr(cls, '_logger', None) is not None:
            cls()._logger.error(message)
