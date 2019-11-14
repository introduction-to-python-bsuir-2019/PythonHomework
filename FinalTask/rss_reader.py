#!/usr/bin/env python3

import argparse
import logging
from RSSHandle import RssHandler


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument('source',
                        type=str,
                        help='RSS URL')

    parser.add_argument('--version',
                        action='store_true',
                        help='Print version info')

    parser.add_argument('--json',
                        action='store_true',
                        help='Print result as JSON in stdout')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='Outputs verbose status messages')

    parser.add_argument('--limit',
                        action='store',
                        type=int,
                        help='Limit news topics if this parameter provided')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    if args.version:
        print('\nRSS-Reader v2.0\n')

    rss_object = RssHandler(args.source)

    rss_object.output(args.json, args.limit)
