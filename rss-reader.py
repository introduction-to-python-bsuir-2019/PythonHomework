import argparse
from bs4 import BeautifulSoup as Soup4
from urllib.request import *
import re


def parsargument():
    parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
    parser.add_argument(
        'source',
        action='store',
        type=str,
        help='RSS URL'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s' + ' 0.0.1',
        help='Print version info'
    )
    parser.add_argument(
        '--json',
        help='Print result as JSON in stdout',
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Outputs verbose status messages',
        action='store_true'
    )
    parser.add_argument(
        '--limit',
        type=int,
        action='store',
        default=1,
        help='Limit news topics if this parameter provided'
    )
    return parser.parse_args()


def get_rss(url):
    req = Request(url)
    rss = urlopen(req).read()
    return rss


def get_news():
    """This function get information from rss page and print int cmd"""
    args = parsargument()
    soup = Soup4(get_rss(args.source), "lxml")
    items = soup.find_all('item', limit=args.limit)
    for item in items:
        date = item.find('pubdate').string
        title = item.find('title').string
        descrip = item.find('description').string
        description = re.sub('<.*?>', '', descrip)
        print(title.replace("&#39;", "'"))
        print("Date: " + date)
        print(description.replace("&#39;", "'"))
        print()

# print(args.verbose)
get_news()
