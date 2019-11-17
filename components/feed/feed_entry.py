import html
from bs4 import BeautifulSoup


class FeedEntry:

    def __init__(self, feed):
        self.title = html.unescape(feed.title)
        self.date = feed.published
        self.link = feed.link
        self.description = self._process_description(feed.description)
        self.links = self._process_links(feed.links)

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
