import sys
import urllib.request
import urllib.error
from xml.dom.minidom import parseString
import dateutil.parser
from .html_parser import parse_HTML
from .converter import Converter
from .log_helper import stdout_write, write_progressbar
from .SQL_cache import Database


class RSSReader():
    """RSSReader: Class for reading rss channels.
    Methods:
    show_news() - print news to stdout
    show_json() - print news to stdout in json format
    """

    def __init__(self, source, limit, verbose, date):
        super(RSSReader, self).__init__()
        self.__source = source
        self.__limit = limit
        self.__verbose = verbose
        self.__date = date
        self.__text = ""

    def __find_news(self):
        """Ask database for news from entered date
        Return data in the same format with __parse function
        """
        output("Reading data from database...", verbose=self.__verbose)
        feed, data = Database().read_data(self.__source, self.__date)
        column = []
        if not data:
            stdout_write("Error: Articles from the entered date not found")
            sys.exit()
        counter = 0
        if self.__verbose:
            write_progressbar(len(data), counter)
        for news in data:
            column += [{"title": news[2],
                        "link": news[3],
                        "text": news[4],
                        "links": news[5].split('\n')}]
            counter += 1
            if self.__verbose:
                write_progressbar(len(data), counter)
        return feed[0][0], column

    def __cache_data(self, column, feed):
        """Take parsed data and write it to database"""
        stdout_write("Writing data to database...", verbose=self.__verbose)

        def date(pubDate): return dateutil.parser.parse(
            pubDate).strftime("%Y%m%d")
        formated_data = [
            (self.__source, date(col["date"]), col["title"],
             col["link"], col["text"], "\n".join(col["links"])) for col in column]
        Database().write_data(formated_data, feed, self.__source, self.__verbose)

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

    def __read(self):
        """Information source selection"""
        if not self.__date:
            self.__read_news()
            return self.__parse()
        return self.__find_news()

    def show_news(self):
        """Read and print info in stdout"""
        feed, column = self.__read()
        stdout_write(f"{feed}", end="\n\n")
        for news in column:
            stdout_write(f"Title: {news['title']}")
            if 'date' in news:
                stdout_write(f"Date: {news['date']}")
            stdout_write(f"Link: {news['link']}", end="\n\n")
            stdout_write(news['text'], end="\n\n")
            if len(news['links']) != 0:
                stdout_write("Links:")
            link_num = 1
            for link in news['links']:
                stdout_write(f"[{link_num}]: {link}")
                link_num += 1
            stdout_write("\n\n")

    def show_json(self):
        """Read, parse, convert into json and print info in stdout"""
        feed, column = self.__read()
        json_text = Converter.to_json(feed, column, self.__verbose)
        stdout_write(json_text)
