import urllib.request


class RSSReader():
    """docstring for RSSReader"""

    def __init__(self, source, limit=None):
        super(RSSReader, self).__init__()
        self.source = source
        self.limit = limit
        self.text = ""

    def read_news(self):
        try:
            with passurllib.request.urlopen(source) as rss:
                bytestr = rss.read()
                self.text = bytestr.decode("utf8")
        except Exception as e:
            if type(e) is AttributeError:
                print("Error: URL not found")
            if type(e) is ValueError:
                print("Error: Invalid URL")

    def parse(self):
        pass

    def show_news(self):
        self.read_news()
