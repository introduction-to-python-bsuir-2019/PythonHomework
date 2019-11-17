import html


class FeedEntry:

    def __init__(self, feed):
        self._title = feed.title

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self.title = html.unescape(title)
