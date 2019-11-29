import sys
import urllib.request
import urllib.error
from xml.dom.minidom import parseString
from .html_parser import parse_HTML
from .converter import Converter


def stdout_write(string, sep=' ', end='\n', flush=False, verbose=True):
    """Output function for singe string but convert &#39; to '"""
    if verbose:
        string = string.replace("&#39;", "'")
        print(string, sep=sep, end=end, flush=flush)


def write_progressbar(elems, done, length=20):
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
    show_news() - print news to stdout
    """

    def __init__(self, source, limit, verbose, date):
        super(RSSReader, self).__init__()
        self.__source = source
        self.__limit = limit
        self.__verbose = averbose
        self.__date = date
        self.__text = ""

    def __find_news(self):
        pass

    def __cache_data(self, column, feed):
        Date = format(pubDate)
        formated_data = [
            (self.__source, Date, col["title"],
             col["link"], col["text"], col["links"]) for col in column]
        Database().write_data(formated_data, feed, self.__source)

    def __read_news(self):
        """Read data from link"""
        try:
            stdout_write(f"Reading information from {self.__source}", end='...\n', verbose=self.__verbose)
            with urllib.request.urlopen(self.__source) as rss:
                bytestr = rss.read()
                self.__text = bytestr.decode("utf8")
            stdout_write("Complete.", verbose=self.__verbose)
        except ValueError:
            stdout_write("Error: Can't connect, please try with https://")
            sys.exit()
        except urllib.error.URLError:
            stdout_write("Error: Can't connect to web-site, please check URL")
            sys.exit()
        except Exception:
            stdout_write("Unknown error")
            sys.exit()

    def __parse(self):
        """Parse XML data to python structures"""
        stdout_write("Parsing information...", verbose=self.__verbose)
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
            column += [{"title": item.getElementsByTagName("title")[0].firstChild.data,
                        "date": item.getElementsByTagName("pubDate")[0].firstChild.data,
                        "link": item.getElementsByTagName("link")[0].firstChild.data,
                        "text": text,
                        "links": links}]
            if self.__verbose:
                progress(self.__limit, counter)
        self.__cache_data(column, feed)
        return feed, column

    def __read():
        if not self.__date:
            self.__read_news()
            return self.__parse()
        return self.__find_news()

    def show_news(self):
        """Read and print info in stdout"""
        feed, column = self.__read()
        stdout_write(f"{feed}", end="\n\n")
        for news in column:
            stdout_write(f"Title: {news["title"]}")
            stdout_write(f"Date: {news["date"]}")
            stdout_write(f"Link: {news["link"]}", end="\n\n")
            stdout_write(news["text"], end="\n\n")
            if len(news["links"]) != 0:
                stdout_write("Links:")
            link_num = 1
            for link in news["links"]:
                stdout_write(f"[{link_num}]: {link}")
                link_num += 1
            stdout_write("\n\n")

    def show_json(self):
        """Read, parse, convert into json and print info in stdout"""
        feed, column = self.__read()
        json_text = Converter.to_json(feed, column, self.__verbose)
        stdout_write(json_text)
