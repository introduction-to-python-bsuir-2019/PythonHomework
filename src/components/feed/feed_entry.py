import html
from bs4 import BeautifulSoup
from datetime import datetime


class FeedEntry:

    def __init__(self, entry):
        self.title = html.unescape(entry.title)
        self.description = self._process_description(entry.description)
        self.link = entry.link
        self.links: list= self._process_links(entry.links)
        self.date = entry.published
        self.published = self._process_published(entry)

    def _process_links(self, links):
        def format_links(link, count):
            return f'[{count}]: {link["href"]} ({link["type"]})\n'

        return ''.join(
            format_links(link, count) for count, link in enumerate(links, start=1)
        )

    def _process_description(self, description):
        return html.unescape(
            BeautifulSoup(description, 'html.parser').get_text()
        )

    def _process_published(self, entry):
        return datetime(*entry.published_parsed[:6])
