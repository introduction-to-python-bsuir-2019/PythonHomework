"""Contain application exceptions."""
from logging import info as logging_info
from typing import Optional


class RSSReaderException(Exception):
    """Application main exception."""

    def __init__(self, message: str, error: Optional[str] = None) -> None:
        """Initialze RSSReaderException class. Print error message."""
        print('{0}. RSS reader critical error'.format(message))
        logging_info('{0}{1}. RSS reader critical error'.format(message, f': {error}' if error else ''))


class RSSReaderParseException(RSSReaderException):
    """Parse exception."""

    def __init__(self, message: str) -> None:
        """Initialze RSSReaderParseException class. Print error message."""
        super().__init__(message)


class RSSNewsJSONSchemaValidationError(RSSReaderException):
    """JSON schema validation exception."""

    def __init__(self, message: str, error: str) -> None:
        """Initialze RSSNewsJSONSchemaValidationError class. Print error message."""
        super().__init__(message, error)


class RSSNewsJSONSchemaReadError(RSSReaderException):
    """JSON schema file read exception."""

    def __init__(self, message: str, error: str) -> None:
        """Initialze RSSNewsJSONSchemaReadError class. Print error message."""
        super().__init__(message, error)
