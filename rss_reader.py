"""
Module Docstring
"""

__author__ = "DiSonDS"
__version__ = "0.1.0"
__license__ = "MIT"


import feedparser
import argparse
import requests
import time
import logging
import json

# from colorama import init  # for colorizing https://pypi.org/project/colorama/
# init(autoreset=True)


class RSSFeed:
    """ Class for rss feed"""
    def __init__(self, source):
        self.source = source
        self.title = None
        self.entries = None
        self.raw_rss = None

    def _get_rss_in_json(self, entries=False):
        """ Converts rss feed to json """
        logging.info("Converting rss feed to json")
        if entries:
            return json.dumps({"title": self.title, "entries": entries})
        else:
            return json.dumps({"title": self.title, "entries": self.entries})

    def get_rss(self):
        """ Gets rss feed by source """
        logging.info("Getting rss feed")
        response = requests.get(self.source).text

        rss = feedparser.parse(response)
        self.title = rss['feed']['title']
        self.raw_rss = response
        self.entries = []
        for entry in rss.entries:
            self.entries.append({
                "title": entry.title,
                "date": time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed),
                "link": entry.link,
                "summary": entry.summary
            })

    def print_rss(self, limit, is_json=False):
        """ Prints rss feed """
        logging.info("Printing rss feed")
        if not self.entries:
            print("error")

        if limit:
            entries = self.entries[:limit]
        else:
            entries = self.entries

        if is_json:
            entries = self._get_rss_in_json(entries)
            print(entries)
        else:
            print(self.title + "\n")
            for entry in entries:
                print(f"{entry['title']}\n"
                      f"{entry['date']}\n"
                      f"{entry['link']}\n\n"
                      f"{entry['summary']}\n\n")


def main(args):
    """ Main entry point of the app """

    feed = RSSFeed(source=args.source)
    feed.get_rss()
    feed.print_rss(limit=args.limit, is_json=args.json)

    logging.info("Exiting")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    # Required positional argument
    parser.add_argument("source", help="rss url")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    # Optional argument flag which defaults to False
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")

    # Optional verbosity counter
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Outputs verbose status messages")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-l", "--limit", action="store", type=int, dest="limit")

    args = parser.parse_args()
    main(args)
