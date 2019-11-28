"""Contain application exceptions."""
import logging
from typing import Any, Optional


class RSSReaderException(Exception):
    """Application main exception."""

    def __init__(self, message: str, error: Optional[Any] = None) -> None:
        """Initialze RSS reader exception. Print error message."""
        logging.exception('{}. RSS reader critical error'.format(message), exc_info=error)


class RSSNewsDisplayError(RSSReaderException):
    """News display exception."""

    def __init__(self, message: str, error: str) -> None:
        """Initialze RSS news display error."""
        super().__init__(message, error)


class RSSReaderParseException(RSSReaderException):
    """RSS source data parse exception."""

    def __init__(self, message: str) -> None:
        """Initialze RSS reader parse exception."""
        super().__init__(message)


class RSSNewsCacheError(RSSReaderException):
    """News caching exception."""

    def __init__(self, message) -> None:
        """Initialze RSS news cache error."""
        super().__init__(message)


class RSSConvertationException(RSSReaderException):
    """News convertation exception."""

    def __init__(self, message: str, error: str) -> None:
        """Initialze RSS news JSON schema exception."""
        super().__init__(message, error)
