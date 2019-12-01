"""This module contain classe for structuring feeds entries"""

import html
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from src.components.helper import Map


class FeedEntry:
    """
        This class represents feed entry structure and preprocess some entry values

        Attributes:
            _soup attribute provide access for work with BeautifulSoup interface
    """

    _soup: BeautifulSoup = BeautifulSoup

    def __init__(self, entry: feedparser.FeedParserDict) -> None:
        """
        This constructor init demand data for feed entry and formatting it
        :param entry: feedparser.FeedParserDict
        """
        self.link = entry.link
        self.title = html.unescape(entry.title)
        self.description = self._process_description(entry.summary)
        self.published = self._process_published(entry)

        self.links: list= self._process_links(entry.links)
        self.media: list= self._process_media(entry.summary)

    def _process_links(self, links) -> list:
        """
        Getting entry links and processing to check links
        :param links:
        :return:
        """
        return [link for link in links if link.get('href', False)]

    def _process_media(self, summary: str) -> list:
        """
        Getting entry text and retrieve media data from it
        :param summary:
        :return:
        """
        return [Map({
            'url': media.get('src'),
            'alt': html.escape(media.get('alt', ''))
        }) for media in self._soup(summary, 'lxml').find_all(['img']) if media.get('src', False)]

    def _process_description(self, description:str) -> str:
        """
        Getting entry text and formatting it into more readable format
        :param description:
        :return: str
        """
        return html.unescape(
            self._soup(description, 'lxml').get_text()
        )

    def _process_published(self, entry: feedparser.FeedParserDict) -> str:
        """
        Retrieve tuple of published data and process it into readable format
        :param entry: feedparser.FeedParserDict
        :return: str
        """
        return datetime(*entry.published_parsed[:6])
