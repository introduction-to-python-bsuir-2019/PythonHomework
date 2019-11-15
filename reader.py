import urllib.request
from xml.dom.minidom import parseString
from xml.dom.minidom import parse as parseFile
from html_parser import parse_HTML


class RSSReader():
    """RSSReader: class for reading rss channels"""

    def __init__(self, args):
        super(RSSReader, self).__init__()
        self.source = args.source
        self.limit = args.limit
        self.json = args.json
        self.verbose = args.verbose
        self.text = ""

    def __read_news(self):
        try:
            with urllib.request.urlopen(self.source) as rss:
                bytestr = rss.read()
                self.text = bytestr.decode("utf8")
        except Exception as e:
            if type(e) == ValueError:
                print("Error: Invalid URL")
            else:
                print("Unknown error")

    def __parse(self):
        xml = parseString(self.text)
        feed = xml.getElementsByTagName("title")[0].firstChild.data
        items = xml.getElementsByTagName("item")
        counter = 0
        column = []
        for item in items:
            if counter == self.limit:
                break
            counter += 1
            a = item.getElementsByTagName("description")[0].firstChild.data
            text, links = parse_HTML(a)
            column += [item.getElementsByTagName("title")[0].firstChild.data,
                       item.getElementsByTagName("pubDate")[0].firstChild.data,
                       item.getElementsByTagName("link")[0].firstChild.data,
                       text,
                       links]
        return feed, column

    def show_news(self):
        self.__read_news()
        feed, column = self.__parse()
        feed.replace("&#39;","'")
        print(f"Feed: {feed}")

