#!/usr/bin/env python3

import argparse
import setuptools
import datetime


class RssHandler:
    pass


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
                    help='Limit news topics if this parameter provided')

parser.parse_args()
