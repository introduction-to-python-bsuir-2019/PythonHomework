"""Contain application exceptions."""
import logging
from typing import Optional


class RSSReaderException(Exception):
    """Application main exception."""

    def __init__(self, message: str, error: Optional[str] = None) -> None:
        """Initialze RSS reader exception. Print error message."""
        print('{0}. RSS reader critical error'.format(message))
        logging.exception('{0}{1}. RSS reader critical error'.format(message, f': {error}' if error else ''))


class RSSNewsDisplayError(RSSReaderException):
    """News display exception."""

    def __init__(self, message) -> None:
        """Initialze RSS news display error."""
        super().__init__(message)


class RSSReaderParseException(RSSReaderException):
    """RSS source data parse exception."""

    def __init__(self, message: str) -> None:
        """Initialze RSS reader parse exception."""
        super().__init__(message)


class RSSNewsJSONSchemaException(RSSReaderException):
    """JSON schema exception."""

    def __init__(self, message: str, error: str) -> None:
        """Initialze RSS news JSON schema exception."""
        super().__init__(message, error)


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
