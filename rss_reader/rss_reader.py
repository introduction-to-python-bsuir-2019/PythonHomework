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
import copy
import json
import pickle
import logging
import argparse
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

import feedparser
import requests
import bs4
from colorama import Fore

from rss_reader.exceptions import RSSFeedException
from rss_reader.converter import Converter
from rss_reader.configuration import CACHE_DIR


class RSSFeed:
    """ Class for RSS feed

        Attributes:
            source (str): URL of RSS feed
            title (str): Title of RSS feed
            entries (list): List of pretty RSS news
            raw_entries (list): List of raw RSS news
    """

    def __init__(self, source):
        self.source = source
        self.title = None
        self.entries = None
        self.raw_entries = None

    def _save_rss_in_file(self):
        """ Saving rss feed to cache/date/domain.rss """
        logging.info("Saving rss feed")

        date_dir = Path(datetime.now().strftime('%Y%m%d'))
        cache_file_dir = CACHE_DIR / date_dir
        if not cache_file_dir.is_dir():
            logging.info("Creating directory /%s", cache_file_dir)
            os.makedirs(cache_file_dir)

        uri = urlparse(self.source)
        file_name = f"{uri.netloc}.rss"

        cache_file_path = cache_file_dir / file_name
        with open(cache_file_path, "wb") as file:
            logging.info("Saving entries in file %s", cache_file_path)
            pickle.dump((self.title, self.raw_entries), file)

    def _load_rss_from_file(self, date):
        """ Loading rss feed from cache/date/domain.rss """
        logging.info("Loading rss feed")

        date_dir = Path(str(date))
        uri = urlparse(self.source)
        file_name = f"{uri.netloc}.rss"

        cache_file_path = CACHE_DIR / date_dir / file_name
        if not cache_file_path.is_file():
            raise RSSFeedException(message=f"There is no entries for {date}")

        with open(cache_file_path, "rb") as file:
            logging.info("Loading entries from file %s", cache_file_path)
            self.title, self.raw_entries = pickle.load(file)
            self.entries = self._get_pretty_entries()

    def _get_rss_in_json(self, entries):
        """ Converts rss feed to json """
        logging.info("Converting rss feed to json")
        return json.dumps({"feed": self.title, "entries": entries},
                          indent=2, ensure_ascii=False)

    def _get_pretty_entries(self):
        """ Prettify entries

        Remove HTML code from summary, parse date
        """
        pretty_entries = []
        for entry in self.raw_entries:
            pretty_entries.append({
                "title": entry.title,
                "date": time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed),
                "link": entry.link,
                "summary": bs4.BeautifulSoup(entry.summary, "html.parser").text.strip()
            })
        return pretty_entries

    def get_rss(self, date):
        """ Gets rss feed from source or cache"""
        logging.info("Getting rss feed")

        if date:
            self._load_rss_from_file(date)
            return

        response = requests.get(self.source).text
        rss = feedparser.parse(response)
        if rss['bozo']:
            raise RSSFeedException(message="Incorrect url")

        self.title = rss['feed']['title']
        self.raw_entries = rss.entries
        self.entries = self._get_pretty_entries()

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

    def convert_to_html(self, directory, limit):
        """ Create html file with rss news in DIR """
        logging.info("Converting RSS to HTML")
        converter = Converter(title=self.title, entries=copy.deepcopy(self.raw_entries[:limit]), directory=directory)
        converter.rss_to_html()
        logging.info("Done.")

    def convert_to_pdf(self, directory, limit):
        """ Create pdf file with rss news in DIR """
        logging.info("Converting RSS to PDF")
        converter = Converter(title=self.title, entries=copy.deepcopy(self.raw_entries[:limit]), directory=directory)
        converter.rss_to_pdf()
        logging.info("Done.")


def get_args():
    """ Parse and return provided args """
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
    parser.add_argument("--to-html", action="store", type=str)
    parser.add_argument("--to-pdf", action="store", type=str)

    return parser.parse_args()


def main():
    """ Main entry point of the app """

    args = get_args()

    if args.verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.info("Verbose output.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    try:
        feed = RSSFeed(source=args.source)
        feed.get_rss(date=args.date)
        feed.print_rss(limit=args.limit, is_json=args.json, colorize=args.colorize)
        if args.to_html:
            feed.convert_to_html(directory=args.to_html, limit=args.limit)
        if args.to_pdf:
            feed.convert_to_pdf(directory=args.to_pdf, limit=args.limit)
    except RSSFeedException as ex:
        print(f"{ex.message}")
        sys.exit(0)
    finally:
        logging.info("Exiting")


if __name__ == "__main__":
    main()
