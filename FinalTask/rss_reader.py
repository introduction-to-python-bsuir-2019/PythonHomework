#!/usr/bin/env python3

import argparse
from RSSHandle import RssHandler


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")

    parser.add_argument('source',
                        type=str,
                        help='RSS URL')

    parser.add_argument('--version',
                        action='version',
                        help='Print version info',
                        version='%(prog)s 0.1')

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

    rss_object = RssHandler(args.source)

    if args.json is True:
        rss_object.to_json()
