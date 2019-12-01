import html
from bs4 import BeautifulSoup
from datetime import datetime
from src.components.helper import Map


class FeedEntry:

    _soup: BeautifulSoup = BeautifulSoup

    def __init__(self, entry):

        self.link = entry.link
        self.title = html.unescape(entry.title)
        self.description = self._process_description(entry.summary)
        self.published = self._process_published(entry)

        self.links: list= self._process_links(entry.links)
        self.media: list= self._process_media(entry.summary)

    def _process_links(self, links):
        return [link for link in links if link.get('href', False)]

    def _process_media(self, summary):
        return [Map({
            'url': media.get('src'),
            'alt': html.escape(media.get('alt', ''))
        }) for media in self._soup(summary, 'lxml').find_all(['img']) if media.get('src', False)]

    def _process_description(self, description):
        return html.unescape(
            self._soup(description, 'lxml').get_text()
        )

    def _process_published(self, entry):
        return datetime(*entry.published_parsed[:6])
