"""
This module provides functions to work with logging.
"""
import logging
import sys


def init_logger(name: str) -> logging.Logger:
    """
    Initialize and return logger object.
    :param name: Name of the logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    # create the logging file handler
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    stream_handler.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(stream_handler)
    return logger
