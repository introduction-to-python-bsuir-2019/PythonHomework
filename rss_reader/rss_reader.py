#!/usr/bin/env python3

"""
Simple RSS reader
"""

__author__ = "DiSonDS"
__version__ = "0.2.0"
__license__ = "MIT"


import sys
import feedparser
import argparse
import requests
import time
import logging
import json
import bs4

# from colorama import init  # for colorizing https://pypi.org/project/colorama/
# init(autoreset=True)


class RSSFeedException(Exception):
    def __init__(self, message):
        self.message = message


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
            return json.dumps({"feed": self.title, "entries": entries},
                              indent=2, ensure_ascii=False)
        else:
            return json.dumps({"feed": self.title, "entries": self.entries},
                              indent=2, ensure_ascii=False)

    def get_rss(self):
        """ Gets rss feed by source """
        logging.info("Getting rss feed")
        response = requests.get(self.source).text

        rss = feedparser.parse(response)
        if rss['bozo']:
            raise RSSFeedException(message="Incorrect url")
        self.title = rss['feed']['title']
        self.raw_rss = response
        self.entries = []
        for entry in rss.entries:
            self.entries.append({
                "title": entry.title,
                "date": time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed),
                "link": entry.link,
                "summary": bs4.BeautifulSoup(entry.summary, "html.parser").text
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
            print(f"Feed: {self.title}\n")
            for entry in entries:
                print(f"Title: {entry['title']}\n"
                      f"Date: {entry['date']}\n"
                      f"Link: {entry['link']}\n\n"
                      f"{entry['summary']}\n\n")


def main():
    """ Main entry point of the app """

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

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    try:
        feed = RSSFeed(source=args.source)
        feed.get_rss()
        feed.print_rss(limit=args.limit, is_json=args.json)
    except RSSFeedException as e:
        print(f"{e.message}")
        sys.exit(0)

    logging.info("Exiting")


if __name__ == "__main__":
    main()
