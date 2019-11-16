import sys
import urllib.request
import urllib.error
from xml.dom.minidom import parseString
from html_parser import parse_HTML


def output(string, sep=' ', end='\n', flush=False, verbose=True):
    """Output function for singe string but convert &#39; to '"""
    if verbose:
        string = string.replace("&#39;", "'")
        print(string, sep=sep, end=end, flush=flush)


def progress(elems, done, length=20):
    """Take arguments
    elems: count of elements
    done: progress (in elements)
    length: progress bar length
    Write progress bar to stdout
    """
    if done != 0:
        print("\r", end="")
    col = int(length * (done/elems))
    print(f"[{'='*col + ' '*(length-col)}] {int(100*done/elems)}%", end="")
    if elems == done:
        print()


class RSSReader():
    """RSSReader: Class for reading rss channels.
    Methods:
    show_news() - output news to stdout
    """

    def __init__(self, args):
        super(RSSReader, self).__init__()
        self.__source = args.source
        self.__limit = args.limit
        self.__json = args.json
        self.__verbose = args.verbose
        self.__text = ""

    def __read_news(self):
        """Read data from link"""
        try:
            output(f"Reading information from {self.__source}", end='...\n', verbose=self.__verbose)
            with urllib.request.urlopen(self.__source) as rss:
                bytestr = rss.read()
                self.__text = bytestr.decode("utf8")
            output("Complete.", verbose=self.__verbose)
        except Exception as e:
            if type(e) is ValueError:
                output("Error: Can't connect, please try with https://")
            elif type(e) is urllib.error.URLError:
                output("Error: Can't connect to web-site, please check URL")
            else:
                output("Unknown error")
            sys.exit()

    def __parse(self):
        """Parse XML data to python structures"""
        output("Parsing information...", verbose=self.__verbose)
        xml = parseString(self.__text)
        feed = xml.getElementsByTagName("title")[0].firstChild.data
        items = xml.getElementsByTagName("item")
        counter = 0
        if self.__verbose:
            progress(self.__limit, counter)
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
            if self.__verbose:
                progress(self.__limit, counter)
        return feed, column

    def show_news(self):
        """Read, parse and print info in stdout"""
        self.__read_news()
        feed, column = self.__parse()
        output(f"{feed}", end="\n\n")
        for news in column:
            output(f"Title: {news[0]}")
            output(f"Date: {news[1]}")
            output(f"Link: {news[2]}", end="\n\n")
            output(news[3], end="\n\n")
            if len(news[4]) != 0:
                output("Links:")
            for i in range(len(news[4])):
                output(f"[{i+1}]: {news[4][i]}")
            output("\n\n")

    def show_json(self):
        """Read, parse, convert into json and print info in stdout"""
        self.__read_news()
        feed, column = self.__parse()
        output("Convert to json...", verbose=self.__verbose)
        counter = 0
        if self.__verbose:
            progress(len(column), counter)
        json = '{\n  "title": "' + feed + '",\n  "news": ['
        separ = False
        for news in column:
            if separ:
                json += ','
            separ = True
            json += '{\n      "title": "' + news[0] + '",'
            json += '\n      "date": "' + news[1] + '",'
            json += '\n      "link": "' + news[2] + '",'
            json += '\n      "description": "' + news[3] + '",'
            json += '\n      "links": ['
            links = ""
            for lin in news[4]:
                links += f'\n        "{lin}",'
            if len(links) != 0:
                json += links[:-1] + "\n      ]"
            else:
                json += ']'
            json += "\n    }"
            counter += 1
            if self.__verbose:
                progress(len(column), counter)
        json += ']\n}'
        output(json)
