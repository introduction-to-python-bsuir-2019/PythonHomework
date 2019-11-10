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

# from colorama import init  # for colorizing https://pypi.org/project/colorama/
# init(autoreset=True)


def get_rss(source):
    """ Gets rss feed by source """
    response = requests.get(source)
    rss = feedparser.parse(response.text)
    return rss


def print_rss(rss):
    """ Prints rss feed """
    print(f"Feed: {rss['feed']['title']}\n")
    for entry in rss.entries:
        print(f"{entry.title}\n"
              f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', entry.published_parsed)}\n"
              f"{entry.link}\n\n"
              f"{entry.summary}\n\n")


def main(args):
    """ Main entry point of the app """
    source = args.source
    rss = get_rss(source)
    print_rss(rss)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

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
