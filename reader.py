import sys
import urllib.request
import urllib.error
from xml.dom.minidom import parseString
from html_parser import parse_HTML


def output(string, sep=' ', end='\n', flush=False):
    """Output function for singe string but convert &#39; to '"""
    string = string.replace("&#39;", "'")
    print(string, sep=sep, end=end, flush=flush)
    

class RSSReader():
    """RSSReader: Class for reading rss channels.


    """
    def __init__(self, args):
        super(RSSReader, self).__init__()
        self.__source = args.source
        self.__limit = args.limit
        self.__json = args.json
        self.__verbose = args.verbose
        self.__text = ""

    def __read_news(self):
        """ """
        try:
            with urllib.request.urlopen(self.__source) as rss:
                bytestr = rss.read()
                self.__text = bytestr.decode("utf8")
        except Exception as e:
            if type(e) is ValueError:
                output("Error: Can't connect, please try with https://")
            elif type(e) is urllib.error.URLError:
                output("Error: Can't connect to web-site, please check URL")
            else:
                output("Unknown error")
            sys.exit()


    def __parse(self):
        xml = parseString(self.__text)
        feed = xml.getElementsByTagName("title")[0].firstChild.data
        items = xml.getElementsByTagName("item")
        counter = 0
        column = []
        for item in items:
            if counter == self.__limit:
                break
            counter += 1
            a = item.getElementsByTagName("description")[0].firstChild.data
            text, links = parse_HTML(a)
            column += [[item.getElementsByTagName("title")[0].firstChild.data,
                        item.getElementsByTagName("pubDate")[0].firstChild.data,
                        item.getElementsByTagName("link")[0].firstChild.data,
                        text,
                        links]]
        return feed, column

    def show_news(self):
        self.__read_news()
        feed, column = self.__parse()
        output(f"Feed: {feed}", end="\n\n")
        for news in column:
            output(f"Title: {news[0]}")
            output(f"Date: {news[1]}")
            output(f"Link: {news[2]}", end="\n\n")
            output(news[3], end="\n\n")
            output("Links:")
            for i in range(len(news[4])):
                output(f"[{i+1}]: {news[4][i]}")
            output("\n\n")
