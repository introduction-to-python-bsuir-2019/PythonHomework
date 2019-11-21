#!/usr/bin/env python3

"""
Simple RSS reader
"""

__author__ = "DiSonDS"
__version__ = "0.3.0"
__license__ = "MIT"


import os
import sys
import time
import json
import pickle
import logging
import argparse
from datetime import datetime
from urllib.parse import urlparse

import feedparser
import requests
import bs4
from colorama import Fore


class RSSFeedException(Exception):
    """ Custom exception class for RSSFeed errors """
    def __init__(self, message):
        super(RSSFeedException, self).__init__(message)
        self.message = message


class RSSFeed:
    """ Class for rss feed """
    def __init__(self, source):
        self.source = source
        self.title = None
        self.entries = None
        self.raw_rss = None

    def _save_rss_in_file(self):
        """ Saving rss feed to cache/date/domain.rss """
        logging.info("Saving rss feed")
        directory = f"{datetime.now().strftime('%Y%m%d')}"
        if not os.path.exists(f"cache/{directory}"):
            logging.info("Creating directory /%s", directory)
            os.makedirs(f"cache/{directory}")

        uri = urlparse(self.source)
        domain_name = f"{uri.netloc}"
        with open(f"cache/{directory}/{domain_name}.rss", "wb") as file:
            logging.info("Saving entries in file %s/%s.rss", directory, domain_name)
            pickle.dump((self.title, self.entries), file)

    def _load_rss_from_file(self, date):
        """ Loading rss feed from cache/date/domain.rss """
        logging.info("Loading rss feed")
        directory = f"{date}"
        uri = urlparse(self.source)
        domain_name = f"{uri.netloc}"
        if not os.path.exists(f"cache/{directory}/{domain_name}.rss"):
            raise RSSFeedException(message=f"There is no entries for {date}")

        with open(f"cache/{directory}/{domain_name}.rss", "rb") as file:
            logging.info("Loading entries from file %s/%s.rss", directory, domain_name)
            self.title, self.entries = pickle.load(file)

    def _get_rss_in_json(self, entries):
        """ Converts rss feed to json """
        logging.info("Converting rss feed to json")
        return json.dumps({"feed": self.title, "entries": entries},
                          indent=2, ensure_ascii=False)

    def get_rss(self, date):
        """ Gets rss feed by source """
        logging.info("Getting rss feed")

        if date:
            self._load_rss_from_file(date)
            return

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

        self._save_rss_in_file()

    def print_rss(self, limit=None, is_json=False, colorize=False):
        """ Prints rss feed """

        if limit:
            entries = self.entries[:limit]
        else:
            entries = self.entries

        logging.info("Printing rss feed")

        if is_json:
            entries = self._get_rss_in_json(entries)
            print(entries)
        else:
            if colorize:
                print(f"{Fore.RED}Feed:{Fore.RESET} {self.title}\n")
                for entry in entries:
                    print(f"{Fore.GREEN}Title:{Fore.RESET} {entry['title']}\n"
                          f"{Fore.MAGENTA}Date:{Fore.RESET} {entry['date']}\n"
                          f"{Fore.BLUE}Link:{Fore.RESET} {entry['link']}\n\n"
                          f"{entry['summary']}\n\n")
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

    parser.add_argument("source", help="rss url")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument(
        "--verbose",
        action="count",
        default=False,
        help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", action="store", type=int, dest="limit")
    parser.add_argument("-d", "--date", action="store", type=int, dest="date")
    parser.add_argument("-c", "--colorize", action="store_true", help="Print colorized result in stdout")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    try:
        feed = RSSFeed(source=args.source)
        feed.get_rss(date=args.date)
        feed.print_rss(limit=args.limit, is_json=args.json, colorize=args.colorize)
    except RSSFeedException as ex:
        print(f"{ex.message}")
        sys.exit(0)

    logging.info("Exiting")


if __name__ == "__main__":
    main()
