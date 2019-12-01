"""Contain application containers."""
from datetime import datetime
from typing import Dict, Generator, List

from tinydb_serialization import Serializer


class DictionaryValues:
    """Provide list of dictionaries values."""

    def __init__(self, list_of_dicts: List[Dict[str, str]]) -> None:
        """Initialze DictionaryValues class."""
        self.list_of_dicts = list_of_dicts

    def __iter__(self) -> Generator[List[str], None, None]:
        """Return list of dictionaries values."""
        for dictionary in self.list_of_dicts:
            yield dictionary.values()


class DateTimeSerializer(Serializer):
    """Encode and decode object 'datetime' for TinyDB."""

    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, date_obj):
        """Encode 'datetime' object to serializable object in TinyDB."""
        return date_obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, date_str):
        """Decode serializable object in TinyDB to 'datetime' object."""
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
