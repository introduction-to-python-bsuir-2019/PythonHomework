import argparse
import logging
from urllib.request import Request
from urllib.request import urlopen


def argparser():
    """Set argparser logic"""
    parser = argparse.ArgumentParser(description='base starter')
    parser.add_argument('source', action='store', help='Rss url authentication', type=str)
    parser.add_argument('--json', action='store_true', help='outputs result as JSON')
    parser.add_argument('--version', action='version', version='1.0', help='print version information')
    parser.add_argument('--verbose', action='store_true', help='outputs verbose status information')
    parser.add_argument('--limit', action='store', help='limits the number of topics', type=int, default=1)
    return parser.parse_args()


def get_rss(url):
    logging.info('URL opened for news reading: %s' % url)
    request = Request(url)
    logging.info('Read our request')
    rss = urlopen(request).read()
    return rss

argparser()

