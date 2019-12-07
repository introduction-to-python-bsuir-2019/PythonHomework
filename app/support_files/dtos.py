"""
This module contains data classes to work with feeds.
"""
from dataclasses import dataclass, field
from time import struct_time, localtime, time
from typing import List


@dataclass
class Item:
    """
    This class represents each item in feed.
    """
    title: str = "no title"
    link: str = "no link"
    author: str = "no author"
    published_parsed: struct_time = localtime(time())
    description: str = "description"
    img_links: List[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(str(self.__dict__))


@dataclass
class Feed:
    """
    This class represents feed.
    """
    rss_link: str
    title: str = "no title"
    link: str = "no link"
    items: List[Item] = field(default_factory=list)
