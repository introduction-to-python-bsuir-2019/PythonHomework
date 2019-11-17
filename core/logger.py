import logging
from typing import Optional

default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)


def create_logger(verbose: Optional[bool] = False) -> logging.Logger:
    """
    Creates new logger instance wich outputs messages to stdout, based on CLI verbose argument.

    Params:
        - verbose (bool): Whether to verbose the module output in console (optional, defaults to False)

    Returns:
        - Logger instance to use for application logging purposes
    """

    logger = logging.getLogger(__name__)
    format_pattern = "%(asctime)s %(levelname)s %(message)s"
    formatter = logging.Formatter(format_pattern)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.FATAL)

    return logger
