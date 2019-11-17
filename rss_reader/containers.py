"""Contain application containers."""
from typing import Dict, Generator, List


class DictionaryValues:
    """Provide list of dictionaries values."""

    def __init__(self, list_of_dicts: List[Dict[str, str]]) -> None:
        """Initialze DictionaryValues class."""
        self.list_of_dicts = list_of_dicts

    def __iter__(self) -> Generator[List[str], None, None]:
        """Return list of dictionaries values."""
        for dictionary in self.list_of_dicts:
            yield dictionary.values()


class FormatSpaces:
    """Provide a string with one space between words."""

    def __init__(self, string: str) -> None:
        """Initialze DictionaryValues class."""
        self.string = string

    def __str__(self) -> str:
        """Return a string with one space between words."""
        return ' '.join(self.string.split())
